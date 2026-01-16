---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1012
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/229

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hack3r-0m
  - pauliax
---

## Vulnerability Title

[H-27] Unrestricted vestFor

### Overview


This bug report concerns a vulnerability in the function vestFor, which allows anyone to block any user with a tiny amount of Vader. This function has no authentication checks, meaning that malicious actors can use it to front-run legitimate vestFor calls. The result of this vulnerability is that users can be locked out for 365 days, preventing them from converting their tokens. 

The recommended mitigation step is to introduce a whitelist of callers that can vest on behalf of others, such as Converter. This would allow legitimate users to convert their tokens while preventing malicious actors from taking advantage of the vulnerability.

### Original Finding Content

_Submitted by pauliax, also found by hack3r-0m_

#### Impact

Anyone can call function `vestFor` and block any user with a tiny amount of Vader. This function has no auth checks so a malicious actor can front-run legit `vestFor` calls with insignificant amounts. This function locks the user for 365 days and does not allow updating the value, thus forbids legit conversions.

#### Recommended Mitigation Steps

Consider introducing a whitelist of callers that can vest on behalf of others (e.g. Converter).

**[SamSteinGG (Vader) confirmed](https://github.com/code-423n4/2021-11-vader-findings/issues/229)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | hack3r-0m, pauliax |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/229
- **Contest**: https://code4rena.com/contests/2021-11-vader-protocol-contest

### Keywords for Search

`vulnerability`

