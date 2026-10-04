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
solodit_id: 56442
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant Capital.md
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

Staking and withdrawal operations might be blocked.

### Overview


The bug report discusses a problem with the MultiFee Distribution contract, specifically in the functions for staking and withdrawing funds. The issue lies in the contract's interaction with other contracts, specifically the Disqualifier and ChefIncentivesController contracts. These contracts have "require" statements that can block the staking and withdrawing of tokens. The recommendation is to not revert the entire transaction if these statements are triggered, but instead claim a bounty for the affected user before completing the transaction. The team has since removed some validations, but it is important to claim a bounty for ineligible users before staking or withdrawing.

### Original Finding Content

**Description**

MultiFee Distribution.sol: _stake(), line 644,_withdrawExpiredLocks For(), line 1134. 
During staking and withdrawing funds, a 'beforeLockUpdate hook is called on the Incentives Controller. This hook checks if a user is to be disqualified. For this purpose, the contract performs another external call to Disqualifier.sol, function processUser(). Inside this function, the contract calls an internal function of Disqualifier, _processUserWithBounty(). It has a "require" which will revert if the storage variable 'DISABLED' is set to true. Thus due to this statement on Disqualifier.sol, staking and withdrawing of tokens on MultiFee Distribution.sol might be blocked. 
Further, in_processUserWithBounty(), an external call is performed to ChefIncentivesController.disqualifyUser(), where there are two checks which can also block the operations (Lines 489, 491). 

**Recommendation**: 

Do not revert a whole stake or withdraw transaction due to require statements in the Disqualifier.sol and ChefIncentives Controller.sol. 

**Post-audit**: 

The team removed validations that might prevent staking and withdrawing. However, if a certain user is ineligible for rewards, a bounty should be claimed for him before staking or withdrawing.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

