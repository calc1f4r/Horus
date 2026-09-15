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
solodit_id: 61986
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/YieldBasis-security-review_2025-03-26.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-01] Staker contract missing in `LT` contract post-creation

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

In the Factory contract, the `add_market` function creates a staker contract for the market if `staker_impl` is provided. However, the code doesn't set this newly created staker in the corresponding LT contract. 

```python
def add_market(
    pool: CurveCryptoPool,
    fee: uint256,
    rate: uint256,
    debt_ceiling: uint256
) -> Market:
    ...
    if self.staker_impl != empty(address):
        market.staker = create_from_blueprint(
            self.staker_impl,
            market.lt)

    ...
```

Therefore, the staker exists but isn't properly configured in the LT contract. As a result, the staking functionality won't work properly until the staker is manually set in a separate transaction.

It's recommended to set the staker for the LT in add_market function.

```diff
    if self.staker_impl != empty(address):
        market.staker = create_from_blueprint(
            self.staker_impl,
            market.lt)
+       extcall LT(market.lt).set_staker(market.staker)
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

