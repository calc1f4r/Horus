---
# Core Classification
protocol: generic
chain: everychain
category: economic
vulnerability_type: missing_slippage_protection

# Attack Vector Details
attack_type: economic_exploit
affected_component: bonding_curves, buy_sell_functions, liquidity_operations, token_graduation

# Technical Primitives
primitives:
  - slippage_protection
  - minAmountOut
  - maxAmountIn
  - bonding_curve_pricing
  - token_supply_dependent_pricing
  - mempool_monitoring
  - front_running
  - sandwich_attack
  - graduation_slippage
  - liquidity_deposit_manipulation

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.80
financial_impact: high

# Context Tags
tags:
  - slippage
  - bonding_curve
  - sandwich_attack
  - front_running
  - price_manipulation
  - mev
  - defi
  - launchpad
  - token_launch
  - liquidity_locking
  - market_seat
  - credit_tokens

# Version Info
language: solidity
version: ">=0.6.0"
---

## References
- [Report-01]: reports/bonding_curve_findings/m-01-no-slippage-protection-for-market-functions.md
- [Report-02]: reports/bonding_curve_findings/m-02-missing-slippage-protection-on-buy-and-sell.md
- [Report-03]: reports/bonding_curve_findings/m-02-missing-slippage-protection-on-sellcredits.md
- [Report-04]: reports/bonding_curve_findings/lack-of-slippage-protection-in-swaptokensforcounterpart-and-addliquidity-makes-e.md
- [Report-05]: reports/bonding_curve_findings/missing-slippage-protection-for-locking-liquidity.md
- [Report-06]: reports/bonding_curve_findings/missing-slippage-protection-in-market-seat-buysell-operations.md
- [Report-07]: reports/bonding_curve_findings/m-24-launchpad-slippage-is-not-enforced-properly-during-token-graduation.md
- [Report-08]: reports/bonding_curve_findings/ineffective-slippage-control.md
- [Report-09]: reports/bonding_curve_findings/m-3-no-slippage-or-deadline-control-for-swapping-while-stability-burning.md
- [Report-10]: reports/bonding_curve_findings/m-02-an-error-in-the-minordersize-check.md

## Vulnerability Title

**Missing or Ineffective Slippage Protection on Bonding Curve Buy/Sell Operations**

### Overview

Bonding curve protocols consistently fail to implement proper slippage protection on buy, sell, liquidity provision, and graduation operations. Because bonding curve prices are deterministically computed from current token supply, any change in supply between transaction submission and execution changes the price — making these functions inherently vulnerable to sandwich attacks, front-running, and unexpected price shifts. This pattern appears across EVM, Solana, and Rust-based protocols with 10 distinct variants documented below.

### Vulnerability Description

#### Root Cause

The fundamental issues across all 10 findings:

1. **No slippage parameters at all** — Buy/sell functions accept no `minAmountOut` or `maxAmountIn`, leaving users completely unprotected (Reports 1, 2, 3, 6)
2. **Zero amountOutMin in UniswapV2 Router calls** — Internal swap/liquidity functions hardcode `0` for slippage (Report 4)
3. **Slippage calculated from manipulable on-chain state** — Using current pool price to compute expected liquidity allows sandwich (Report 8)
4. **Slippage check in wrong code path** — Check applied before value reassignment, bypassed when graduation triggers (Reports 7, 10)
5. **Missing deadline parameter** — Transactions can sit in mempool indefinitely, executing at stale prices (Report 9)
6. **Liquidity locking without price range checks** — UniswapV3 position conversion can be sandwiched (Report 5)

---

### Vulnerable Pattern Examples

---

#### **Pattern 1: No Slippage on Bonding Curve Share Buy/Sell** [MEDIUM]
**Protocol**: Canto | **Auditor**: Code4rena | **Severity**: Medium | **Finders**: rice_cooker, glcanvas, neocrao +54 others

```solidity
// ❌ VULNERABLE: No slippage parameter — price depends on current tokenCount
// https://github.com/code-423n4/2023-11-canto/blob/main/1155tech-contracts/src/Market.sol#L132-L145

function getBuyPrice(uint256 _id, uint256 _amount) public view returns (uint256 price, uint256 fee) {
    // If id does not exist, this will return address(0), causing a revert in the next line
    address bondingCurve = shareData[_id].bondingCurve;
    (price, fee) = IBondingCurve(bondingCurve).getPriceAndFee(shareData[_id].tokenCount + 1, _amount);
}

function getSellPrice(uint256 _id, uint256 _amount) public view returns (uint256 price, uint256 fee) {
    // If id does not exist, this will return address(0), causing a revert in the next line
    address bondingCurve = shareData[_id].bondingCurve;
    (price, fee) = IBondingCurve(bondingCurve).getPriceAndFee(shareData[_id].tokenCount - _amount + 1, _amount);
}
```

