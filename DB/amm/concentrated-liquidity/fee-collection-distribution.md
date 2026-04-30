---
title: "Fee Collection and Distribution Vulnerabilities in AMMs"
protocol: generic
vulnerability_class: amm-fee-vulnerabilities
category: amm/concentrated-liquidity
vulnerability_type: fee_collection_distribution
attack_type: fee_theft|accounting_manipulation|denial_of_service
affected_component: fee_accounting|fee_collection|fee_distribution
severity: high
impact: fund_loss|fee_theft|denial_of_service
severity_range: "MEDIUM to HIGH"
consensus_severity: HIGH

affected_protocols:
  - "Uniswap V3/V4 and forks"
  - "Ammplify"
  - "Goat Trading"
  - "OpenZeppelin Uniswap Hooks"
  - "Good Entry"
  - "Superposition"
  - "Vultisig"
  - "Particle Protocol"
  - "GFX Labs"
  - "Gainsnetwork"
  - "Serum v4"

pattern_frequency:
  total_reports_analyzed: 74
  patterns_identified: 12
  critical_patterns: 6

root_causes:
  - "Fee accounting manipulation via spot price or liquidity"
  - "Missing fee tracking state updates on transfers"
  - "Fee growth underflow not handled with unchecked{}"
  - "Fees not segregated from user principal"
  - "Permissionless fee withdrawal on behalf of others"
  - "JIT liquidity capturing unearned fees"
  - "Parameter ordering errors in fee collection"
  - "Flash loan attacks on uncollected fees"

audit_sources:
  - "Code4rena"
  - "Sherlock"
  - "Cyfrin"
  - "Cantina"
  - "OpenZeppelin"
  - "Pashov Audit Group"
  - "OtterSec"

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | unknown | unknown

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _distributeFilledOrderFees
  - addMakerLiquidity
  - balanceOf
  - borrow
  - claim
  - claimFees
  - collectFees
  - deposit
  - executeIncreasePositionSizeMarket
  - getEquivalentLiquidity
  - getOwedFee
  - manipulation
  - msg.sender
  - receive
  - swap
  - withdraw
  - withdrawFees
  - withdrawNative
---

## Overview

Fee collection and distribution mechanisms in AMMs are critical revenue sources for liquidity providers but present complex attack surfaces. This vulnerability class covers issues in **fee calculation**, **fee collection**, **fee distribution**, and **fee tracking** that can lead to fee theft, unfair distribution, or loss of earned fees.

**Root Cause Statement:**
> These vulnerabilities exist because AMM fee mechanisms rely on precise accounting, proper segregation between principal and fees, temporal ordering assumptions, and underflow-dependent arithmetic that developers frequently misimplement, allowing attackers to steal fees, manipulate fee distribution, or cause DoS.

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | unknown | unknown`
- Interaction scope: `single_contract`
- Primary affected component(s): `unknown`
- High-signal code keywords: `_distributeFilledOrderFees`, `addMakerLiquidity`, `balanceOf`, `borrow`, `claim`, `claimFees`, `collectFees`, `deposit`
- Typical sink / impact: `fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: State variable updated after external interaction instead of before (CEI violation)
- Signal 2: Withdrawal path produces different accounting than deposit path for same principal
- Signal 3: Reward accrual continues during paused/emergency state
- Signal 4: Edge case in state machine transition allows invalid state

#### False Positive Guards

- Not this bug when: Standard security patterns (access control, reentrancy guards, input validation) are in place
- Safe if: Protocol behavior matches documented specification
- Requires attacker control of: specific conditions per pattern

#### Code Patterns to Look For

```solidity
collectFees(tokenId); // callable for another user's position without recipient/accounting checks
feesOwed = feeGrowthInside - lastFeeGrowthInside; // underflow expected but not handled intentionally
withdraw(amount); // principal and uncollected fees share the same balance bucket
addMakerLiquidity(); swap(); removeLiquidity(); // JIT liquidity earns fees for no inventory risk
claimFees(pool, token0, token1); // parameter order or fee tier not authenticated
```

#### False Positive Detail

- Permissionless fee collection is acceptable only when fees are credited to the rightful owner or an authenticated recipient, not `msg.sender`.
- Fee-growth underflow is normal in Uniswap-style math only if the implementation deliberately mirrors the modulo arithmetic; checked arithmetic that reverts can create DoS.
- JIT-liquidity findings need an economic path where the attacker captures fees or rewards without bearing the intended exposure, not merely a profitable LP strategy.

