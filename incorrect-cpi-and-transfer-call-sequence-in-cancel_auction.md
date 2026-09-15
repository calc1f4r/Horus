---
# Core Classification
protocol: Gain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58486
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-22-Gain.md
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
  - zokyo
---

## Vulnerability Title

Incorrect CPI and transfer call sequence in `cancel_auction`.

### Overview


The team found a problem with cancelling auctions during testing. A runtime error called "UnbalancedInstruction" occurred because a transfer of lamports happened before all Cross-Program Invocations were finished. This prevented sellers from cancelling auctions where a bid had already been made. The recommended solution is to replace the close_account function and the 'if' block. This issue has been resolved after re-auditing.

### Original Finding Content

**Description**

During the testing phase, the team discovered an issue with the cancellation of the auction where the bid was placed. We received a runtime error "UnbalancedInstruction". It occurred because there is a transfer of lamports before all Cross-Program Invocations are finished. In this regard, the seller is deprived of the opportunity to cancel the auction, which has already made a bid.
Line. 75-92, programs/auction_house/src/methods/cancel_auction.rs, function 'handle'

**Recommendation**

Swap out the call to the close_account function and the 'if' block.

**Re-audit comment**

Resolved

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Gain |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-22-Gain.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

