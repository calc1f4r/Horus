---
# Core Classification
protocol: Rollie
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35483
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-16-Rollie.md
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

`userLastDepositTime` can be enforced without user's consent

### Overview


The bug report discusses an issue in the TradingVault.sol function `deposit()`, where a caller can deposit a small amount of `standardToken` for a user and prevent them from withdrawing their deposits. This can be considered a denial of service attack on the user. The report recommends implementing a minimum deposit requirement and carefully selecting and vetting allowed callers. The issue has been addressed in a recent commit, but there is still a concern about the list of allowed depositors and the potential for collusion between an allowed depositor and a user. Additionally, there is a potential issue with the `userLastDepositTime` timeframe not accurately reflecting the user's deposit in certain scenarios. The client has committed to reviewing all permissions granted for staking and ensuring they are thoroughly validated.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Location**: TradingVault.sol

**Description**

In function `deposit(uint256 _amount, address _user)`, caller can deposit `_amount` of `standardToken` for `_user` and update `userLastDepositTime` for that user. The mapping `userLastDepositTime` limits the user from withdrawing the deposits.
```solidity
userLastDepositTime[user] = block.timestamp;
```
Caller `msg.sender` can deposit dust amounts (i.e. 1 wei) in order to block user from withdrawing which can be considered a denial of service being imposed on that user from doing withdrawal operations.

**Recommendation** 

The following strategies can be implemented to address the issue:

Implementing a minimum deposit requirement can serve as a deterrent to potential attackers.
It is important to carefully select and vet allowed callers, particularly those listed in the allowed mapping (i.e. no code change required). 

**Fix** - Finding is addressed in commit fdfa146 ,  the instruction:   `userLastDepositTime[user] = block.timestamp;`    is only executed when caller is not among the list of privileged allowed depositors.  Therefore the timestamp update can not be imposed on the user. However the list of allowed depositors still require careful vetting to avoid a scenario in which allowed depositor conspires with a user to give advantage to the user to deposit without any time constraint to stay locked in the protocol. 
                    
An important issue arises when the user have no deposit and the allowed depositor is depositing for them for the first time. In this case we have  `userLastDepositTime[_user] = 0;`    which gives a misleading piece of information about the user’s deposit. If rewards are distributed based on the locking time here from another protocol this can be critical.  

In response to the identified issue, the client provided clarification regarding the purpose of the specified timeframe `userLastDepositTime`. They affirmed that this timeframe is not directly associated with rewarding users but rather serves as a mechanism to prevent malicious staking and withdrawal activities. Additionally, the client committed to conducting a comprehensive review of each permission granted for staking, emphasizing the importance of understanding and validating these permissions thoroughly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Rollie |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-16-Rollie.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

