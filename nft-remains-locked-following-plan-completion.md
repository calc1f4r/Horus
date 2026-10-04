---
# Core Classification
protocol: Cyan
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59445
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/cyan/5ef87add-ca0f-43eb-b6bb-758ec81a7e85/index.html
source_link: https://certificate.quantstamp.com/full/cyan/5ef87add-ca0f-43eb-b6bb-758ec81a7e85/index.html
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
  - Jennifer Wu
  - Ibrahim Abouzied
  - Jonathan Mevs
---

## Vulnerability Title

NFT Remains Locked Following Plan Completion

### Overview


The client has marked a bug as "Fixed" in the file `CyanPeerPlan.sol`. The bug caused an NFT to remain locked even after completing a plan during a revival. This issue can be resolved by unlocking the NFT immediately after the plan is completed in the `CyanPeerPlan.revive()` function. 

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `064b6987653c92bfb428a2931be7893cfe1900df`.

The NFT is now unlocked if the plan is being completed during a revival.

**File(s) affected:**`CyanPeerPlan.sol`

**Description:** In `CyanPeerPlan.revive()`, if a plan is being completed, the `_paymentPlan.status` is set to `PlanStatus.COMPLETED` , despite the NFT remaining locked. Although an Operator address could manually unlock the NFT following the revival & completion of a Peer Plan, this NFT should be unlocked immediately following the plan completion.

**Recommendation:** In `CyanPeerPlan.revive()`, unlock the NFT whose plan is being completed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Cyan |
| Report Date | N/A |
| Finders | Jennifer Wu, Ibrahim Abouzied, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/cyan/5ef87add-ca0f-43eb-b6bb-758ec81a7e85/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/cyan/5ef87add-ca0f-43eb-b6bb-758ec81a7e85/index.html

### Keywords for Search

`vulnerability`

