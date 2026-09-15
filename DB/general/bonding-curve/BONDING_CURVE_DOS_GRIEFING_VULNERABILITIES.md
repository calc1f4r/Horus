---
# Core Classification
protocol: generic
chain: everychain
category: denial_of_service
vulnerability_type: bonding_curve_dos_griefing

# Attack Vector Details
attack_type: griefing
affected_component: bonding_curve_creation, pool_migration, share_distribution, liquidity_provision

# Technical Primitives
primitives:
  - deterministic_address
  - PDA_pre_funding
  - escrow_invariant
  - gas_limit
  - share_inflation
  - zero_amount
  - uint8_overflow
  - init_if_needed
  - EnumerableMap
  - selfdestruct

# Impact Classification
severity: high
impact: dos
exploitability: 0.8
financial_impact: high

# Context Tags
tags:
  - dos
  - griefing
  - bonding_curve
  - escrow
  - pre_funding
  - gas_limit
  - share_inflation
  - first_depositor
  - PDA
  - solana
  - defi

# Version Info
language: solidity
version: ">=0.6.0"

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | bonding_curve_creation, pool_migration, share_distribution, liquidity_provision | bonding_curve_dos_griefing

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - EnumerableMap
  - PDA_pre_funding
  - _findSlice
  - approve
  - block.timestamp
  - buy
  - buyShareCredFor
  - deposit
  - deterministic_address
  - distribute
  - escrow_invariant
  - gas_limit
  - graduateToken
  - init_if_needed
  - legitimate
  - mint
  - permissioned
  - selfdestruct
  - share_inflation
  - swap
---

## References
- [Report-01]: reports/bonding_curve_findings/h-02-bonding-curve-dos-through-escrow-pre-funding.md
- [Report-02]: reports/bonding_curve_findings/h-01-direct-sol-transfers-to-bonding-curve-escrow-can-break-protocol-invariant.md
- [Report-03]: reports/bonding_curve_findings/denial-of-service-conditions-caused-by-the-use-of-more-than-256-slices.md
- [Report-04]: reports/bonding_curve_findings/dos-with-block-gas-limit.md
- [Report-05]: reports/bonding_curve_findings/h-01-the-lock_pool-operation-can-be-dos.md
- [Report-06]: reports/bonding_curve_findings/h-02-zero-amount-withdrawals-of-safeth-or-votium-will-brick-the-withdraw-process.md
- [Report-07]: reports/bonding_curve_findings/h-03-sharebalance-bloating-eventually-blocks-curator-rewards-distribution.md
- [Report-08]: reports/bonding_curve_findings/m-02-dos-of-createbondingcurve.md
- [Report-09]: reports/bonding_curve_findings/m-07-attacker-can-dos-user-from-selling-shares-of-a-credid.md
- [Report-10]: reports/bonding_curve_findings/m-3-share-price-inflation-by-first-lp-er-enabling-dos-attacks-on-subsequent-buys.md
- [Report-11]: reports/bonding_curve_findings/m-8-a-newly-deployed-pool-can-be-dos.md
- [Report-12]: reports/bonding_curve_findings/mnbd1-4-tokens-cannot-graduate-if-an-attacker-transfers-kas-to-the-bondingcurvep.md
- [Report-13]: reports/bonding_curve_findings/linearity-assumption-on-the-royalty-can-lead-to-denial-of-service.md
- [Report-14]: reports/bonding_curve_findings/griefing-of-csmodulecompensateelrewardsstealingpenalty.md

## Vulnerability Title

**Denial of Service and Griefing Attacks on Bonding Curves, Pool Creation, and Share Distribution**

### Overview

