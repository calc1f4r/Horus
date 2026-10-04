---
# Core Classification
protocol: EVAA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59119
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/evaa/df7aa699-793b-49f7-b348-1f78e9ca9870/index.html
source_link: https://certificate.quantstamp.com/full/evaa/df7aa699-793b-49f7-b348-1f78e9ca9870/index.html
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
  - Gereon Mendler
  - Julio Aguilar
  - Valerian Callens
---

## Vulnerability Title

Possible Unfair Race Conditions Between Borrowers and Liquidators when the System Is Activated Again

### Overview


This bug report explains that there is an issue with the master contract in a system that allows users to borrow and lend money. The problem is that if the system is temporarily disabled and then reactivated, there is a chance that some users may lose their borrowed money because of a race between borrowers and liquidators. The client suggests adding a delay in the system to give borrowers a chance to add more collateral before liquidation occurs. 

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> We mitigate this on the process level: before update we warn in advance users to take action for securing their positions against volatility

**File(s) affected:**`master-storage.fc`

**Description:** It is possible for the admin via the functions `update_dynamics_process()`, `disable_contract_for_upgrade_process()`, `force_enable_process()` and `cancel_upgrade_process()` to disable or enable the master contract. If the protocol is temporarily disabled with active positions, these positions could become liquidable and, when the protocol is set back to active, a race condition will happen between borrowers who want to send back more collateral and liquidators who want to liquidate these users, which seems unfair for borrowers who were not able to do that earlier because protocol operations were disabled.

**Recommendation:** Consider adding a period when the system is activated again to delay the liquidations but make it possible instantly to supply more collateral to favor depositors over liquidators.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | EVAA |
| Report Date | N/A |
| Finders | Gereon Mendler, Julio Aguilar, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/evaa/df7aa699-793b-49f7-b348-1f78e9ca9870/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/evaa/df7aa699-793b-49f7-b348-1f78e9ca9870/index.html

### Keywords for Search

`vulnerability`

