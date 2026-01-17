---
# Core Classification
protocol: Arkham Intel Exchange Bounty Contract
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60266
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/arkham-intel-exchange-bounty-contract/f86ecee0-d44f-48c3-80e9-e8570e2abadb/index.html
source_link: https://certificate.quantstamp.com/full/arkham-intel-exchange-bounty-contract/f86ecee0-d44f-48c3-80e9-e8570e2abadb/index.html
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
finders_count: 3
finders:
  - Shih-Hung Wang
  - Ibrahim Abouzied
  - Mostafa Yassin
---

## Vulnerability Title

Valid Submissions Are Not Refunded Their Full Stake Value

### Overview


The client has marked a bug as "Fixed" in the file `BountyV1.sol`. The bug was found in the function `approveSubmission()`, where the stake value was not being fully returned to the submitter. Instead, a fee was being taken from the stake along with the bounty amount. The bug has been fixed in commit `b5b04b152c4fdf421787571c2337495dfc0fd37c` and it is recommended to update the function to return the full stake value.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. The initial stake value is now refunded in full. Addressed in: `b5b04b152c4fdf421787571c2337495dfc0fd37c`.

**File(s) affected:**`BountyV1.sol`

**Description:** In `approveSubmission()`, the submission's stake is returned to the submitter. However, the `_takerFee` is extracted from the stake along with the bounty amount. The full stake value is not returned and is considered part of the bounty payout.

**Recommendation:** Update `approveSubmission()` such that the full stake value is returned.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Arkham Intel Exchange Bounty Contract |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Ibrahim Abouzied, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/arkham-intel-exchange-bounty-contract/f86ecee0-d44f-48c3-80e9-e8570e2abadb/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/arkham-intel-exchange-bounty-contract/f86ecee0-d44f-48c3-80e9-e8570e2abadb/index.html

### Keywords for Search

`vulnerability`