## Vulnerable Pattern Examples

### Pattern 1: Fee Theft via Spot Price Manipulation

**Severity:** HIGH | **Sources:** Ammplify (Sherlock)

Attackers manipulate spot price to reduce equivalent liquidity calculations, deposit at reduced share price, then withdraw at correct price to steal accumulated fees.

```solidity
// H-1: Fees stolen by manipulating uniswap pool spot price
function addMakerLiquidity(...) {
    // Equivalent liquidity depends on spot price
    uint128 equivLiq = PoolLib.getEquivalentLiq(
        lowTick, highTick,
        node.fees.xCFees, node.fees.yCFees,
        data.sqrtPriceX96,  // BUG: Manipulatable spot price!
        true
    );
    
    // Share price calculated from manipulated value
    compoundingLiq = node.liq.mLiq - node.liq.ncLiq + equivLiq;
    targetSliq = uint128(FullMath.mulDiv(node.liq.shares, targetLiq, compoundingLiq));
}
```

**Attack Path:**
1. Manipulate spot price to reduce equivalent liquidity
2. Deposit maker liquidity at reduced share price
3. Restore spot price
4. Withdraw liquidity at correct share price
5. Profit = stolen fees

**Reference:** [h-1-accrued-maker-fees-not-yet-compounded-can-be-stolen-by-manipulating-uniswap-.md](../../reports/constant_liquidity_amm/h-1-accrued-maker-fees-not-yet-compounded-can-be-stolen-by-manipulating-uniswap-.md)

---

### Pattern 2: Permissionless Fee Withdrawal

**Severity:** HIGH | **Sources:** Goat Trading (Sherlock)

Permissionless `withdrawFees()` combined with missing tracking updates on transfers enables stealing all LP fees.

```solidity
// H-1: LP fees can be stolen from any pair
// Transfer to pair doesn't update fee tracking
if (to != address(this)) {
    _updateFeeRewards(to);  // BUG: Skipped for pair address
}

// Permissionless fee withdrawal on behalf of ANY address
function withdrawFees(address onBehalf) external {  // BUG: No access control
    // feesPerTokenPaid[address(pair)] = 0 because never updated
    // Attacker can claim fees for the pair itself
}
```

**Attack Path:**
1. Add liquidity to pair (receive LP tokens)
2. Transfer LP tokens directly to pair address (bypasses fee tracking update)
3. Call `withdrawFees(address(pair))` - claims all pending fees
4. Burn LP tokens to recover deposited funds

**Reference:** [h-1-liquidity-provider-fees-can-be-stolen-from-any-pair.md](../../reports/constant_liquidity_amm/h-1-liquidity-provider-fees-can-be-stolen-from-any-pair.md)

---

### Pattern 3: JIT Fee Theft on Limit Orders

**Severity:** HIGH | **Sources:** OpenZeppelin Uniswap Hooks

Just-in-time liquidity additions capture fees accrued before their participation.

```solidity
// Limit order fees split by liquidity share at fill time
// BUG: No consideration of when liquidity was added
function _distributeFilledOrderFees(...) {
    // User who added liquidity 1 block ago gets same share
    // as user who provided liquidity for months
    userShare = totalFees * userLiquidity / totalLiquidity;
}
```

**Attack Path:**
1. Monitor limit order pool with significant unclaimed fees
2. Create large limit order (90% of liquidity)
3. Swap to fill the order
4. Withdraw - capture 90% of ALL fees (including pre-existing)

**Reference:** [accrued-limit-order-fees-can-be-stolen.md](../../reports/constant_liquidity_amm/accrued-limit-order-fees-can-be-stolen.md)

---

### Pattern 4: Fee Flash Loan Attack

**Severity:** HIGH | **Sources:** Good Entry (Code4rena)

Uncollected fees can be stolen via flash loan when fee value calculation is flawed.

```solidity
// H-04: Flash loan attack on uncollected fees
function deposit(uint256 n0, uint256 n1) external {
    // Fee reinvestment check based on amounts, not value
    if (fee0 > token0Amount * 0.01 || fee1 > token1Amount * 0.01) {
        reinvestFees();  // BUG: Price changes can make this bypass
    }
    
    // Attacker bypasses fee downscaling with tiny second token
    if (n0 > 0 && n1 > 0) {
        // No fee adjustment!  // BUG: Attacker adds 1 wei of token1
    }
}
```

