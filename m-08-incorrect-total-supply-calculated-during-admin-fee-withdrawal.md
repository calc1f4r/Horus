---
# Core Classification
protocol: YieldBasis_2025-03-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61984
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/YieldBasis-security-review_2025-03-26.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-08] Incorrect total supply calculated during admin fee withdrawal

### Overview


Bug report summary:

The bug involves an incorrect total supply calculation in the LT contract when the `withdraw_admin_fees` function is called. This is due to a failure to update the `self.totalSupply` value before minting new tokens to the fee receiver. The recommendation is to update the `self.totalSupply` value before minting tokens.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In the LT contract, when the `withdraw_admin_fees` function is called, the `_calculate_values` function is executed to recalculate all liquidity values. During this calculation, the total supply can be reduced due to a token reduction mechanism (downward rebasing) that adjusts the number of tokens based on value changes.

However, while the function updates various liquidity parameters, it fails to update `self.totalSupply` to the latest value `v.supply_tokens` before minting new tokens to the fee receiver. This mistake leads to an incorrect total supply calculation after admin fees are withdrawn.

```python
def withdraw_admin_fees():
    ...
    v: LiquidityValuesOut = self._calculate_values(self._price_oracle_w())
    ...
    self.liquidity.total = new_total
    self.liquidity.admin = 0
    self.liquidity.staked = v.staked
    staker: address = self.staker
    if staker != empty(address):
        self.balanceOf[staker] = v.staked_tokens

    log WithdrawAdminFees(receiver=fee_receiver, amount=to_mint)
```

## Recommendations

Update `self.totalSupply` to the recalculated value before minting tokens to the fee receiver.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | YieldBasis_2025-03-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/YieldBasis-security-review_2025-03-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

