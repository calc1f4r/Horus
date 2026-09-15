---
# Core Classification
protocol: Beanstalk Bip
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31281
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-12-05-cyfrin-beanstalk-bip-39.md
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
  - Dacian
  - Giovanni Di Siena
  - Carlos Amarante
---

## Vulnerability Title

Missing validation in `LibWhitelist::verifyTokenInLibWhitelistedTokens`

### Overview

See description below for full details.

### Original Finding Content

**Description:** Prior to the introduction of [`LibWhitelistedToken.sol`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibWhitelistedTokens.sol), Beanstalk did not have a way of iterating through its whitelisted tokens. To mitigate against an upgrade where a new asset is whitelisted, but `LibWhitelistedToken.sol` is not updated, [`LibWhitelist::verifyTokenInLibWhitelistedTokens`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibWhitelist.sol#L196-L217) verifies that the token is both in the correct array(s) and not in invalid arrays.

While `LibWhitelistedTokens::getWhitelistedWellLpTokens` is supposed to return a subset of whitelisted LP tokens, this is not guaranteed. In this case, if the token is either Bean or an Unripe Token, the first `else` block within `LibWhitelist::verifyTokenInLibWhitelistedTokens` should also check that the token is not in the whitelisted Well LP token array.

**Recommended Mitigation:**
```diff
} else {
    checkTokenNotInArray(token, LibWhitelistedTokens.getWhitelistedLpTokens());
+   checkTokenNotInArray(token, LibWhitelistedTokens.getWhitelistedWellLpTokens());
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Beanstalk Bip |
| Report Date | N/A |
| Finders | Dacian, Giovanni Di Siena, Carlos Amarante |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-12-05-cyfrin-beanstalk-bip-39.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

