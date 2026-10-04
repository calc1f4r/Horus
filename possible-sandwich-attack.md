---
# Core Classification
protocol: Ember
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37890
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-20-Ember.md
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
  - Zokyo
---

## Vulnerability Title

Possible Sandwich Attack

### Overview


This bug report discusses a medium severity issue that has been resolved in a contract called EmberVault.sol. The function liquidateToken() in this contract can be exploited by MEV bots due to having no limits on slippage and deadline. This can result in unnecessary value being extracted from the protocol, which can harm users. The recommendation is to add reasonable limits on slippage and deadline to prevent this issue. The bug has been resolved in a recent commit by the client.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

In the contract EmberVualt.sol, the function liquidateToken() can be sandwich attacked due to having unlimited slippage and deadline. 

The code snippet above has zero and the max value of uint256 for slippage and deadline. This means that when liquidating a token, the token will take any amount against it. An MEV bot might pick this up and flashloan a trade against it to extract as much value as possible. This hurts the users of the protocol by extracting unnecessary value. 

**Recommendation**: 

Put a reasonable amount of slippage on the trade and do not allow for an infinite deadline. 

**Comment**: Client resolved the issue in commit: 609d6bff264c180b21fabd6a75e7658f6cb885f6

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Ember |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-20-Ember.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

