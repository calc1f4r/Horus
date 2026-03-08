---
# Core Classification (Required)
protocol: generic
chain: sui
category: defi_logic
vulnerability_type: state_management|reward_accounting|staking_logic|order_book|tank_accounting

# Attack Vector Details (Required)
attack_type: logical_error|state_manipulation|data_manipulation
affected_component: reward_system|staking|unstaking|vault|tank|order_book|flow_tracking|stake_update

# Technical Primitives (Required)
primitives:
  - reward_accumulator
  - stake_update
  - tank_deposit
  - vault_redeem
  - order_fill
  - flow_limiter
  - epoch_reward
  - pending_coins
  - surplus_claim
  - exchange_rate
  - total_staked
  - unbonding
  - collateral
  - redistribution
  - function_call
  - record_name

# Impact Classification (Required)
severity: high
impact: fund_loss|incorrect_accounting|protocol_insolvency|reward_theft
exploitability: 0.65
financial_impact: high

# Context Tags
tags:
  - sui
  - move
  - defi
  - staking
  - rewards
  - vault
  - tank
  - order_book
  - flow_tracking
  - liquid_staking
  - surplus
  - epoch
  - state_management

# Version Info
language: move
version: all
---

## References & Source Reports

> **For Agents**: Read the full report for each finding at the referenced path.

### State Management / Accounting Errors
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Improper Stake Update | `reports/sui_move_findings/improper-stake-update.md` | MEDIUM | OtterSec | Bucket Protocol |
| Improper Tank Value Update | `reports/sui_move_findings/improper-tank-value-update.md` | MEDIUM | OtterSec | Bucket Protocol |
| Utilization of Incorrect Flow Tracking | `reports/sui_move_findings/utilization-of-incorrect-flow-tracking.md` | HIGH | OtterSec | Axelar |
| Incorrect Function Call | `reports/sui_move_findings/incorrect-function-call.md` | MEDIUM | OtterSec | Axelar |

### Reward Accounting Errors
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Incorrectly Calculated Reward Period | `reports/sui_move_findings/incorrectly-calculated-reward-period.md` | MEDIUM | OtterSec | Turbos Finance |
| Reward Accumulation During Inactive Period | `reports/sui_move_findings/reward-accumulation-during-inactive-time-period.md` | MEDIUM | OtterSec | Bluefin Spot |

### Liquid Staking Logic Errors
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Restake SUI Issue | `reports/sui_move_findings/restake-sui.md` | MEDIUM | OtterSec | Volo |
| Include Pending in Unstake | `reports/sui_move_findings/include-pending-in-unstake.md` | MEDIUM | OtterSec | Volo |
| Round Up Shares | `reports/sui_move_findings/round-up-shares.md` | HIGH | OtterSec | Volo |

### Vault / Tank Fund Loss
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Users Unable to Claim Surplus | `reports/sui_move_findings/users-unable-to-claim-surplus.md` | HIGH | OtterSec | Bucket Protocol |
| Share Price Manipulation | `reports/sui_move_findings/share-price-manipulation.md` | HIGH | OtterSec | BlueFin |
| Share Price Inflation | `reports/sui_move_findings/share-price-inflation.md` | MEDIUM | OtterSec | BlueFin |
| Price Manipulation | `reports/sui_move_findings/price-manipulation.md` | MEDIUM | OtterSec | Aftermath |

### Order Book Logic Errors
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Incorrect Base Quantity Calculation | `reports/sui_move_findings/incorrect-base-quantity-calculation.md` | HIGH | OtterSec | DeepBook V3 |
| Improper Order Quantity Calculation | `reports/sui_move_findings/improper-order-quantity-calculation.md` | MEDIUM | OtterSec | DeepBook V3 |