Bonding curve protocols are systematically vulnerable to denial-of-service and griefing attacks that exploit deterministic address pre-funding, integer overflow in index variables, gas limit exhaustion via unbounded iterations, share price inflation by first depositors, zero-amount edge cases in withdrawal flows, and permissionless functions that can be front-run to prevent legitimate operations.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | bonding_curve_creation, pool_migration, share_distribution, liquidity_provision | bonding_curve_dos_griefing`
- Interaction scope: `single_contract`
- Primary affected component(s): `bonding_curve_creation, pool_migration, share_distribution, liquidity_provision`
- High-signal code keywords: `EnumerableMap`, `PDA_pre_funding`, `_findSlice`, `approve`, `block.timestamp`, `buy`, `buyShareCredFor`, `deposit`
- Typical sink / impact: `dos`
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

### Vulnerability Description

#### Root Cause

The fundamental issues across all 14 findings fall into these categories:

1. **Deterministic address pre-funding** — PDA or CREATE2 addresses can be pre-funded/pre-created to break invariant checks during bonding curve creation (Reports 1, 2, 5, 8)
2. **Integer overflow in iteration** — Using `uint8` for index variables that can exceed 256 causes silent overflow and infinite loops (Report 3)
3. **Unbounded loop gas exhaustion** — Iterating over growing arrays without pagination hits block gas limit (Reports 4, 7)
4. **First depositor share inflation** — First LP can inflate share price via donation, making subsequent deposits require extreme capital (Report 10)
5. **Zero-amount edge cases** — Functions that revert on zero amounts called unconditionally in multi-step flows (Report 6)
6. **Zero-amount first provision** — Pool allows zero-amount first liquidity provision, bricking all subsequent operations via division-by-zero (Report 11)
7. **Force-sent native tokens** — `selfdestruct` or direct transfers inflate `address(this).balance`, breaking balance-based calculations (Report 12)
8. **Permissionless function front-running** — Lock timers reset by third-party calls or compensation functions griefed by minimal front-run (Reports 9, 14)
9. **Non-linear royalty assumptions** — Binary search assumes linear royalties; non-linear providers cause incorrect pricing and swap reverts (Report 13)

---

### Vulnerable Pattern Examples

---

#### **Pattern 1: Deterministic Escrow Pre-Funding Breaks Invariant** [HIGH]
**Protocol**: PumpScience | **Auditor**: Pashov Audit Group | **Severity**: High

```rust
// ❌ VULNERABLE: sol_escrow PDA is deterministic; pre-funding breaks invariant
pub fn handler(ctx: Context<CreateBondingCurve>, params: CreateBondingCurveParams) -> Result<()> {
    ctx.accounts.bonding_curve.update_from_params(...);
    // real_sol_reserves initialized to 0
    BondingCurve::invariant(locker)?; // Fails if escrow has existing SOL
}