**Root Cause**: Both `getBuyPrice` and `getSellPrice` use `IBondingCurve(bondingCurve).getPriceAndFee` with the current `tokenCount` as the start index. The price at execution time can differ from submission time because other buy/sell transactions can change `tokenCount`. No slippage parameter exists on `buy`, `sell`, `burnNFT`, or `mintNFT` functions.

**Attack Steps (Buy Sandwich)**:
1. User expects to buy shares for 5 USD
2. Attacker front-runs and buys shares that cost 5 USD
3. User's buy tx executes — shares now cost 10 USD due to increased supply
4. Attacker back-runs with sell — shares now worth 10 USD, earns 5 USD profit

**Attack Steps (Sell Sandwich)**:
1. User expects to sell shares for 20 USD
2. Attacker sells own share (receives 20 USD), reducing supply
3. User sells their share cheaper (receives 15 USD)
4. Attacker buys share back cheaper (for 10 USD), earns 10 USD profit

**Impact**: User can lose funds. Sell sandwiching doesn't need user approval since it only sends tokens to the victim.

**Fix**: Make user provide slippage to `buy`, `sell`, `burnNFT` and `mintNFT` functions. **Confirmed** by OpenCoreCH (Canto) — params introduced.

---

#### **Pattern 2: Missing Slippage on FRouter Buy/Sell** [MEDIUM]
**Protocol**: Virtuals Protocol | **Auditor**: Code4rena | **Severity**: Medium | **Finders**: Ejineroz, 0x60scs, ThanatOS +36 others

```solidity
// ❌ VULNERABLE: sell and buy functions in FRouter lack any slippage check
// https://github.com/code-423n4/2025-04-virtuals-protocol/blob/28e93273daec5a9c73c438e216dde04c084be452/contracts/fun/FRouter.sol#L95-L163
// No minAmountOut parameter — amountOut is calculated and applied without validation
```

**Root Cause**: The `sell` and `buy` functions in the `FRouter` contract lack a slippage check to ensure that the `amountOut` is not less than a user-specified minimum. Slippage occurs when the price changes between submission and execution due to low liquidity or high volatility.

**Impact**:
1. **User Losses**: Users may receive significantly fewer tokens than expected
2. **Front-Running Attacks**: Malicious actors can exploit the lack of slippage check by front-running transactions
3. **Economic Exploits**: Arbitrageurs or bots could extract value at the expense of users

**Secure Fix**:
```solidity
// ✅ SECURE: Add minAmountOut parameter for slippage protection
function sell(
    uint256 amountIn,
    address tokenAddress,
    address to,
    uint256 minAmountOut // Add a parameter for slippage protection
) public nonReentrant onlyRole(EXECUTOR_ROLE) returns (uint256, uint256) {
    require(tokenAddress != address(0), "Zero addresses are not allowed.");
    require(to != address(0), "Zero addresses are not allowed.");

    address pairAddress = factory.getPair(tokenAddress, assetToken);

    IFPair pair = IFPair(pairAddress);

    IERC20 token = IERC20(tokenAddress);

    uint256 amountOut = getAmountsOut(tokenAddress, address(0), amountIn);

    // Ensure the amountOut is greater than or equal to minAmountOut
    require(amountOut >= minAmountOut, "Slippage exceeded");

    token.safeTransferFrom(to, pairAddress, amountIn);

    uint fee = factory.sellTax();
    uint256 txFee = (fee * amountOut) / 100;

    uint256 amount = amountOut - txFee;
    address feeTo = factory.taxVault();

    pair.transferAsset(to, amount);
    pair.transferAsset(feeTo, txFee);

    pair.swap(amountIn, 0, 0, amountOut);

    if (feeTo == taxManager) {
        IBondingTax(taxManager).swapForAsset();
    }

    return (amountIn, amountOut);
}
```

---

#### **Pattern 3: Missing Slippage on Credit Token Sells** [MEDIUM]
**Protocol**: Noodles | **Auditor**: Pashov Audit Group | **Severity**: Medium

