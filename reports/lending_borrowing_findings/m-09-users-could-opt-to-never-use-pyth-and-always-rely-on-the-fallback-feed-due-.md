---
# Core Classification
protocol: Apollon Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53849
audit_firm: Recon Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-22-Apollon_Report.md
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
  - Alex The Entreprenerd
---

## Vulnerability Title

[M-09] Users could opt to never use Pyth and always rely on the fallback feed due to lack of validation on certain functions

### Overview


This bug report discusses an issue with using the Pyth and Fallback oracles. When Pyth is unavailable, users are given the option to choose between Pyth and the fallback oracle. However, the fallback oracle is not always updated, which creates opportunities for arbitrage. This can lead to issues with redemptions and increasing debts. To mitigate this, the report suggests rethinking the FSM (finite state machine) and considering changing fees based on the oracle being used. It also recommends implementing an oracle deviation threshold and time to update to prevent arbitrage. The report suggests changing fees based on the oracle being used, with Pyth having a lower fee and the fallback oracle charging a higher fee. 

### Original Finding Content

**Impact**

The rationale for using Pyth and the Fallback oracle is logical:
Sometimes Pyth is unavailable

However, once Pyth becomes unavailable, people will have the option to constantly chose between Pyth and the fallback oracle

The fallback oracle is a push type oracle, meaning that it won't always be updated

This may create opportunity for arbitrage for:
- Redemptions
- Increasing Debts (as other account debts will not have their prices checked for staleness)

**Mitigation**

Overall you should rethink the FSM around how stale vs trusted prices could be used as the current implementation opens up for a lot of arbitrage and edge cases

You should consider changing fees based on the oracle you're using

An oracle deviation threshold + time to update are inherently +EV to arbitrageurs
You should consider changing fees based on which oracle is being used, where Pyth could have a lower fee and the fallback would most likely have to charge a higher fee

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Recon Audits |
| Protocol | Apollon Report |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-22-Apollon_Report.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

