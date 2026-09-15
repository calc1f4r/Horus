---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44901
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-30-Vaultka.md
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

Users Might Receive Undesired Tokens In fullfilledRequestSwap

### Overview


This bug report describes a medium severity bug that has been resolved. The bug involved a user closing their position and not wanting to withdraw in a specific currency, causing their withdrawal amount to be set incorrectly. An attacker could exploit this by calling a function with a volatile or meme coin, causing the user to receive a currency that could quickly lose value. The recommendation is to add a check to ensure the user is the one making the request. The bug has been fixed in the latest commit. 

### Original Finding Content

**Severity** : Medium

**Status** : Resolved 

**Description**

Say a user closed his position (closePosition() in SakeVaultV2.sol) and does not want to withdraw in USDC. 
`closePositionAmount[_user][_positionID] = amountAfterFee;` and `closePositionRequest[_user][_positionID] = true;` would be set in this case.
Now imagine, me as an attacker call `fulfilledRequestSwap` at L744 but with `_outputAsset` as a token which is pretty volatile or in extreme conditions a meme coin, whereas the user wanted to swap to a more stable coin (all whitelisted).

The user gets his withdraw amount in an asset which might lose value quickly and is highly intended.

**Recommendation** 

Ensure this check on the function ->
```solidity
UserInfo storage _userInfo = userInfo[_user][_positionID];
require(msg.sender == _userInfo.user)
```

**Comment**: Client fixed the following issue in commit: 7d32cf53cebcb6c81bc4755bbfd6befe4ac8522b

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-30-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

