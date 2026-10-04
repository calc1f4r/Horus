---
# Core Classification
protocol: Pulse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57719
audit_firm: Kann
contest_link: none
source_link: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/Pulse.md
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
  - Kann
---

## Vulnerability Title

[M-02] Constant Fee for Relayer

### Overview


This bug report addresses an issue with gas consumption on the chain, which may result in relayers paying more in gas fees than the rewards they receive. This can discourage relayer participation and make it difficult for new users to use the protocol. The recommendation is to implement a user-defined relayer fee or a dynamic gas fee function to address this issue. The team has responded that the issue has been fixed.

### Original Finding Content

## Severity

Medium Risk

## Description

Gas consumption on the chain could increase—either temporarily during high conges-
tion periods or permanently due to evolving network conditions. With the current fixed fee parame-
ters, relayers may not receive sufficient incentives to cover their gas expenses. In some cases, a relayer
might end up paying more in gas fees than the reward they receive. This imbalance not only discour-
ages relayer participation but also forces new addresses to source gas from elsewhere in order to call
the withdraw() function, which negatively impacts the protocol’s overall usability and efficiency.

## Recommendation

User-Defined Relayer Fee: Allow users to input a custom relayer fee when initi-
ating a transaction. This approach gives users the flexibility to determine what they consider a fair
incentive for the relayer, based on current network conditions and their own willingness to pay.
Dynamic Gas Fee Function: Alternatively, implement a function that can adjust the gas fee for relay-
ers. This function would allow the protocol administrator (or even potentially the community through
governance mechanisms) to update the relayer fee dynamically in response to changes in gas prices.
This ensures that the fee remains competitive and sufficient to cover relayer costs.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Kann |
| Protocol | Pulse |
| Report Date | N/A |
| Finders | Kann |

### Source Links

- **Source**: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/Pulse.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

