---
# Core Classification
protocol: Accountable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62981
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
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

protocol_categories:
  - options_vault
  - liquidity_manager
  - insurance
  - uncollateralized_lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Immeas
  - Chinmay
  - Alexzoid
---

## Vulnerability Title

Borrower in OpenTerm loan can stay delinquent effectively forever

### Overview


The report highlights a bug in the lending protocol where borrowers can avoid late penalties by briefly restoring their liquidity before the grace period expires. This allows them to remain delinquent indefinitely without incurring any penalties, which can harm lenders. The recommended solution is to either remove the grace period entirely or redesign it to be cumulative. The team responsible for the protocol will acknowledge the bug, but there is currently no clear plan on how to address it. This bug is due to the design of the protocol, where borrow/repay actions are not frequent and can come with a reputational cost.

### Original Finding Content

**Description:** Delinquency is flagged when vault reserves fall below `_calculateRequiredLiquidity()`, setting `delinquencyStartTime`. Late penalties only accrue after the grace period elapses. If the borrower briefly restores liquidity (e.g., `supply()`/`repay()`) before grace expiry, delinquency is cleared and `delinquencyStartTime` resets to 0. The borrower can immediately `borrow()` again to drop reserves to the threshold and the next block, when interest has accrued again, start a fresh grace window. This “pulse” can be executed back-to-back, even within one block, allowing the borrower to remain effectively delinquent indefinitely without ever incurring penalties.

**Impact:** Borrowers can avoid late penalties while keeping lenders under-reserved, degrading lender protections.

**Recommended Mitigation:** Consider removing the grace period entirely so penalties accrue as soon as the loan becomes delinquent. This would reduce complexity and be in line with how a lot of other lending protocols work.

Alternatively consider redesigning the grace period to be cumulative, i.e. A year loan has a cumulative 1 week grace period which the borrower can draw from.

**Accountable:** We will acknowledge this. We don't have an actionable path on how loans are managed when it comes to penalties grace periods or even whether penalties are enabled or not. Having a considerable grace period is by design and as a fallback a manager can always initiate a default. In most use-cases borrow/repay actions won't be very often and given these entities deploy funds to other venues, also off-chain, doing such actions can come with a reputational cost.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Accountable |
| Report Date | N/A |
| Finders | Immeas, Chinmay, Alexzoid |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