**Attack Path:**
1. Wait for price to move significantly (fees > 1% in value)
2. Flash loan large amount
3. Deposit with 1 wei of second token (bypass fee adjustment)
4. Withdraw immediately - claim proportional share of fees
5. Repay flash loan

**Reference:** [h-04-tokenisableranges-incorrect-accounting-of-non-reinvested-fees-in-deposit-ex.md](../../reports/constant_liquidity_amm/h-04-tokenisableranges-incorrect-accounting-of-non-reinvested-fees-in-deposit-ex.md)

---

### Pattern 5: Parameter Ordering in Fee Collection

**Severity:** HIGH | **Sources:** Superposition (Code4rena)

Simple parameter ordering mistakes in fee transfer functions cause complete DoS.

```rust
// H-05: Parameter misordering causes DoS
fn collect_protocol_fees(pool: Address, recipient: Address, ...) {
    // BUG: recipient and pool swapped!
    erc20::transfer_to_addr(recipient, pool, token_0)?;  // Wrong order!
    erc20::transfer_to_addr(recipient, FUSDC_ADDR, token_1)?;
    
    // Correct: transfer_to_addr(token_address, recipient, amount)
}
```

**Impact:** Complete failure of protocol fee collection, funds locked permanently.

**Reference:** [h-05-parameter-misordering-in-fee-collection-function-causes-denial-of-service-a.md](../../reports/constant_liquidity_amm/h-05-parameter-misordering-in-fee-collection-function-causes-denial-of-service-a.md)

---

### Pattern 6: Collect All Fees on First Claim

**Severity:** HIGH | **Sources:** Vultisig (Code4rena)

First user to claim collects ALL pool fees, leaving nothing for others.

```solidity
// H-01: First claimer takes all fees
function claim(uint256 tokenId) external {
    // BUG: Collects ALL owed tokens from pool
    pool.collect(
        address(this), TICK_LOWER, TICK_UPPER,
        type(uint128).max,  // All token0
        type(uint128).max   // All token1
    );
    
    // User gets their share
    tokenOut.safeTransfer(user, owed);
    
    // "Extra" fees go to fee taker (but it's other users' fees!)
    TransferHelper.safeTransfer(token0, feeTaker, amountCollected0 - amount0);
}
```

**Impact:** Subsequent claimers find no fees remaining, transactions revert.

**Reference:** [h-01-most-users-wont-be-able-to-claim-their-share-of-uniswap-fees.md](../../reports/constant_liquidity_amm/h-01-most-users-wont-be-able-to-claim-their-share-of-uniswap-fees.md)

---

### Pattern 7: Fee Growth Underflow Returns Zero

**Severity:** HIGH | **Sources:** Particle Protocol (Cantina)

Missing `unchecked{}` in fee owed calculation returns zero instead of correct value.

```solidity
// BUG: Returns zero due to checked subtraction
function getOwedFee(...) internal pure returns (uint128, uint128) {
    // When feeGrowthInside wraps around (underflow), this check fails
    if (feeGrowthInside0X128 > feeGrowthInside0LastX128) {  // FALSE after wrap!
        token0Owed = calculate(...);
    }
    // Returns 0 when it shouldn't
}

// Correct: Use unchecked and check for inequality
function getOwedFee(...) internal pure returns (uint128, uint128) {
    unchecked {
        if (feeGrowthInside0X128 != feeGrowthInside0LastX128) {
            token0Owed = uint128(FullMath.mulDiv(
                feeGrowthInside0X128 - feeGrowthInside0LastX128, liquidity, Q128
            ));
        }
    }
}
```

**Reference:** [getowedfee-can-incorrectly-return-zero-because-of-fee-growth-underﬂow.md](../../reports/constant_liquidity_amm/getowedfee-can-incorrectly-return-zero-because-of-fee-growth-underﬂow.md)

---

### Pattern 8: Fee Tier Spoofing

**Severity:** MEDIUM | **Sources:** Serum v4 (OtterSec)

Incorrect account ownership validation allows obtaining fee discounts without holding required tokens.

```rust
// BUG: Checks user ownership instead of token program
if let Some(discount_account) = a.discount_token_account {
    check_account_owner(
        discount_account,
        a.user_owner.key,  // Wrong! Should be spl_token::ID
        DexError::InvalidStateAccountOwner,
    )?;
}
```

**Attack:** Create fake discount token account owned by user instead of SPL token program, get maximum fee tier discount.