**Root Cause**: `VisibilityCredits.sol` uses a bonding curve where the price of credit tokens increases/decreases as total supply changes. `sellCredits()` has no `minAmountOut` parameter.

**Attack Steps**:
1. Alice submits `sellCredits()` transaction
2. Transaction remains in mempool
3. During this period, another `sellCredits()` transaction executes (unintentionally by other users or intentionally by bots), decreasing the trading cost
4. Alice's transaction goes through but receives lesser native tokens than intended

**Fix**: Provide users with the option to pass in a `minAmountOut` parameter on sells. Check the trading cost against this parameter.

---

#### **Pattern 4: Zero Slippage in Internal UniswapV2 Calls** [MEDIUM]
**Protocol**: Qoda DAO | **Auditor**: Halborn | **Severity**: Medium

```solidity
// ❌ VULNERABLE: 0 amountOutMin — accepts any amount of counterpart token
// src/QodaToken.sol Lines 342-358
function swapTokensForCounterpart(uint256 tokenAmount) private {
    // generate the uniswap pair path of token -> counterpart token address
    address[] memory path = new address[](2);
    path[0] = address(this);
    path[1] = tokenAddress;

    _approve(address(this), address(uniswapV2Router), tokenAmount);

    // make the swap
    uniswapV2Router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        tokenAmount,
        0, // accept any amount of counterpart token  ← ZERO SLIPPAGE
        path,
        address(this),
        block.timestamp
    );
}
```

```solidity
// ❌ VULNERABLE: 0 slippage on addLiquidity
// src/QodaToken.sol Lines 360-376
function addLiquidity(uint256 tokenAmount, uint256 counterpartAmount) private {
    // approve token transfer to cover all possible scenarios
    _approve(address(this), address(uniswapV2Router), tokenAmount);
    IERC20(tokenAddress).forceApprove(address(uniswapV2Router), counterpartAmount);

    // add the liquidity
    uniswapV2Router.addLiquidity(
        address(this),
        tokenAddress,
        tokenAmount,
        counterpartAmount,
        0, // slippage is unavoidable  ← ZERO SLIPPAGE
        0, // slippage is unavoidable  ← ZERO SLIPPAGE
        owner(),
        block.timestamp
    );
}
```

**Foundry Test Confirming Revert**:
```solidity
function test_calls_to_UniswapV2_without_slippage_protection() public {
    vm.startPrank(seraph);
    qoda_token.transfer(address(qoda_token), 1_000 ether);
    qoda_token.addLiquidity(100 ether, 1);
    qoda_token.swapTokensForCounterpart(100 ether);
    vm.stopPrank();
}
```

**Stack Trace** (verbatim):
```
├─ [20376] UniswapV2Router::swapExactTokensForTokensSupportingFeeOnTransferTokens(1e20, 0, [...], ...)
│   ├─ [3658] UniswapV2Pair::swap(0, 0, ...)
│   │   └─ ← [Revert] revert: UniswapV2: INSUFFICIENT_OUTPUT_AMOUNT
│   └─ ← [Revert] revert: UniswapV2: INSUFFICIENT_OUTPUT_AMOUNT
└─ ← [Revert] revert: UniswapV2: INSUFFICIENT_OUTPUT_AMOUNT
```

**Impact**: Financial loss, arbitrage exploitation, transaction failure, loss of trust.

**Fix**: Enforce minimum amount out or create `uint` parameter for off-chain calculations. **SOLVED** in commit `144cab46e7b09ac62604dd83996db4e6a2c5f083`.

---

#### **Pattern 5: Sandwich on UniswapV3 Liquidity Lock Position Conversion** [HIGH]
**Protocol**: UNCX UniswapV3 Liquidity Locker | **Auditor**: OpenZeppelin | **Severity**: High

**Root Cause**: When a non-full-range UniswapV3 position is locked, it is removed and redeposited as full-range in `_convertPositionToFullRange`. The liquidity distribution change can be sandwiched.

**Attack Steps**:
1. Attacker manipulates pool tick outside victim's tick range (`tickLower` to `tickUpper`)
2. When liquidity is removed, position is entirely one token (amount 0 for the other)
3. Contract would attempt to mint 0 liquidity and revert — **BUT** attacker transfers a small amount of the missing token directly to the contract
4. The cost of transfer is negligible since AMM is already at extreme tick
5. Victim's liquidity deposited at manipulated range
6. Attacker sells back into the new liquidity distribution for profit

