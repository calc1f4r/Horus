---
# Core Classification
protocol: Interpol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42138
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Interpol-security-review.md
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

[M-03] Users can avoid paying fees to the protocol due to rounding

### Overview


The report describes a bug in the `HoneyLocker` contract where the owner can avoid paying fees when withdrawing funds by exploiting the rounding down feature in the EVM. This can be done by withdrawing small amounts of tokens, resulting in a zero fee calculation. This may not be profitable for most tokens due to high gas fees, but could be used for high-value tokens with fewer decimal places. To fix this, it is recommended to either always round up the fee calculation or set a minimum fee threshold.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

When the owner of a `HoneyLocker` initiates a withdrawal of funds through the `withdrawERC20` or `withdrawBERA` methods, a fee is required to be paid to both the referral and the treasury. However, the owner can take advantage of the rounding down in the EVM to avoid paying any fees at all. The root cause of the issue is in `HoneyQueen::computeFees`:

```solidity
uint256 public fees = 200; // in bps
// ...
function computeFees(uint256 amount) public view returns (uint256) {
    return (amount * fees) / 10000;
}
```

To exploit this, the owner can withdraw funds in very small batches. For instance, if an owner wants to withdraw 1,000,000 tokens, they can repeatedly request a withdrawal of just 49 tokens. This specific amount is chosen because, with a nominal fee rate of 2%, the calculated fee should round down to zero:

```solidity
49 * 200 / 10000 = 0
```

This attack is generally not cost-effective for most tokens because the gas fees required can exceed the benefit. However, it could be viable for high-value tokens that have fewer decimal places, where the loss from rounding becomes more significant relative to transaction costs.

## Recommendations

To mitigate this issue, two solutions are suggested:

1. Modify the fee calculation in `computeFees` to always round up, ensuring that no withdrawal is completely free of charge.
2. Set a minimum fee threshold so that no calculated fee results in zero, irrespective of the withdrawal amount.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Interpol |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Interpol-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