**Reference:** [fee-tier-spoofing.md](../../reports/constant_liquidity_amm/fee-tier-spoofing.md)

---

### Pattern 9: Fees Not Segregated from Principal

**Severity:** HIGH | **Sources:** GFX Labs (Sherlock)

User principal (WETH) and collected fees (Native ETH) not separated, owner withdrawal takes user funds.

```solidity
// H-1: Fees and user assets mixed
function withdrawNative() external onlyOwner {
    // Withdraws BOTH fee (Native ETH) AND user principal (WETH)!
    uint256 wrappedNativeBalance = WRAPPED_NATIVE.balanceOf(address(this));
    uint256 nativeBalance = address(this).balance;
    
    if (wrappedNativeBalance > 0) WRAPPED_NATIVE.safeTransfer(owner, wrappedNativeBalance);
    if (nativeBalance > 0) owner.safeTransferETH(nativeBalance);
}
```

**Impact:** User's swapped WETH sent to owner, unrecoverable.

**Reference:** [h-1-lack-of-segregation-between-users-assets-and-collected-fees-resulting-in-los.md](../../reports/constant_liquidity_amm/h-1-lack-of-segregation-between-users-assets-and-collected-fees-resulting-in-los.md)

---

### Pattern 10: Double Fee Points Update

**Severity:** HIGH | **Sources:** Gainsnetwork (Pashov)

Fee tier points updated twice in same operation, giving users double rewards.

```solidity
// H-01: FeeTierPoints increased twice
function executeIncreasePositionSizeMarket(...) {
    // 5.2 Distribute opening fees - ALSO updates fee tier points
    TradingCommonUtils.processOpeningFees(existingTrade, values.positionSizeCollateralDelta);
    
    // 5.3 Store trader fee tier points - REDUNDANT UPDATE!
    TradingCommonUtils.updateFeeTierPoints(
        existingTrade.collateralIndex,
        existingTrade.user,
        values.positionSizeCollateralDelta  // Double counted!
    );
}
```

**Impact:** Users get fee discounts twice as fast, protocol loses fee revenue.

**Reference:** [h-01-feetierpoints-is-incorrectly-increased-twice.md](../../reports/constant_liquidity_amm/h-01-feetierpoints-is-incorrectly-increased-twice.md)

---

### Pattern 11: Subtree Borrow Not Propagated (Fee Underpayment)

**Severity:** HIGH | **Sources:** Ammplify (Sherlock)

Taker fees calculated on node's borrowed amount only, ignoring children's values.

```solidity
// H-10: subtreeBorrowedX not propagated from children
// Only node's own borrow is stored, not subtree total
node.liq.subtreeBorrowedX += xBorrow;  // Just this node

// But fee calculation assumes it's the full subtree
totalXBorrows += node.liq.subtreeBorrowedX;  // Missing children!
```

**Impact:** Takers pay up to 99% less fees, makers lose expected revenue.

**Reference:** [h-10-takers-can-pay-significantly-less-fees-with-makers-losing-these-amounts-due.md](../../reports/constant_liquidity_amm/h-10-takers-can-pay-significantly-less-fees-with-makers-losing-these-amounts-due.md)

---

## Secure Implementation Patterns

### Secure Pattern 1: TWAP-Based Fee Value Calculation

```solidity
function getEquivalentLiquidity(uint256 feeX, uint256 feeY) internal view returns (uint128) {
    // Use TWAP instead of spot price to prevent manipulation
    uint256 twapPrice = getTwapPrice(TWAP_DURATION);
    uint256 feeValue = feeX * twapPrice + feeY;
    
    // Calculate equivalent liquidity from fee value
    return SafeCast.toUint128(feeValue * Q128 / liquidityValue);
}
```

### Secure Pattern 2: Per-User Fee Tracking

```solidity
mapping(address => uint256) public feeGrowthLastClaimed;

function claimFees(uint256 tokenId) external {
    uint256 feeGrowthGlobal = getFeeGrowthGlobal();
    uint256 feeGrowthLast = feeGrowthLastClaimed[msg.sender];
    
    // Only claim fees accrued since last claim
    uint256 owedFees = (feeGrowthGlobal - feeGrowthLast) * userLiquidity / PRECISION;
    
    feeGrowthLastClaimed[msg.sender] = feeGrowthGlobal;
    token.safeTransfer(msg.sender, owedFees);
}
```

### Secure Pattern 3: Proportional Fee Collection

