---
# Core Classification
protocol: Radiant Capital
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56438
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant Capital.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Owner is able to withdraw staking token.

### Overview


The bug report is about a function called recoverERC20() in a contract called MultiFee Distribution.sol. This function allows the owner of the contract to access and withdraw tokens from users' funds. However, this poses a risk as the owner could potentially exploit this function and take all the tokens. To prevent this, it is recommended to add a validation check to ensure that the token being withdrawn is not a staking token. This validation check has been added in the function. Additionally, the function has been removed after an audit was conducted.

### Original Finding Content

**Description**

MultiFee Distribution.sol: recoverERC20(). 
The owner can directly access users' funds and withdraw their tokens anytime since the owner can't recover only reward tokens. As a result, in the case of the private key exploit (of an owner account), users' funds can be withdrawn directly from the contract. That's why it is recommended to validate that the provided 'tokenAddress is not a staking token, in order to exclude a centralization risk. 

**Recommendation**: 

Validate that 'tokenAddress' is not a staking token in the function. 

**Post-audit**. 

Function recoverERC20() was removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Radiant Capital |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant Capital.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