pub fn invariant<'info>(ctx: &mut BondingCurveLockerCtx<'info>) -> Result<()> {
    if sol_escrow_lamports != bonding_curve.real_sol_reserves {
        return Err(ContractError::BondingCurveInvariant.into());
    }
}
```

**Root Cause**: The `sol_escrow` PDA address is deterministic from the known mint. An attacker sends SOL to the escrow before curve creation. Since `real_sol_reserves` starts at 0, the invariant check fails permanently.

**Impact**: Permanent DOS of bonding curve creation for that mint.

**Recommended Fix**: Initialize `real_sol_reserves` to match any existing SOL balance; or add a sweep mechanism before the invariant check.

---

#### **Pattern 2: Direct Transfers Break Running Invariant** [HIGH]
**Protocol**: PumpScience | **Auditor**: Pashov Audit Group | **Severity**: High

```rust
// ❌ VULNERABLE: External transfers inflate lamports but not real_sol_reserves
if sol_escrow_lamports != bonding_curve.real_sol_reserves {
    return Err(ContractError::BondingCurveInvariant.into());
}
// Any direct SOL transfer to sol_escrow breaks this for ALL swap operations
```

**Root Cause**: `real_sol_reserves` is only updated during swaps, but the escrow's actual lamport balance can change via direct transfers. Even 1 lamport difference bricks all swaps.

**Impact**: Permanent DOS of all buy/sell operations on the bonding curve.

**Recommended Fix**: Use `>=` instead of `==` for the invariant check, or add a sync function to reconcile the difference.

---

#### **Pattern 3: uint8 Index Overflow Causes Infinite Loop** [HIGH]
**Protocol**: Cowri Labs Shell Protocol v2 (Proteus AMM) | **Auditor**: Trail of Bits | **Severity**: High

```solidity
// ❌ VULNERABLE: uint8 wraps on overflow when slices > 256
function _findSlice(int128 m) internal view returns (uint8 i) {
    i = 0;
    while (i < slices.length) {
        if (m <= slices[i].mLeft && m > slices[i].mRight) return i;
        unchecked { ++i; }  // Wraps at 256 → infinite loop → OOG
    }
    return i - 1;
}
```

**Root Cause**: The index variable `i` is `uint8`, capping iteration at 256. With >256 slices, `unchecked { ++i }` wraps to 0, causing an infinite loop that consumes all gas.

**Attack Steps**:
1. Eve creates pool with valid initial parameters
2. Alice deposits $100K into pool
3. Eve calls `_updateSlices` setting 257 slices
4. Current balance ratio falls in slice 257 — `_findSlice` infinite loops
5. All swaps, deposits, withdrawals permanently revert (OOG)

**Recommended Fix**: Change `uint8` to `uint256`; add upper bound on slice count; add timelock on `_updateSlices`.

---

#### **Pattern 4: Unbounded Recipient Loop Hits Gas Limit** [MEDIUM]
**Protocol**: Pangolin Exchange | **Auditor**: Halborn | **Severity**: Medium

```solidity
// ❌ VULNERABLE: Unbounded loop over growing recipient list
function distribute() external {
    for (uint i; i < _recipientsLength; i++) {
        Recipient memory recipient = _recipients[i];
        uint amount = recipient.allocation * _vestingAmount / DENOMINATOR;
        if (!recipient.isMiniChef) {
            vestedToken.mint(recipient.account, amount);
        } else {
            vestedToken.mint(address(this), amount);
            vestedToken.approve(recipient.account, amount);
            IMiniChefV2(recipient.account).fundRewards(amount, VESTING_CLIFF);
        }
    }
}
```

**Root Cause**: No upper bound on recipient count. As recipients grow, gas exceeds block limit.

**Recommended Fix**: Limit recipient count or implement batch-based distribution with pagination.

---

#### **Pattern 5: Pre-Created PDA Blocks Pool Lock Operation** [HIGH]
**Protocol**: Pump Science | **Auditor**: Code4rena | **Severity**: High

```rust
// ❌ VULNERABLE: lockEscrow uses init (not init_if_needed), owner is not a signer
#[account(
    init,
    seeds = ["lock_escrow".as_ref(), pool.key().as_ref(), owner.key().as_ref()],
    space = 8 + std::mem::size_of::<LockEscrow>(),
    bump,
    payer = payer,
)]
pub lock_escrow: UncheckedAccount<'info>,
pub owner: UncheckedAccount<'info>, // no signer constraint!
```

**Root Cause**: `lock_escrow` PDA derived from `pool + owner` without requiring owner signature. Attacker derives and pre-creates the account, causing `init` to fail.

**Impact**: LP tokens cannot be locked; post-graduation migration permanently blocked.

**Recommended Fix**: Use `init_if_needed` instead of `init`; or require owner signature.

---

#### **Pattern 6: Zero-Amount Withdrawal Bricks Multi-Step Flow** [HIGH]
**Protocol**: Asymmetry Finance | **Auditor**: Code4rena | **Severity**: High

```solidity
// ❌ VULNERABLE: Both calls unconditional; either reverts on zero amount
ISafEth(SAF_ETH_ADDRESS).unstake(withdrawInfo.safEthWithdrawAmount, 0);
AbstractStrategy(vEthAddress).withdraw(withdrawInfo.vEthWithdrawId);

