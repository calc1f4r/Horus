---
# Core Classification
protocol: Ithaca Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59741
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ithaca-finance/8cacdbf3-9f47-4135-854d-1d004abad065/index.html
source_link: https://certificate.quantstamp.com/full/ithaca-finance/8cacdbf3-9f47-4135-854d-1d004abad065/index.html
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Mustafa Hasan
  - Mostafa Yassin
  - Gelei Deng
---

## Vulnerability Title

Missing Token Validation in Withdraw Process

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `c7bcee49190cb724df3c1e37645f0aec2f06cfe6`.

**File(s) affected:**`contracts/fundlock/Fundlock.sol`

**Description:** In `Fundlock.sol`, the method `withdraw()` does not check whether the token is valid through `tokenValidator.validateToken()`. This means that the user can withdraw any token from the contract, even if it is not whitelisted. Since there is `removeTokenFromWhitelist()` method, this can be a potential issue as some tokens may not be intended to be withdrawn.

**Recommendation:** We recommend the team to consider adding the token validation in the `withdraw()` method if necessary.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ithaca Finance |
| Report Date | N/A |
| Finders | Mustafa Hasan, Mostafa Yassin, Gelei Deng |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ithaca-finance/8cacdbf3-9f47-4135-854d-1d004abad065/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ithaca-finance/8cacdbf3-9f47-4135-854d-1d004abad065/index.html

### Keywords for Search

`vulnerability`

