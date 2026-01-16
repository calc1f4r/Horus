---
# Core Classification
protocol: Pstake
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55902
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-25-pStake.md
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

Evergrowing array:

### Overview


The report discusses a bug in a loop that allows users to unstake and withdraw tokens. The issue is that the array storing the unstaked amounts increases in length with each unstake, but does not decrease when the tokens are withdrawn. This can lead to a situation where the user is unable to withdraw their tokens after repeating the process multiple times. The recommendation is to use a counter variable to keep track of the index in the loop and prevent this issue from occurring.

### Original Finding Content

**Description**

![image](https://github.com/user-attachments/assets/22799dde-9c63-45cb-a343-838121160417)

The problem with this loop is that on every unStake() the user pushes a new unstake value to
the array increasing its length, but on withdrawUnstakedTokens() array’s length is not
decreased. If the user repeats the process of (stake -> unstake -> withdraw) some amount of
times, he would no longer be able to withdraw the tokens.

**Recommendation**:

Because the array grows only to its right, it would be helpful to have a counter variable
indicating from what index to start the loop. More precisely:

```solidity
mapping(address => uint256) internal _counters;
function withdrawUnstakedTokens() {
...
for (uint256 i = ; i < _unstakingExpiration[staker].length; i++) {
if (block.timestamp > _unstakingExpiration[staker][i]) {
_withdrawBalance =_withdrawBalance +
_unstakingAmount[staker][i];
_unstakingExpiration[staker][i] = 0;
_unstakingAmount[staker][i] = 0;
_counters[_msgSender()]++;
}
}
...
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Pstake |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-25-pStake.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

