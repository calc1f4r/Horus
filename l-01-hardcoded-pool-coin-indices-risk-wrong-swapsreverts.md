---
# Core Classification
protocol: RegnumAurum_2025-08-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63406
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2025-08-12.md
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

[L-01] Hardcoded pool coin indices risk wrong swaps/reverts

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

`_swap` calls the Curve pool with hardcoded indices `(1, 0)`:

```solidity
// Exchange index token (1) for crvUSD (0) since we swapped the order in the pool
liquidityPool.exchange(1, 0, amount, minDy, address(this)); // hardcoded indices
```

This assumes a single pool and a fixed coin order. If the pool is replaced or its coin order differs, approvals and `exchange()` indices won’t match the actual tokens, causing **reverts or unintended swaps**. Additionally, `minDy` is derived from `pricePerShare()` rather than the pool’s own quote, increasing slippage/mispricing risk.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RegnumAurum_2025-08-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2025-08-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