// SafEth: if (_safEthAmount == 0) revert AmountTooLow();
// Curve:  assert dx > 0  # dev: do not exchange 0 coins
```

**Root Cause**: `AfEth.withdraw()` calls both `SafEth.unstake()` and `VotiumStrategy.withdraw()` unconditionally. When one allocation is zero, the corresponding call reverts, bricking the entire withdrawal permanently.

**Recommended Fix**: Guard each call with a zero-amount check before execution.

---

#### **Pattern 7: Zero-Balance Map Entries Block Reward Distribution** [HIGH]
**Protocol**: Phi | **Auditor**: Code4rena | **Severity**: High

```solidity
// ❌ VULNERABLE: Sold shares leave zero entries in EnumerableMap
if ((currentNum - amount_) == 0) {
    _removeCredIdPerAddress(credId_, sender_);
    _credIdExistsPerAddress[sender_][credId_] = false;
}
shareBalance[credId_].set(sender_, currentNum - amount_); // Zero entry persists
// distribute() enumerates ALL entries including zeros → gas limit exceeded at ~4000 entries
```

**Root Cause**: When curators sell all shares, their entry is set to 0 instead of removed from the `EnumerableMap`. The map grows unbounded, and `distribute()` iterates all entries, hitting gas limit at ~4000 entries.

**Impact**: Reward distribution permanently blocked for affected `credId`.

**Recommended Fix**: Remove entries from the map when balance reaches zero: `shareBalance[credId_].remove(sender_)`.

---

#### **Pattern 8: Pre-Created Token Account Blocks Curve Creation** [MEDIUM]
**Protocol**: PumpScience | **Auditor**: Pashov Audit Group | **Severity**: Medium

```rust
// ❌ VULNERABLE: Deterministic ATA uses init (not init_if_needed)
#[account(
    init,
    payer = creator,
    associated_token::mint = mint,
    associated_token::authority = bonding_curve,
)]
bonding_curve_token_account: Box<Account<'info, TokenAccount>>,
```

**Root Cause**: The associated token account address is deterministic. An attacker creates it before the curve, causing `init` to fail.

**Recommended Fix**: Use `init_if_needed` instead of `init`.

---

#### **Pattern 9: Third-Party Purchases Reset Share Lock Timer** [MEDIUM]
**Protocol**: Phi | **Auditor**: Code4rena | **Severity**: Medium

```solidity
// ❌ VULNERABLE: Anyone can buy shares for another user, resetting their lock
function buyShareCredFor(uint256 credId_, uint256 amount_, address curator_, uint256 maxPrice_) public payable {
    _handleTrade(credId_, amount_, true, curator_, maxPrice_);
}
// In _handleTrade, isBuy resets lastTradeTimestamp for curator_
if (isBuy) {
    lastTradeTimestamp[credId_][curator_] = block.timestamp;
}
// Sell blocked during SHARE_LOCK_PERIOD after last trade
```

**Root Cause**: `buyShareCredFor()` allows anyone to buy shares on behalf of another user, resetting their `lastTradeTimestamp`. Repeated calls every ~10 minutes indefinitely prevent the target from selling.

**Impact**: Target cannot sell shares; price can drop during enforced lock, causing financial loss.

**Recommended Fix**: Don't reset lock timer when third parties buy on a user's behalf; or remove `buyShareCredFor`.

---

#### **Pattern 10: First Depositor Share Price Inflation** [MEDIUM]
**Protocol**: DODO GSP | **Auditor**: Sherlock | **Severity**: Medium

```solidity
// ❌ VULNERABLE: First depositor can inflate share price
// Step 1: Mint 1001 shares with minimal deposit
// Step 2: Sell 1000 shares, keeping 1 wei
// Step 3: Donate large amounts + sync() → reserves inflated per share
// Step 4: Subsequent depositors get shares < 1001 → _mint reverts
require(value > 1000, "MINT_AMOUNT_NOT_ENOUGH");
```

**Root Cause**: No minimum liquidity lock on first deposit. Attacker mints minimal shares, sells most, then donates to inflate per-share reserves. New depositors need >1001× the attacker's cost.

**Impact**: Pool permanently DOS'd — no new LPs can join without extreme capital.

**Recommended Fix**: Lock first 1001 LP tokens to address(0) on initial deposit (Uniswap V2 pattern).

---

#### **Pattern 11: Zero-Amount First Provision Bricks Pool** [MEDIUM]
**Protocol**: Dango DEX | **Auditor**: Sherlock | **Severity**: Medium

```rust
// ❌ VULNERABLE: No check that first provision amounts are non-zero
// After zero provision: supply > 0 but reserves = 0
// Subsequent provisions:
let invariant_ratio = Price::checked_from_ratio(invariant_after, invariant_before)?;
// invariant_before = 0 → division by zero → permanent revert
```

**Root Cause**: First liquidity provision accepts zero amounts, setting supply > 0 with zero reserves. All subsequent `provide_liquidity` hits division-by-zero.

**Recommended Fix**: Require non-zero amounts and non-zero LP mint on first provision.

---

#### **Pattern 12: Force-Sent Native Tokens Block Graduation** [MEDIUM]
**Protocol**: Moonbound | **Auditor**: Hexens | **Severity**: Medium

```solidity
// ❌ VULNERABLE: address(this).balance includes force-sent tokens
function graduateToken() internal {
    uint256 kasCollected = address(this).balance; // Inflated by selfdestruct
    uint256 tokenForLiquidity = (kasCollected * SCALING_FACTOR) / currentPrice;
    // tokenForLiquidity > reservedTokens → revert
}
```

**Root Cause**: `graduateToken()` uses `address(this).balance` (inflatable via `selfdestruct`) to compute required tokens. Inflated balance causes `tokenForLiquidity` to exceed `reservedTokens`, reverting graduation.

**Recommended Fix**: Track collected funds in state variable instead of using `address(this).balance`; or cap `tokenForLiquidity` to `reservedTokens`.

---

#### **Pattern 13: Non-Linear Royalty Breaks Binary Search** [HIGH]
**Protocol**: Sudoswap | **Auditor**: Cyfrin | **Severity**: High

```solidity
// ❌ VULNERABLE: Assumes royalty is linear to trade size
currentOutput -= currentOutput * royaltyAmount / BASE;
// priceToFillAt computed from linearity assumption
// Non-linear royalty providers → wrong priceToFillAt → swap reverts
```

**Root Cause**: `VeryFastRouter._findMaxFillableAmtForSell/Buy` assumes royalty amounts scale linearly with trade size. Non-linear royalty providers (rounding, custom logic) cause computed `priceToFillAt` to exceed actual output, reverting legitimate swaps.

**Recommended Fix**: Calculate per-trade royalty amounts; don't extrapolate from linearity assumption.

---

#### **Pattern 14: Permissionless Compensation Function Griefed by Front-Run** [MEDIUM]
**Protocol**: Lido CSM | **Auditor**: MixBytes | **Severity**: Medium

**Root Cause**: `compensateELRewardsStealingPenalty()` is permissionless. A griefer front-runs the legitimate call with 1-share compensation, reducing the locked amount below the original transaction's amount, causing revert.

**Recommended Fix**: Make the function permissioned (only callable by Node Operator manager).

---

### Impact Analysis

#### Technical Impact (Frequency across 14 reports)
- Permanent bonding curve creation DOS (3/14 — Solana PDA pre-funding)
- Complete pool/swap DOS via invariant violation (2/14)
- Withdrawal/distribution permanently bricked (3/14 — gas limit, zero amounts)
- Pool unusable for new LPs (2/14 — share inflation, zero provision)
- Graduation/migration blocked (2/14 — force-sent tokens, pre-created accounts)
- Selling prevention via timer manipulation (2/14)

#### Business Impact
- Protocol unable to launch new tokens (creation DOS)
- All user funds trapped in non-functional pools
- Reward distributions permanently blocked
- Users unable to exit positions (sell DOS)
- Economic griefing with minimal attacker cost

### Secure Implementation

**Fix 1: Handle Pre-Existing Balances in Deterministic Accounts**
```rust
// ✅ SECURE: Account for pre-existing balance on creation
pub fn handler(ctx: Context<CreateBondingCurve>) -> Result<()> {
    let existing_balance = ctx.accounts.sol_escrow.lamports();
    ctx.accounts.bonding_curve.real_sol_reserves = existing_balance;
    // Or: sweep existing balance to admin
}
```

**Fix 2: Use >= Instead of == for Balance Invariants**
```rust
// ✅ SECURE: Allow balance to be higher than tracked (excess is ignored)
if sol_escrow_lamports < bonding_curve.real_sol_reserves {
    return Err(ContractError::BondingCurveInvariant.into());
}
```

**Fix 3: Lock Minimum Liquidity on First Deposit**
```solidity
// ✅ SECURE: Uniswap V2 pattern prevents share inflation
uint256 MINIMUM_LIQUIDITY = 1000;
if (totalSupply == 0) {
    shares = Math.sqrt(amount0 * amount1) - MINIMUM_LIQUIDITY;
    _mint(address(0), MINIMUM_LIQUIDITY); // Permanently locked
}
```

**Fix 4: Guard Multi-Step Flows Against Zero Amounts**
```solidity
// ✅ SECURE: Check before each call
if (withdrawInfo.safEthWithdrawAmount > 0) {
    ISafEth(SAF_ETH_ADDRESS).unstake(withdrawInfo.safEthWithdrawAmount, 0);
}
if (cvxWithdrawAmount > 0) {
    ethReceived = sellCvx(cvxWithdrawAmount);
}
```

**Fix 5: Track State Instead of Using address(this).balance**
```solidity
// ✅ SECURE: Internal accounting immune to selfdestruct donations
uint256 public trackedBalance;