### Artifacts Index
| Artifact | Source | Type |
|----------|--------|------|
| `artifacts/7-github.com-Bucket-Protocol-v1-periphery-2f6.html` | Bucket Protocol GitHub | HTML |
| `artifacts/11-github.com-volo-sui-volo-liquid-staking-2f4.html` | Volo Liquid Staking GitHub | HTML |
| `artifacts/13-github.com-axelarnetwork-axelar-cgp-sui-3c5.html` | Axelar CGP Sui GitHub | HTML |

---

# Sui Move DeFi Logic & State Management Vulnerabilities — Comprehensive Database

**A Complete Pattern-Matching Guide for DeFi State Management, Reward Accounting, and Protocol Logic in Sui/Move**

---

## Table of Contents

1. [Improper Stake Accounting Updates](#1-improper-stake-accounting-updates)
2. [Tank/Stability Pool Value Update Errors](#2-tankstability-pool-value-update-errors)
3. [Surplus Claim Logic Failure](#3-surplus-claim-logic-failure)
4. [Incorrect Flow Rate Tracking](#4-incorrect-flow-rate-tracking)
5. [Wrong Function Call in Integration](#5-wrong-function-call-in-integration)
6. [Reward Accumulation During Inactive Periods](#6-reward-accumulation-during-inactive-periods)
7. [Reward Period Boundary Errors](#7-reward-period-boundary-errors)
8. [Liquid Staking: Pending Coin Inclusion in Unstake](#8-liquid-staking-pending-coin-inclusion-in-unstake)
9. [Liquid Staking: Restake Routing Errors](#9-liquid-staking-restake-routing-errors)
10. [Liquid Staking: Share Rounding Direction](#10-liquid-staking-share-rounding-direction)
11. [Order Book: Base/Quote Quantity Mismatch](#11-order-book-basequote-quantity-mismatch)
12. [Order Book: Partial Fill Tracking](#12-order-book-partial-fill-tracking)
13. [Share Price Manipulation via Donation](#13-share-price-manipulation-via-donation)
14. [Share Price Inflation via Rounding Drift](#14-share-price-inflation-via-rounding-drift)
15. [Exchange Rate Manipulation at Low TVL](#15-exchange-rate-manipulation-at-low-tvl)

---

## 1. Improper Stake Accounting Updates

### Overview

Stability pool (tank) systems track each user's "stake" — their proportional claim on the pool. When the accounting update applies the wrong formula or uses stale values, users' stakes become disconnected from their actual entitlements.

> **Validation strength**: Moderate — 1 report from OtterSec on Bucket Protocol
> **Frequency**: 1/69 reports

### Vulnerability Description

#### Root Cause

The stake update function uses the wrong multiplier or doesn't account for compounding effects. For example, applying a global multiplier directly instead of relative to the user's last-seen multiplier.

### Vulnerable Pattern Examples

**Example 1: Stake Not Adjusted Relative to User's Last Snapshot** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/improper-stake-update.md`
```move
// ❌ VULNERABLE: Uses absolute multiplier instead of relative
public fun update_user_stake(tank: &mut Tank, user: &mut UserStake) {
    let global_scale = tank.global_accumulator;
    // BUG: Should compute relative change since user's last update
    user.stake = user.initial_deposit * global_scale / PRECISION;
    // This doesn't account for user's own accumulator snapshot
}
```

### Secure Implementation

```move
// ✅ SECURE: Use relative accumulator pattern
public fun update_user_stake(tank: &Tank, user: &mut UserStake) {
    let relative_change = tank.global_accumulator - user.last_accumulator;
    user.stake = user.stake + (user.stake * relative_change / PRECISION);
    user.last_accumulator = tank.global_accumulator;
}
```

---

## 2. Tank/Stability Pool Value Update Errors

### Overview

Bucket Protocol's stability pool ("tank") tracks pool-wide value changes for proportional redistribution. Updating the tank value with wrong amounts or at wrong times corrupts all subsequent stake calculations.

> **Validation strength**: Moderate — 1 report from OtterSec on Bucket Protocol
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Tank Value Updated with Wrong Amount** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/improper-tank-value-update.md`
```move
// ❌ VULNERABLE: Updates tank total with deposited amount instead of net change
public fun process_liquidation(tank: &mut Tank, collateral_gained: u64, debt_absorbed: u64) {
    tank.total_deposited = tank.total_deposited + collateral_gained;
    // BUG: total should decrease by debt_absorbed, not increase by collateral_gained
    // Should be: tank.total_deposited = tank.total_deposited - debt_absorbed;
    // Collateral tracking should be separate
}
```

### Secure Implementation

```move
// ✅ SECURE: Track stablecoin deposits and collateral rewards separately
struct Tank has key, store {
    total_stablecoin: u64,       // Decreases on liquidation
    total_collateral_reward: u64, // Increases on liquidation
}

public fun process_liquidation(tank: &mut Tank, collateral_gained: u64, debt_absorbed: u64) {
    tank.total_stablecoin = tank.total_stablecoin - debt_absorbed;
    tank.total_collateral_reward = tank.total_collateral_reward + collateral_gained;
}
```

---

## 3. Surplus Claim Logic Failure

### Overview

When a stability pool (tank) is emptied through liquidations, remaining users should be able to claim their proportional surplus. A logic error can make the surplus forever unclaimable.

> **Validation strength**: Strong — 1 report from OtterSec on Bucket Protocol
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Surplus Locked Due to Zero-Division Guard** [HIGH]
> 📖 Reference: `reports/sui_move_findings/users-unable-to-claim-surplus.md`
```move
// ❌ VULNERABLE: When total_deposit = 0, surplus cannot be distributed
public fun claim_surplus(tank: &mut Tank, user: &mut UserStake, ctx: &mut TxContext) {
    // After full liquidation, total_deposit = 0
    let user_share = user.deposit * PRECISION / tank.total_deposit;
    // Division by zero → abort, surplus permanently locked
    let surplus = user_share * tank.collateral_surplus / PRECISION;
    // ...
}
```

### Secure Implementation

```move
// ✅ SECURE: Handle zero total_deposit case for surplus distribution
public fun claim_surplus(tank: &mut Tank, user: &mut UserStake, ctx: &mut TxContext) {
    if (tank.total_deposit == 0) {
        // Use snapshot of deposits before final liquidation
        let user_share = user.deposit_snapshot * PRECISION / tank.total_deposit_snapshot;
        let surplus = user_share * tank.collateral_surplus / PRECISION;
        transfer_surplus(surplus, tx_context::sender(ctx));
    } else {
        let user_share = user.deposit * PRECISION / tank.total_deposit;
        let surplus = user_share * tank.collateral_surplus / PRECISION;
        transfer_surplus(surplus, tx_context::sender(ctx));
    }
}
```

---

## 4. Incorrect Flow Rate Tracking

### Overview

Cross-chain bridges like Axelar track flow rates (token volume per time period) for rate limiting. Using the wrong flow direction (inbound vs outbound) or wrong token type corrupts the rate limiter, either blocking legitimate transfers or allowing excessive ones.

> **Validation strength**: Strong — 1 report from OtterSec on Axelar
> **Frequency**: 1/69 reports (generalizable to any rate-limited system)

### Vulnerable Pattern Examples

**Example 1: Wrong Flow Direction Tracked** [HIGH]
> 📖 Reference: `reports/sui_move_findings/utilization-of-incorrect-flow-tracking.md`
```move
// ❌ VULNERABLE: Inbound flow tracked as outbound (or vice versa)
public fun process_inbound_transfer(limiter: &mut FlowLimiter, amount: u64) {
    // BUG: Updates outbound flow instead of inbound flow
    limiter.outbound_flow = limiter.outbound_flow + amount;
    // This incorrectly reduces outbound capacity while not tracking inbound
    // Attacker can exceed inbound limits; legitimate outbound transfers blocked
}
```

### Secure Implementation

```move
// ✅ SECURE: Track correct flow direction
public fun process_inbound_transfer(limiter: &mut FlowLimiter, amount: u64) {
    limiter.inbound_flow = limiter.inbound_flow + amount;
    assert!(limiter.inbound_flow <= limiter.inbound_limit, E_INBOUND_LIMIT_EXCEEDED);
}

public fun process_outbound_transfer(limiter: &mut FlowLimiter, amount: u64) {
    limiter.outbound_flow = limiter.outbound_flow + amount;
    assert!(limiter.outbound_flow <= limiter.outbound_limit, E_OUTBOUND_LIMIT_EXCEEDED);
}
```

---

## 5. Wrong Function Call in Integration

### Overview

When integrating with external modules or SDKs, calling a similar-but-wrong function (e.g., `add_flow_out` instead of `add_flow_in`) produces silently incorrect behavior.

> **Validation strength**: Moderate — 1 report from OtterSec on Axelar
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Incorrect Function Name in Integration** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/incorrect-function-call.md`
```move
// ❌ VULNERABLE: Calls wrong flow tracking function
public fun handle_receive(gateway: &mut Gateway, message: Message) {
    // ... process incoming message ...
    flow_limiter::add_flow_out(&mut gateway.limiter, message.amount);
    // BUG: Should be add_flow_in — this is an INCOMING message
}
```

### Secure Implementation

```move
// ✅ SECURE: Correct function call matching the operation semantics
public fun handle_receive(gateway: &mut Gateway, message: Message) {
    flow_limiter::add_flow_in(&mut gateway.limiter, message.amount);
}
```

### Detection Patterns

```
- Function calls with "in"/"out" or "send"/"receive" that may be swapped
- Integration points where function names are similar but have opposite semantics
- Review all flow_limiter / rate_limiter call sites for direction correctness
```

---

## 6. Reward Accumulation During Inactive Periods

### Overview

DeFi reward systems that accumulate rewards per-epoch may continue accruing during periods when the position/liquidity is inactive, unfairly diluting active participants or creating phantom rewards.

> **Validation strength**: Moderate — 1 report from OtterSec on Bluefin Spot
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Rewards Accrue During Paused/Inactive Period** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/reward-accumulation-during-inactive-time-period.md`
```move
// ❌ VULNERABLE: Reward calculation doesn't exclude inactive periods
public fun calculate_rewards(
    position: &Position,
    current_epoch: u64,
    reward_rate: u64
): u64 {
    let elapsed = current_epoch - position.start_epoch;
    elapsed * reward_rate * position.liquidity / total_liquidity
    // Includes epochs where position was inactive/paused
    // Should only count active epochs
}
```

### Secure Implementation

```move
// ✅ SECURE: Track active epochs explicitly
struct Position has store {
    liquidity: u64,
    active_epochs: u64,     // Incremented each epoch the position is active
    last_active_epoch: u64, // Last epoch where position had activity
}

public fun update_epoch(position: &mut Position, current_epoch: u64) {
    if (position.is_active && current_epoch > position.last_active_epoch) {
        position.active_epochs = position.active_epochs + (current_epoch - position.last_active_epoch);
        position.last_active_epoch = current_epoch;
    };
}

public fun calculate_rewards(position: &Position, reward_rate: u64): u64 {
    position.active_epochs * reward_rate * position.liquidity / total_liquidity
}
```

---

## 7. Reward Period Boundary Errors

### Overview

Off-by-one errors in reward period boundary calculations cause rewards to either overcount (distributing beyond the designated period) or undercount (not distributing during the final eligible epoch).

> **Validation strength**: Moderate — 1 report from OtterSec on Turbos Finance
> **Frequency**: 1/69 reports

See [Arithmetic Precision Entry, Section 14](SUI_MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md#14-reward-period-miscalculation) for detailed patterns and secure implementations.

---

## 8. Liquid Staking: Pending Coin Inclusion in Unstake

### Overview

Liquid staking protocols on Sui (like Volo) manage pending coins that are in-transit between staking and active states. When the unstake calculation includes pending coins that haven't been formally staked, the exchange rate is artificially inflated.

> **Validation strength**: Moderate — 1 report from OtterSec on Volo
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Pending SUI Inflates Staking Total** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/include-pending-in-unstake.md`
```move
// ❌ VULNERABLE: Includes pending (not-yet-staked) SUI in total calculation
public fun get_total_sui(staking: &Staking): u64 {
    staking.staked_sui + staking.pending_sui  // pending_sui is not yet earning rewards
    // Inflates exchange rate: users get fewer shares per SUI on deposit
    // Or: users get more SUI per share on withdrawal
}
```

### Secure Implementation

```move
// ✅ SECURE: Only count actively staked SUI in exchange rate
public fun get_total_sui(staking: &Staking): u64 {
    staking.staked_sui  // Only count confirmed staked amount
    // Pending SUI tracked separately for operational purposes
}

// Or: Use a time-weighted approach where pending enters the total after confirmation
public fun get_total_sui_with_pending(staking: &Staking, clock: &Clock): u64 {
    let confirmed_pending = filter_confirmed(staking.pending_sui, clock);
    staking.staked_sui + confirmed_pending
}
```

---

## 9. Liquid Staking: Restake Routing Errors

### Overview

When liquid staking protocols redistribute stake across validators, routing errors can send stake to wrong validators or fail to properly track the redistribution.

> **Validation strength**: Moderate — 1 report from OtterSec on Volo
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Restake Doesn't Update Validator Tracking** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/restake-sui.md`
```move
// ❌ VULNERABLE: Restake moves SUI but doesn't update validator distribution record
public fun restake(
    staking: &mut Staking,
    from_validator: address,
    to_validator: address,
    amount: u64,
    ctx: &mut TxContext
) {
    let sui = unstake_from(staking, from_validator, amount, ctx);
    stake_to(staking, to_validator, sui, ctx);
    // BUG: validator_distribution map not updated
    // staking.validator_stakes[from_validator] still shows old amount
    // staking.validator_stakes[to_validator] still shows old amount
}
```

### Secure Implementation

```move
// ✅ SECURE: Update all tracking state on restake
public fun restake(
    staking: &mut Staking,
    from_validator: address,
    to_validator: address,
    amount: u64,
    ctx: &mut TxContext
) {
    let sui = unstake_from(staking, from_validator, amount, ctx);
    stake_to(staking, to_validator, sui, ctx);
    // Update validator distribution tracking
    let from_stake = table::borrow_mut(&mut staking.validator_stakes, from_validator);
    *from_stake = *from_stake - amount;
    let to_stake = table::borrow_mut(&mut staking.validator_stakes, to_validator);
    *to_stake = *to_stake + amount;
}
```

---

## 10. Liquid Staking: Share Rounding Direction

### Overview

When converting between SUI and staking shares (voSUI/stSUI), the rounding direction must always favor the protocol. Rounding in favor of the user allows small extraction of value on each operation.

> **Validation strength**: Strong — 1 report from OtterSec on Volo
> **Frequency**: 1/69 reports

See [Arithmetic Precision Entry, Section 11](SUI_MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md#11-share-to-asset-rounding-direction) for detailed patterns.

---

## 11. Order Book: Base/Quote Quantity Mismatch

### Overview

DeepBook V3's order matching engine must correctly calculate base and quote quantities during fills. Using the wrong field or formula produces incorrect trade amounts.

> **Validation strength**: Strong — 1 report from OtterSec on DeepBook V3
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Wrong Field Used in Base Quantity** [HIGH]
> 📖 Reference: `reports/sui_move_findings/incorrect-base-quantity-calculation.md`
```move
// ❌ VULNERABLE: Uses fill quantity where order quantity is expected
public(package) fun match_bid(order: &mut Order, fill_qty: u64): (u64, u64) {
    // BUG: base_qty should derive from the order's price and fill, not just fill_qty
    let base_qty = fill_qty;
    let quote_qty = mul_u64(base_qty, order.price);
    // base_qty and quote_qty are both wrong for limit orders
    (base_qty, quote_qty)
}
```

### Secure Implementation

```move
// ✅ SECURE: Correctly compute base and quote quantities
public(package) fun match_bid(order: &mut Order, fill_qty: u64): (u64, u64) {
    let quote_qty = fill_qty;  // fill_qty is in quote terms for bids
    let base_qty = div_u64(quote_qty, order.price);
    assert!(base_qty > 0, E_ZERO_FILL);
    (base_qty, quote_qty)
}
```

---

## 12. Order Book: Partial Fill Tracking

### Overview

Order books that allow partial fills must correctly track the unfilled quantity. Using the wrong base (original vs remaining) for subtraction leads to accounting errors.

> **Validation strength**: Moderate — 1 report from OtterSec on DeepBook V3
> **Frequency**: 1/69 reports

See [Arithmetic Precision Entry, Section 13](SUI_MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md#13-incorrect-quantity-calculation-in-order-books) for detailed patterns.

---

## 13. Share Price Manipulation via Donation

### Overview

Protocols where the share price = total_assets / total_shares are vulnerable to donation attacks. An attacker donates assets directly to inflate total_assets, manipulating the share price.

> **Validation strength**: Moderate — 2 reports from OtterSec across BlueFin and Aftermath
> **Frequency**: 2/69 reports

See [Arithmetic Precision Entry, Section 10](SUI_MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md#10-share-price-inflation--first-depositor-attack) for the first-depositor variant.

### Vulnerable Pattern Examples

**Example 1: Aftermath Pool NAV Manipulation** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/price-manipulation.md`
```move
// ❌ VULNERABLE: Pool's Net Asset Value is directly manipulable
public fun get_lp_price(pool: &Pool): u64 {
    let total_value = balance::value(&pool.reserve_a) * price_a + 
                      balance::value(&pool.reserve_b) * price_b;
    total_value / pool.total_lp_supply
    // Attacker donates reserve tokens → inflates LP price
    // Affects all operations using LP price: lending, liquidation, swaps
}
```

---

## 14. Share Price Inflation via Rounding Drift

### Overview

Even without direct donation, persistent rounding in withdraw operations (always rounding down the amount returned to user) causes the share price to slowly inflate. This is a design smell that compounds over time.

> **Validation strength**: Moderate — 1 report from OtterSec on BlueFin
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Withdrawal Rounding Inflates Share Price** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/share-price-inflation.md`
```move
// ❌ VULNERABLE: Every withdrawal leaves dust, inflating share price
public fun withdraw(vault: &mut Vault, shares: u64, ctx: &mut TxContext): Coin<SUI> {
    let amount = shares * vault.total_assets / vault.total_shares;  // Rounds DOWN
    vault.total_shares = vault.total_shares - shares;
    vault.total_assets = vault.total_assets - amount;
    // Dust = (shares * total_assets) % total_shares stays in vault
    // Over time, total_assets > expected → share price inflated
    coin::take(&mut vault.balance, amount, ctx)
}
```

### Secure Implementation

```move
// ✅ SECURE: Use virtual offset pattern to minimize rounding impact
const VIRTUAL_SHARES: u64 = 1_000_000;
const VIRTUAL_ASSETS: u64 = 1;

public fun withdraw(vault: &mut Vault, shares: u64, ctx: &mut TxContext): Coin<SUI> {
    let effective_shares = vault.total_shares + VIRTUAL_SHARES;
    let effective_assets = vault.total_assets + VIRTUAL_ASSETS;
    let amount = (shares as u128) * (effective_assets as u128) / (effective_shares as u128);
    vault.total_shares = vault.total_shares - shares;
    vault.total_assets = vault.total_assets - (amount as u64);
    coin::take(&mut vault.balance, (amount as u64), ctx)
}
```

---

## 15. Exchange Rate Manipulation at Low TVL

### Overview

When a liquid staking or vault protocol has very low TVL, the exchange rate is sensitive to small deposits or withdrawals. Attackers exploit this window to manipulate the rate in their favor.

> **Validation strength**: Moderate — derived from Volo + BlueFin patterns
> **Frequency**: 2/69 reports (combine round-up-shares + share-price-manipulation)

### Detection Patterns

#### Code Patterns to Look For
```
- Exchange rate calculation: total_sui / total_shares (or similar)
- No minimum TVL threshold before enabling deposits/withdrawals
- No virtual offset or minimum initial deposit
- share_to_amount or amount_to_share conversions without bounds
```

#### Audit Checklist
- [ ] Check first-depositor protection (virtual offset or minimum initial deposit)
- [ ] Verify rounding direction favors protocol on all operations
- [ ] Test exchange rate manipulation at very low TVL (< 100 tokens)
- [ ] Verify donation attacks are mitigated (accounted vs actual balance)
- [ ] Check that pending/unbonding amounts don't inflate exchange rates

---

## Prevention Guidelines

### DeFi Logic Best Practices on Sui
1. **Accumulator Pattern**: Use per-share accumulators with user snapshots for reward distribution
2. **Pull Over Push**: Users claim their own rewards/surplus instead of admin distributing
3. **Separate Tracking**: Track stablecoins and collateral rewards in separate fields
4. **Snapshot Before Zero**: Take state snapshots before total can reach zero
5. **Direction-Aware Rate Limiting**: Verify inbound/outbound flow tracking matches operation semantics
6. **Active Period Tracking**: Only accumulate rewards during active/non-paused epochs
7. **Exchange Rate Hardening**: Use virtual offsets, minimum TVL, and accounted (not actual) balances
8. **Order Book Invariants**: Assert base * price = quote (within precision) after every fill
9. **Validator State Sync**: Update all tracking maps when performing restake operations
10. **Rounding Direction**: Always round in protocol's favor (down on withdraw, up on deposit)

### Testing Requirements
- Verify stake/share calculations with small values (1, 2, 3)
- Test surplus claiming after total deposit reaches zero
- Test reward accumulation across paused/unpaused transitions
- Verify flow limiter direction by simulating inbound/outbound separately
- Test order matching with partial fills of varying sizes
- Property: total_shares * price_per_share ≈ total_assets (within dust tolerance)

---

### Keywords for Search

`stake_update`, `tank_value`, `surplus_claim`, `flow_limiter`, `flow_tracking`, `inbound_flow`, `outbound_flow`, `reward_accumulation`, `inactive_period`, `reward_period`, `epoch_reward`, `pending_sui`, `staked_sui`, `restake`, `validator_distribution`, `share_rounding`, `exchange_rate`, `round_up`, `round_down`, `base_quantity`, `quote_quantity`, `partial_fill`, `order_fill`, `unfilled_quantity`, `donation_attack`, `price_manipulation`, `NAV`, `total_assets`, `total_shares`, `virtual_offset`, `CLMM`, `stability_pool`, `liquidation`, `redistribution`, `collateral_reward`, `accumulator_pattern`, `snapshot`

### Related Vulnerabilities
- `DB/general/defi/share-inflation/` — Generic vault inflation patterns
- `DB/general/defi/precision-loss/` — Precision patterns
- `DB/amm/` — AMM-specific logic bugs
- `DB/tokens/erc4626/` — ERC4626 vault patterns (EVM equivalent)
