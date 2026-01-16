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
solodit_id: 53847
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

[M-07] Ticking Interest Rate opens up to multi-block MEV - Directly Triggering Recovery Mode on the next block due to interest ticking

### Overview


The bug report discusses a potential vulnerability in the Apollon platform that could allow an attacker to trigger Recovery Mode and liquidate Troves that are below the TCR (Total Collateral Ratio). This could result in significant losses for users who have borrowed money on the platform. The report suggests several ways to mitigate this risk, such as enforcing a buffer for opening positions, changing the mechanisms around Recovery Mode, or introducing a delay for liquidations. However, these solutions may have downsides and require further economic modeling. Overall, the report highlights the need for addressing this vulnerability to protect users leveraging their positions on the Apollon platform.

### Original Finding Content

**Impact**

Because Apollon charges an interest on borrowing, an attack can guarantee triggering Recovery Mode on the next block by simply borrowing up to the threshold

Triggering Recovery mode would then allow liquidating Troves that are below the TCR

This puts the attacker at risk as well, however with some setup the attack can be +EV, posing a close to unmitigatable risk to other Trove owners


**Mitigation**

Recovery Mode liquidations being too easily accessible is a big risk for users leveraging up

In order to avoid this you could opt-into:
1) Enforcing a Buffer for Opening Positions
- This unfortunately has the downside of allowing the triggering of Recovery Mode via multiple positions

2) Changing the mechanisms around how Recovery Mode works
- This requires extensive work, possible solutions can be: Increasing the fee as you open a Trove that brings the sytem towards recovery mode (Make the attack economically expensive)

3) Remove or Alter the logic for Recovery Mode by enforcing higher Liquidations
- This requires economic modelling

4) Introduce a Delay for Recovery Mode Liquidations like we did in eBTC
- This doesn't remove the risk but reduces it and makes the attack more expensive

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