function buy() external payable {
    trackedBalance += msg.value;
}

function graduateToken() internal {
    uint256 kasCollected = trackedBalance; // Not address(this).balance
}
```

### Detection Patterns

```
- Pattern: init (not init_if_needed) on deterministic PDA/CREATE2 accounts
- Pattern: Strict equality (==) invariant check on account.lamports or address(this).balance
- Pattern: uint8 used as loop index with dynamic array length
- Pattern: Unbounded for loop over growing array without pagination
- Pattern: Zero-amount call to external protocol that reverts on zero
- Pattern: EnumerableMap entries set to 0 instead of removed
- Pattern: buyFor/transferFor functions that reset lock timers
- Pattern: First deposit without minimum liquidity lock
- Pattern: address(this).balance used in graduation/migration calculations
- Pattern: Permissionless compensation/penalty functions without griefing protection
```

### Keywords for Search

`DOS`, `denial of service`, `griefing`, `pre-funding`, `deterministic address`, `PDA`, `init_if_needed`, `invariant`, `escrow`, `lamports`, `selfdestruct`, `force send`, `uint8 overflow`, `gas limit`, `unbounded loop`, `EnumerableMap`, `shareBalance`, `zero amount`, `MINIMUM_LIQUIDITY`, `share inflation`, `first depositor`, `donation attack`, `buyShareCredFor`, `lock timer`, `SHARE_LOCK_PERIOD`, `division by zero`, `royalty linearity`, `compensate`, `front-run`, `block gas limit`, `OOG`, `out of gas`

### Related Vulnerabilities

- Bonding Curve State Management Vulnerabilities
- Vault Inflation / First Depositor Attacks
- Solana PDA Security Issues
- Gas Griefing Attacks
- Force-Sending Native Tokens

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

`EnumerableMap`, `PDA`, `PDA_pre_funding`, `_findSlice`, `approve`, `block.timestamp`, `bonding_curve`, `bonding_curve_dos_griefing`, `buy`, `buyShareCredFor`, `defi`, `denial_of_service`, `deposit`, `deterministic_address`, `distribute`, `dos`, `escrow`, `escrow_invariant`, `first_depositor`, `gas_limit`, `graduateToken`, `griefing`, `init_if_needed`, `legitimate`, `mint`, `permissioned`, `pre_funding`, `selfdestruct`, `share_inflation`, `solana`, `swap`, `uint8_overflow`, `zero_amount`