```solidity
function claim(uint256 tokenId) external returns (uint256 amount0, uint256 amount1) {
    Position storage position = positions[tokenId];
    
    // Calculate user's fee share based on their liquidity proportion
    (uint256 totalFees0, uint256 totalFees1) = calculateAccruedFees(position);
    
    // Collect ONLY user's portion, not all fees
    pool.collect(
        address(this), TICK_LOWER, TICK_UPPER,
        SafeCast.toUint128(totalFees0),  // Only user's share
        SafeCast.toUint128(totalFees1)
    );
    
    token0.safeTransfer(msg.sender, totalFees0);
    token1.safeTransfer(msg.sender, totalFees1);
}
```

### Secure Pattern 4: Segregated Fee Accounting

```solidity
uint256 public collectedFees;  // Track fees separately

function collectFees() external {
    uint256 fee = calculateFee();
    collectedFees += fee;
}

function withdrawFees() external onlyOwner {
    uint256 toWithdraw = collectedFees;
    collectedFees = 0;
    token.safeTransfer(owner, toWithdraw);  // Only withdraw tracked fees
}
```

---

## Impact Analysis

| Impact Category | Severity | Frequency | Description |
|----------------|----------|-----------|-------------|
| Fee Theft | HIGH | Common | Attackers steal accumulated LP fees |
| Fee DoS | HIGH | Moderate | Fee collection completely blocked |
| Unfair Distribution | MEDIUM-HIGH | Common | Some LPs get more than deserved |
| Revenue Loss | HIGH | Common | Protocol loses fee revenue |
| User Fund Loss | HIGH | Moderate | User principal mixed with fees |

---

## Detection Checklist

- [ ] Fee calculations use TWAP, not spot price
- [ ] Fee tracking updated on ALL token transfers (including to self)
- [ ] withdrawFees() has proper access control
- [ ] Fee collection proportional to user's share, not all at once
- [ ] Fee owed calculation uses `unchecked{}` for underflow
- [ ] Fees segregated from user principal in accounting
- [ ] JIT liquidity cannot capture pre-existing fees
- [ ] Parameter ordering verified in all fee transfer calls
- [ ] Double-update bugs checked in fee point systems

---

## Real-World Examples

| Protocol | Vulnerability | Severity | Audit Firm | Year |
|----------|--------------|----------|------------|------|
| Ammplify | Spot price fee manipulation | HIGH | Sherlock | 2025 |
| Goat Trading | Permissionless fee withdrawal | HIGH | Sherlock | 2024 |
| OpenZeppelin Hooks | JIT fee theft on limit orders | HIGH | OpenZeppelin | 2025 |
| Good Entry | Flash loan fee attack | HIGH | Code4rena | 2023 |
| Superposition | Parameter ordering DoS | HIGH | Code4rena | 2024 |
| Vultisig | First claimer takes all | HIGH | Code4rena | 2024 |
| Particle | Fee growth underflow zero | HIGH | Cantina | 2024 |
| Serum v4 | Fee tier spoofing | MEDIUM | OtterSec | 2022 |
| GFX Labs | Fee/principal not segregated | HIGH | Sherlock | 2023 |
| Gainsnetwork | Double fee points | HIGH | Pashov | 2024 |

---

## Related Vulnerabilities

- [Tick/Range/Position Vulnerabilities](./tick-range-position-vulnerabilities.md) - Fee growth calculations overlap
- [Slippage/Sandwich Attacks](./slippage-sandwich-frontrun.md) - Price manipulation affects fees

---

## Keywords

**Primary:** fee theft, fee manipulation, LP fees, protocol fees, fee collection, fee distribution, trading fees, swap fees

**Technical:** feeGrowthInside, feeGrowthOutside, tokensOwed, collect, accruedFees, pendingFees, claimFees

**Vulnerability:** JIT attack, flash loan, fee drain, fee DoS, fee underflow, permissionless withdrawal

**Protocols:** uniswap_v3, uniswap_v4, ammplify, goat_trading, particle, serum, good_entry

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`_distributeFilledOrderFees`, `addMakerLiquidity`, `amm/concentrated-liquidity`, `balanceOf`, `borrow`, `claim`, `claimFees`, `collectFees`, `deposit`, `executeIncreasePositionSizeMarket`, `getEquivalentLiquidity`, `getOwedFee`, `manipulation`, `msg.sender`, `receive`, `swap`, `withdraw`, `withdrawFees`, `withdrawNative`
