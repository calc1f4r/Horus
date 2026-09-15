---
# Core Classification
protocol: Parallel Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18226
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/ParallelFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/ParallelFinance.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Artur Cygan Will Song Fredrik Dahlgren
---

## Vulnerability Title

Missing validation in multiple StakingLedger methods

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: High

## Type: Data Validation

## Target: pallets/liquid-staking/src/types.rs

## Description
The staking ledger is used to keep track of the total amount of staked funds in the system. It is updated in response to cross-consensus messaging (XCM) requests to the parent chain (either Polkadot or Kusama). A number of the `StakingLedger` methods lack sufficient input validation before they update the staking ledger’s internal state. Even though the input is validated as part of the original XCM call, there could still be issues due to implementation errors or overlooked corner cases.

First, the `StakingLedger::rebond` method does not use checked arithmetic to update the active balance. The method should also check that the computed `unlocking_balance` is equal to the input value at the end of the loop to ensure that the system remains consistent.

```rust
pub fn rebond(&mut self, value: Balance) {
    let mut unlocking_balance: Balance = Zero::zero();
    while let Some(last) = self.unlocking.last_mut() {
        if unlocking_balance + last.value <= value {
            unlocking_balance += last.value;
            self.active += last.value;
            self.unlocking.pop();
        } else {
            let diff = value - unlocking_balance;
            unlocking_balance += diff;
            self.active += diff;
            last.value -= diff;
        }
        if unlocking_balance >= value {
            break;
        }
    }
}
```

![Figure 4.1: pallets/liquid-staking/src/types.rs:199-219](Figure-4.1)

Second, the `StakingLedger::bond_extra` method does not use checked arithmetic to update the total and active balances.

```rust
pub fn bond_extra(&mut self, value: Balance) {
    self.total += value;
    self.active += value;
}
```

![Figure 4.2: pallets/liquid-staking/src/types.rs:223-226](Figure-4.2)

Finally, the `StakingLedger::unbond` method does not use checked arithmetic when updating the active balance.

```rust
pub fn unbond(&mut self, value: Balance, target_era: EraIndex) {
    if let Some(mut chunk) = self.unlocking.last_mut().filter(|chunk| chunk.era == target_era) {
        // To keep the chunk count down, we only keep one chunk per era. Since
        // `unlocking` is a FIFO queue, if a chunk exists for `era` we know that
        // it will be the last one.
        chunk.value = chunk.value.saturating_add(value);
    } else {
        self.unlocking.push(UnlockChunk {
            value,
            era: target_era,
        });
    }
    // Skipped the minimum balance check because the platform will
    // bond `MinNominatorBond` to make sure:
    // 1. No chill call is needed
    // 2. No minimum balance check
    self.active -= value;
}
```

![Figure 4.3: pallets/liquid-staking/src/types.rs:230-253](Figure-4.3)

Since the staking ledger is updated by a number of the XCM response handlers, and XCM responses may return out of order, it is important to ensure that input to the staking ledger methods is validated to prevent issues due to race conditions and corner cases. We could not find a way to exploit this issue, but we cannot rule out the risk that it could be used to cause a denial-of-service condition in the system.

## Exploit Scenario
The staking ledger's state is updated as part of a `WithdrawUnbonded` request, leaving the unlocking vector in the staking ledger empty. Later, when the response to a previous call to `rebond` is handled, the ledger is updated again, which leaves it in an inconsistent state.

## Recommendations
Short term, ensure that the balance represented by the staking ledger’s unlocking vector is enough to cover the input balance passed to `StakingLedger::rebond`. Use checked arithmetic in all staking ledger methods that update the ledger’s internal state to ensure that issues due to data races are detected and handled correctly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Parallel Finance |
| Report Date | N/A |
| Finders | Artur Cygan Will Song Fredrik Dahlgren |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/ParallelFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/ParallelFinance.pdf

### Keywords for Search

`vulnerability`

