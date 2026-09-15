---
# Core Classification
protocol: Orga and Merk
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43778
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-11-orgaandmerk-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-11-orgaandmerk-securityreview.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Tjaden Hess
  - Anish Naik
---

## Vulnerability Title

Slashing of re-delegated stake is computed incorrectly

### Overview


This bug report discusses an issue in the orga staking module where a miscalculation causes a higher percentage of funds to be slashed from redelegated stakes than intended. This can be exploited by a malicious validator to manipulate the price of the staking token by encouraging delegators to redelegate and then intentionally causing a double-signing fault. The report recommends short term and long term solutions to fix the issue and prevent it from being missed in unit testing.

### Original Finding Content

## Diﬃculty: Medium

## Type: Denial of Service

### Target: orga/src/coins/staking

## Description

When a validator is slashed due to double-signing, any stake delegated to that validator at the time of the misbehavior must also be slashed. The `orga` staking module allows delegators to transfer delegated coins from one validator to another; these coins are tracked so that the proper amount can be deducted if the original validator is slashed. 

Due to a miscalculation in the staking module, coins that are slashed while in the process of being re-delegated will forfeit an incorrect percentage of funds. For example, if the `slash_fraction_double_sign` percentage is 1/20, the re-delegated stake will be slashed by 95% rather than the intended 5%.

Figure 1.1 contains the code responsible for slashing redelegations. Note that the computed value `(multiplier * redelegation_amount)` is equal to the intended final balance after slashing. However, inside `slash_redelegation` (figure 1.2), this parameter is treated as an amount to deduct.

```rust
let multiplier = (Decimal::one() - self.slash_fraction_double_sign)?;
for entry in redelegations.iter() {
    let del_address = entry.delegator_address;
    for redelegation in entry.outbound_redelegations.iter() {
        let mut validator = self.validators.get_mut(redelegation.address.into())?;
        let mut delegator = validator.get_mut(del_address.into())?;
        delegator.slash_redelegation((multiplier * redelegation.amount)?.amount()?)?;
    }
}
```
*Figure 1.1: Input to `slash_redelegation` pre-deducts the slash amount (orga/src/coins/staking/mod.rs#503–511)*

```rust
pub (super) fn slash_redelegation(&mut self, amount: Amount) -> Result<()> {
    let stake_slash = if amount > self.staked.shares.amount()? {
        self.staked.shares.amount()?
    } else {
        amount
    };
    if stake_slash > 0 {
        self.staked.take(stake_slash)?.burn();
    }
}
```
*Figure 1.2: `slash_redelegation` burns the input amount (orga/src/coins/staking/delegator.rs#124–133)*

This miscalculation was not detected by the unit test suite because all unit testing is done with a `slash_fraction_double_sign` of ½, which is the unique value x for which `1 - x = x`.

## Exploit Scenario

Mallory, a malicious validator, encourages honest users to delegate their staking tokens to her. She wants to manipulate the price of the staking token by artificially burning the supply. Mallory tells her delegators that she will be switching accounts and encourages them to redelegate to another address. During the redelegation period, Mallory intentionally produces a double-sign fault and is slashed. Mallory loses only 5% of her own stake, but all of her delegators lose 95% of theirs, allowing Mallory to manipulate the overall supply at only a minor cost to herself.

## Recommendations

- Short term, compute the `slash_redelegation` amount by directly multiplying `slash_fraction_double_sign` by the redelegated amount.
- Long term, modify the test suite to use a value other than ½ for the slash fraction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Orga and Merk |
| Report Date | N/A |
| Finders | Tjaden Hess, Anish Naik |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-11-orgaandmerk-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-11-orgaandmerk-securityreview.pdf

### Keywords for Search

`vulnerability`

