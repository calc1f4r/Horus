---
# Core Classification
protocol: Backend / Frontend Whitebox
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51048
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/truffles/backend-frontend-whitebox-webapp-pentest
source_link: https://www.halborn.com/audits/truffles/backend-frontend-whitebox-webapp-pentest
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
  - Halborn
---

## Vulnerability Title

PRIVATE ACCESS TOKEN IN URL

### Overview


This bug report discusses a potential issue with sensitive information being exposed in URLs. This can happen when users share or save URLs, and it puts them at risk of being accessed by attackers. The severity of this issue is rated as Impact: 4 and Likelihood: 2. A solution is currently being worked on and will be implemented in a future release.

### Original Finding Content

##### Description

Sensitive information within URLs may be logged in various locations, including the user's browser, the web server and any forward or reverse proxy servers between the two endpoints. URLs may also be displayed on-screen, bookmarked or emailed around by users. Placing secrets into the URL increases the risk that they will be captured by an attacker.

![token-url.png](https://halbornmainframe.com/proxy/audits/images/659ef547a1aa3698c0f13de8)

* [CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N)

##### Score

Impact: 4  
Likelihood: 2

##### Recommendation

**PENDING**: Truffles will implement the solution in a future release.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Backend / Frontend Whitebox |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/truffles/backend-frontend-whitebox-webapp-pentest
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/truffles/backend-frontend-whitebox-webapp-pentest

### Keywords for Search

`vulnerability`

