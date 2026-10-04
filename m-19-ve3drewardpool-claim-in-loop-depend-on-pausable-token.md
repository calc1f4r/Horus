---
# Core Classification
protocol: veToken Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6140
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-vetoken-finance-contest
source_link: https://code4rena.com/reports/2022-05-vetoken
github_link: https://github.com/code-423n4/2022-05-vetoken-findings/issues/166

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

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - VAD37
---

## Vulnerability Title

[M-19] `VE3DRewardPool` claim in loop depend on pausable token

### Overview


A bug has been identified in the veToken project, which is a generalized version of Convex for non-Curve tokens. Currently, all ve3Token rewards are bundled together inside `ve3DLocker` and `ve3DRewardPool` into a single contract. This is a problem because if one of the tokens has a pausable transfer, users cannot claim their rewards or withdraw them if they have multiple rewards including the paused token. This is because the `IERC20.transfer` function is blocked. 

An example of this is the Ribbon token which has a pausable transfer controlled by the Ribbon DAO. Normally, this would not be an issue in Convex where only a few pools would be affected by a single coin. However, since veAsset are bundled together into a single reward pool, it becomes a major problem.

The recommended mitigation step is to have a second `getReward()` function which accepts an array of tokens that can be interacted with. This would save gas and only require some extra work on the frontend website, instead of the current implementation of withdrawing all tokens bundled together.

### Original Finding Content

_Submitted by VAD37_

<https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/contracts/VE3DRewardPool.sol#L296-L299>

<https://github.com/code-423n4/2022-05-vetoken/blob/1be2f03670e407908f175c08cf8cc0ce96c55baf/contracts/VeAssetDepositor.sol#L134-L152>

### Vulnerability Details

Project veToken is supposed to be a generalized version of Convex for non-Curve token.
There is only one contract for all rewards token in the platform.

All ve3Token rewards are bundled together inside `ve3DLocker` and `ve3DRewardPool` in a loop. Instead of having its own unique contract like `VeAssetDepositer` or `VoterProxy` for each token.

### Impact

If one token has pausable transfer, user cannot claim rewards or withdraw if they have multiple rewards include that pause token.

Right now the project intends to support only 6 tokens, including Ribbon token which has [pausable transfer](https://etherscan.io/address/0x6123b0049f904d730db3c36a31167d9d4121fa6b#code#L810) controlled by Ribbon DAO.

Normally, this would not be an issue in Convex where only a few pools would be affected by single coin. Since, veAsset are bundled together into single reward pool, it becomes a major problem.

### Proof of Concept

*   Token like Ribbon pause token transfer by DAO due to an unfortunate event.
*   `VE3DRewardPool` try call `getReward()`, `VeAssetDepositor` [try deposit token from earned rewards](https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/contracts/VE3DRewardPool.sol#L296-L299) does not work anymore because `IERC20.transfer` [is blocked](https://github.com/code-423n4/2022-05-vetoken/blob/1be2f03670e407908f175c08cf8cc0ce96c55baf/contracts/VeAssetDepositor.sol#L134-L152). This effectively reverts current function if user have this token reward > 0.

### Recommended Mitigation Steps

It would be a better practice if we had a second `getReward()` function that accepts an array of token that we would like to interact with.

It saves gas and only requires some extra work on frontend website.
Instead of current implementation, withdraw all token bundles together.

**[solvetony (veToken Finance) confirmed and commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/166#issuecomment-1156706193):**
 > It might happen rarely, but we might fix that.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/166#issuecomment-1194847379):**
 > The warden has shown how, in certain cases, because a reward token could be pausable, this can cause the entire claim process to break as `getReward` doesn't allow the caller to specify which tokens to receive.
> 
> I have to agree that the odds are low, however the finding is valid and because it's reliant on external conditions I believe Medium Severity to be appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | veToken Finance |
| Report Date | N/A |
| Finders | VAD37 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-vetoken
- **GitHub**: https://github.com/code-423n4/2022-05-vetoken-findings/issues/166
- **Contest**: https://code4rena.com/contests/2022-05-vetoken-finance-contest

### Keywords for Search

`vulnerability`