**Fix**: Add slippage parameters to the `lock` function — either input parameters or hardcoded to require the pool's price tick to be within the locker's position's tick range.

**Status**: Resolved in [PR#1](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/pull/1) at commit `56a8037`.

---

#### **Pattern 6: No Slippage on Bonding Curve Market Seat Operations** [MEDIUM]
**Protocol**: Deriverse Dex | **Auditor**: Cyfrin | **Severity**: Medium | **Finders**: RajKumar, Ctrus, Alexzoid, JesJupyter

```rust
// ❌ VULNERABLE: No slippage protection — price depends on perp_clients_count at execution time
// In buy_market_seat():
let seat_price = PerpEngine::get_place_buy_price(
    instrument.perp_clients_count,
    instrument.crncy_token_decs_count,
)?;

instrument.seats_reserve += seat_price;
let price = data.amount + seat_price;
// ... price is deducted without validation
client_state.sub_crncy_tokens(price)?;
```

```rust
// In sell_market_seat():
let seat_price = PerpEngine::get_place_sell_price(
    instrument.perp_clients_count,
    instrument.crncy_token_decs_count,
)?;

client_state.add_crncy_tokens(seat_price)?;
```

```rust
// Bonding curve price functions:
pub fn get_place_buy_price(supply: u32, dec_factor: u32) -> Result<i64, DeriverseError> {
    let df = get_dec_factor(dec_factor);
    Ok(get_reserve(supply + 1, df)? - get_reserve(supply, df)?)
}

pub fn get_place_sell_price(supply: u32, dec_factor: u32) -> Result<i64, DeriverseError> {
    let df = get_dec_factor(dec_factor);
    Ok(get_reserve(supply, df)? - get_reserve(supply - 1, df)?)
}
```

**Root Cause**: Price calculated dynamically based on `perp_clients_count` at execution time. Between submission and execution, concurrent seat purchases/sales change the count. Users cannot specify max/min acceptable prices.

**Impact**: Unpredictable execution, poor user experience during high activity.

**Fix**: Add slippage protection with max/min acceptable prices in instruction data. **Fixed** in commit `a8181f3`.

---

#### **Pattern 7: Slippage Not Enforced During Token Graduation** [MEDIUM]
**Protocol**: GTE | **Auditor**: Code4rena | **Severity**: Medium | **Finders**: Legend, NexusAudits, hgrano +17 others

```solidity
// ❌ VULNERABLE: Slippage check only covers bonding curve portion, not graduation
// launchpad/Launchpad.sol#L287
function buy(BuyData calldata buyData)
    external
    nonReentrant
    onlyBondingActive(buyData.token)
    onlySenderOrOperator(buyData.account, SpotOperatorRoles.LAUNCHPAD_FILL)
    returns (uint256 amountOutBaseActual, uint256 amountInQuote)
{
    IUniswapV2Pair pair = _assertValidRecipient(buyData.recipient, buyData.token);
    LaunchData memory data = _launches[buyData.token];

    (amountOutBaseActual, data.active) = _checkGraduation(buyData.token, data, buyData.amountOutBase);

    amountInQuote = data.curve.buy(buyData.token, amountOutBaseActual);

    if (data.active && amountInQuote == 0) revert DustAttackInvalid();
    if (amountInQuote > buyData.maxAmountInQuote) revert SlippageToleranceExceeded(); // ← only checks bonding curve cost

    buyData.token.safeTransfer(buyData.recipient, amountOutBaseActual);
    address(data.quote).safeTransferFrom(buyData.account, address(this), amountInQuote);

    _emitSwapEvent({
        account: buyData.account,
        token: buyData.token,
        baseAmount: amountOutBaseActual,
        quoteAmount: amountInQuote,
        isBuy: true,
        curve: data.curve
    });

    // If graduated, handle AMM setup and remaining swap
    if (!data.active) {
        (amountOutBaseActual, amountInQuote) = _graduate(buyData, pair, data, amountOutBaseActual, amountInQuote);
    }
}
```

**Root Cause**: When a purchase exhausts the bonding curve's supply and triggers graduation to AMM, slippage checks only validate `amountInQuote` against bonding curve cost — not the total intended purchase. User may receive a fraction of desired tokens at an exorbitant effective price.

**Fix**: Calculate and check price per token the user is willing to pay vs. price per token actually bought.

---

#### **Pattern 8: Liquidity Amount Calculated from Manipulable On-Chain Price** [HIGH]
**Protocol**: Olas (Lockbox V2) | **Auditor**: Cantina | **Severity**: High | **Finder**: 99Crits

```rust
// ❌ VULNERABLE: liquidity_amount derived from current on-chain price — sandwichable
pub fn deposit(ctx: Context<DepositPositionForLiquidity>,
    token_max_a: u64,
    token_max_b: u64,
) -> Result<()> {
```

```rust
// token_max_a used to calculate liquidity at CURRENT manipulable price:
let sqrt_price_current_x64 = ctx.accounts.whirlpool.sqrt_price;
let sqrt_price_upper_x64 = sqrt_price_from_tick_index(ctx.accounts.position.tick_upper_index);
let liquidity_amount = get_liquidity_from_token_a(token_max_a as u128, sqrt_price_current_x64,
    sqrt_price_upper_x64)?;
```

```rust
// liquidity_amount used for increase_liquidity:
let (delta_a, delta_b) = calculate_liquidity_token_deltas(
    tick_index_current,
    sqrt_price_current_x64,
    &ctx.accounts.position,
    liquidity_amount as i128
)?;

whirlpool::cpi::increase_liquidity(cpi_ctx_modify_liquidity, liquidity_amount, delta_a, delta_b)?;
```

```rust
// The math in get_liquidity_from_token_a:
fn get_liquidity_from_token_a(amount: u128, sqrt_price_lower_x64: u128, sqrt_price_upper_x64: u128) {
    // liquidity = a * ((sqrt_price_lower * sqrt_price_upper) / (sqrt_price_upper - sqrt_price_lower))
    // Lower sqrt_price_lower → lower numerator, higher denominator → LESS liquidity
}
```

**Root Cause**: Liquidity requested is based on `token_max_a` at current on-chain price. Attacker can manipulate the pool price via Jito Bundles to reduce the liquidity the depositor receives.

**Attack Steps**:
1. Attacker buys up a lot of token B (lowering price/sqrt_price)
2. User transaction executes — deposits `token_max_a` and little token B, gets **much less liquidity** than intended
3. Attacker sells token B back and profits from higher liquidity in pool

**Recommended Fix**: Deposit instruction should take an additional `liquidity_amount` parameter (like Orca's `increase_liquidity`):
1. User selects deposit amounts and slippage percentage
2. Frontend calculates expected `liquidity_amount` at current non-manipulated prices
3. Frontend passes calculated `liquidity_amount`, `max_token_a`, `max_token_b` to deposit tx
4. Lockbox forwards these parameters to Orca whirlpool program

---

#### **Pattern 9: No Slippage or Deadline During Stability Burns** [MEDIUM]
**Protocol**: Unitas Protocol | **Auditor**: Sherlock | **Severity**: Medium | **Finders**: Juntao, 0xGoodess, PawelK +9 others

```solidity
// ❌ VULNERABLE: Swap function at Unitas.sol#L208 has no slippage or deadline params
// Stability burns reduce totalSupply of usd1 unilaterally
// Users swapping during a burn get affected by slippage
// Without deadline, tx may sit in mempool and execute after a stability burn
```

**Root Cause**: Unitas can mint/burn tokens unilaterally for stability. When stability burn occurs (reserve ratio <130%), `usd1` `totalSupply` is reduced one-sided. Any user swapping during this period gets affected by slippage. Without a deadline param, the transaction may sit in the mempool and execute at a much later time, potentially after a stability burn.

**Impact**: User affected by unintended slippage. A swap with 10000 USDEMC could result in 100 LESS USD1 due to 10% slippage caused by depreciation.

**Fix**: Allow user to specify `deadline` and `minOutAmount` parameters. Check both at start and end of swap execution.

---

#### **Pattern 10: Slippage Check Before Graduation Supply Cap** [MEDIUM]
**Protocol**: Stardusts | **Auditor**: Pashov Audit Group | **Severity**: Medium

```javascript
// ❌ VULNERABLE: minOrderSize check happens BEFORE trueOrderSize is reassigned
function _validateBondingCurveBuy(uint256 minOrderSize)
        internal
        returns (uint256 totalCost, uint256 trueOrderSize, uint256 fee, uint256 refund, bool shouldGraduate)
    {
        // Set the total cost to the amount of ETH sent
        totalCost = msg.value;

        // Calculate the fee
        fee = (totalCost * feeBps) / 10000;

        // Calculate the amount of ETH remaining for the order
        uint256 remainingEth = totalCost - fee;

        // Get quote for the number of tokens that can be bought with the amount of ETH remaining
        trueOrderSize = getOutTokenAmount(remainingEth);

        // Ensure the order size is greater than the minimum order size
        if (trueOrderSize < minOrderSize) revert SlippageTooHigh(); // ← CHECK IS HERE

        // Calculate the maximum number of tokens that can be bought on the bonding curve
        uint256 maxRemainingTokens = (X0 - X1) - totalSupply();

        // Start the market if the order size equals the number of remaining tokens
        if (trueOrderSize == maxRemainingTokens) {
            shouldGraduate = true;
        }

        // If the order size is greater than the maximum number of remaining tokens:
        if (trueOrderSize > maxRemainingTokens) {
            // Reset the order size to the number of remaining tokens
            trueOrderSize = maxRemainingTokens; // ← REASSIGNED HERE — no re-check!

            // Calculate the amount of ETH needed to buy the true order
            uint256 ethNeeded = Y1 - virtualEthLiquidity;

            // Recalculate the fee with the updated order size
            fee = (ethNeeded * feeBps) / 10000;

            // Recalculate the total cost with the updated order size and fee
            totalCost = ethNeeded + fee;

            // Refund any excess ETH
            if (msg.value > totalCost) {
                refund = msg.value - totalCost;
            }

            shouldGraduate = true;
        }
    }
```

**Root Cause**: When `trueOrderSize > maxRemainingTokens`, `trueOrderSize` is reassigned to `maxRemainingTokens` but the `minOrderSize` check has already passed. If a user is front-run reducing `maxRemainingTokens`, they receive fewer tokens than their `minOrderSize` with no revert.

**Fix**: Move `if (trueOrderSize < minOrderSize) revert SlippageTooHigh();` to the **end** of the function, after all reassignments.

---

### Impact Analysis

#### Technical Impact
- Users receive fewer tokens/assets than expected on bonding curve trades
- Sandwich attacks extract value from every unprotected buy/sell operation
- Graduation-triggered trades bypass slippage checks entirely
- Liquidity deposits receive less LP tokens than intended
- Stability mechanism interactions cause unprotected slippage

#### Business Impact
- Systematic MEV extraction from all bonding curve participants
- Loss of user trust when trades consistently execute at worse-than-expected prices
- Front-running bots capture all consumer surplus
- Protocol reputation damage from repeated user losses

#### Affected Scenarios
- Any bonding curve buy/sell without `minAmountOut`/`maxAmountIn`
- Internal UniswapV2/V3 calls with hardcoded zero slippage
- Liquidity provision/locking operations without price range validation
- Token graduation transitions where slippage only covers the bonding curve phase
- Operations during protocol state changes (stability burns, weight changes)

### Secure Implementation

**Fix 1: User-Provided Slippage on Buy/Sell**
```solidity
// ✅ SECURE: User specifies maximum acceptable cost
function buy(uint256 _id, uint256 _amount, uint256 _maxCost) external payable {
    (uint256 price, uint256 fee) = getBuyPrice(_id, _amount);
    uint256 totalCost = price + fee;
    require(totalCost <= _maxCost, "Slippage exceeded");
    // ... execute buy ...
}

function sell(uint256 _id, uint256 _amount, uint256 _minProceeds) external {
    (uint256 price, uint256 fee) = getSellPrice(_id, _amount);
    uint256 proceeds = price - fee;
    require(proceeds >= _minProceeds, "Slippage exceeded");
    // ... execute sell ...
}
```

**Fix 2: Non-Zero Slippage on UniswapV2 Calls**
```solidity
// ✅ SECURE: Calculate minimum from oracle/off-chain and pass as parameter
function swapTokensForCounterpart(uint256 tokenAmount, uint256 minAmountOut) private {
    address[] memory path = new address[](2);
    path[0] = address(this);
    path[1] = tokenAddress;
    _approve(address(this), address(uniswapV2Router), tokenAmount);
    uniswapV2Router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        tokenAmount,
        minAmountOut, // NOT zero — calculated off-chain
        path,
        address(this),
        block.timestamp
    );
}
```

**Fix 3: Slippage Check After All Reassignments**
```solidity
// ✅ SECURE: Check minOrderSize AFTER graduation cap is applied
function _validateBondingCurveBuy(uint256 minOrderSize) internal returns (...) {
    trueOrderSize = getOutTokenAmount(remainingEth);
    uint256 maxRemainingTokens = (X0 - X1) - totalSupply();

    if (trueOrderSize > maxRemainingTokens) {
        trueOrderSize = maxRemainingTokens;
        // ... recalculate costs ...
        shouldGraduate = true;
    }

    // Check AFTER all reassignments
    if (trueOrderSize < minOrderSize) revert SlippageTooHigh();
}
```

**Fix 4: Liquidity Amount as Input Parameter (Solana/Orca)**
```rust
// ✅ SECURE: Frontend calculates expected liquidity at non-manipulated price
pub fn deposit(ctx: Context<DepositPositionForLiquidity>,
    liquidity_amount: u64,  // calculated off-chain
    token_max_a: u64,
    token_max_b: u64,
) -> Result<()> {
    // Forward all three to whirlpool's increase_liquidity
    whirlpool::cpi::increase_liquidity(cpi_ctx, liquidity_amount, token_max_a, token_max_b)?;
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern: Bonding curve buy/sell functions with no minAmountOut/maxAmountIn parameter
- Pattern: UniswapV2Router calls with 0 as amountOutMin or amountBMin
- Pattern: addLiquidity calls with (0, 0) as minimum amounts
- Pattern: Slippage check (revert) before conditional value reassignment
- Pattern: Graduation/migration path that bypasses slippage check
- Pattern: liquidity_amount computed from current on-chain sqrt_price
- Pattern: Swap function with no deadline parameter
- Pattern: sellCredits/sellShares with no minimum receive amount
- Pattern: block.timestamp used as deadline (provides no protection)
```

#### Audit Checklist
- [ ] Does every bonding curve buy/sell function accept a user-provided slippage parameter?
- [ ] Are all internal UniswapV2/V3 swap calls using non-zero minAmountOut?
- [ ] Is the slippage check applied AFTER all conditional value reassignments?
- [ ] Does the graduation code path preserve slippage validation?
- [ ] Do liquidity operations use off-chain computed expected amounts?
- [ ] Is there a deadline parameter on swap/trade functions?
- [ ] Are LP deposit operations protected against price manipulation before locking?

### Real-World Examples

| Protocol | Year | Severity | Auditor | Key Issue |
|----------|------|----------|---------|-----------|
| Canto (1155tech) | 2023 | Medium | Code4rena | No slippage on Market buy/sell |
| Virtuals Protocol | 2025 | Medium | Code4rena | No slippage on FRouter buy/sell |
| Noodles | 2025 | Medium | Pashov | No minAmountOut on sellCredits |
| Qoda DAO | 2024 | Medium | Halborn | Zero slippage in UniswapV2 Router calls |
| UNCX UniV3 Locker | 2023 | High | OpenZeppelin | Sandwich on liquidity lock conversion |
| Deriverse Dex | 2025 | Medium | Cyfrin | No slippage on market seat bonding curve |
| GTE Launchpad | 2025 | Medium | Code4rena | Slippage not enforced during graduation |
| Olas Lockbox V2 | 2024 | High | Cantina | Liquidity from manipulable on-chain price |
| Unitas Protocol | 2023 | Medium | Sherlock | No slippage/deadline during stability burn |
| Stardusts | 2024 | Medium | Pashov | minOrderSize check before graduation cap |

### Keywords for Search

`slippage protection`, `minAmountOut`, `maxAmountIn`, `amountOutMin`, `bonding curve`, `sandwich attack`, `front-running`, `price manipulation`, `token supply`, `graduation slippage`, `liquidity locking`, `UniswapV2Router`, `addLiquidity`, `swapExactTokensForTokens`, `sellCredits`, `buyShareCred`, `market seat`, `perp_clients_count`, `graduation`, `minOrderSize`, `deadline`, `stability burn`, `sqrt_price`, `liquidity_amount`, `SHARE_LOCK_PERIOD`, `SlippageTooHigh`, `block.timestamp`

### Related Vulnerabilities

- Sandwich attacks and MEV on swap functions (see SANDWICH_ATTACK_MEV_BONDING_CURVE_VULNERABILITIES.md)
- Flash loan amplified price manipulation
- Oracle manipulation / stale price vulnerabilities
- Token graduation DoS attacks
- Bonding curve parameter misconfiguration
