---
# Core Classification
protocol: Vector Reserve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59679
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/vector-reserve/68ff317c-7b13-4bdf-8245-9df1bc99f7cc/index.html
source_link: https://certificate.quantstamp.com/full/vector-reserve/68ff317c-7b13-4bdf-8245-9df1bc99f7cc/index.html
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
finders_count: 3
finders:
  - Julio Aguilar
  - Mostafa Yassin
  - Guillermo Escobero
---

## Vulnerability Title

Managed Funds Are Not Validated at Redemption

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged". The Vector Reserve team provided the following explanation:

> _Managed funds would be sent back prior to a redemption period. - Acknowledged_

**File(s) affected:**`VectorETH.sol`

**Description:** LSTs and LRTs deposited in the `VectorETH` contract can be withdrawn by approved managers. The withdrawn amounts are tracked in `restakedLSTManaged` mapping.

In the event of a user redemption, `redeem()` just validates the amount in `totalRestakedLSTDeposited`, which can be greater than the actual balance of the LST in the contract. This can cause unexpected reverts when trying to transfer the tokens to the user - the contract could be insolvent.

**Recommendation:**

1.   The `redeem()` function should include managed LSTs in validations.
2.   The Vector Reserve team should return all the managed tokens to `VectorETH` before enabling redemptions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Vector Reserve |
| Report Date | N/A |
| Finders | Julio Aguilar, Mostafa Yassin, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/vector-reserve/68ff317c-7b13-4bdf-8245-9df1bc99f7cc/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/vector-reserve/68ff317c-7b13-4bdf-8245-9df1bc99f7cc/index.html

### Keywords for Search

`vulnerability`

