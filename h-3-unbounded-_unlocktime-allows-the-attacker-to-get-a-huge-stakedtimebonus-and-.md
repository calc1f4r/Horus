---
# Core Classification
protocol: FrankenDAO
chain: everychain
category: uncategorized
vulnerability_type: min/max_cap_validation

# Attack Vector Details
attack_type: min/max_cap_validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3591
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/18
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/53

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - min/max_cap_validation

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - launchpad
  - payments

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - curiousapple
  - bin2chen
  - koxuan
  - WATCHPUG
  - Trumpero
---

## Vulnerability Title

H-3: Unbounded `_unlockTime` allows the attacker to get a huge `stakedTimeBonus` and dominate the voting

### Overview


This bug report concerns a vulnerability in the code of the FrankenDAO project, which was found by Trumpero, WATCHPUG, neumo, bin2chen, curiousapple, koxuan, John, and hansfriese. The vulnerability is that there is no maximum `_unlockTime` check in the `_stakeToken()` function, which allows an attacker to set a large value for `_unlockTime` and obtain an excessively big `stakedTimeBonus`. This would allow the attacker to gain a large number of votes and dominate the voting. The code snippet provided shows the code that needs to be changed to fix this vulnerability. A Pull Request was created by zobront, which fixed the issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/53 

## Found by 
Trumpero, WATCHPUG, neumo, bin2chen, curiousapple, koxuan, John, hansfriese

## Summary

`stakingSettings.maxStakeBonusTime` is not enforced, allowing the attacker to gain a huge `stakedTimeBonus` by using a huge value for `_unlockTime`.

## Vulnerability Detail

There is no max `_unlockTime` check in `_stakeToken()` to enforce the `stakingSettings.maxStakeBonusTime`.

As a result, an attacker can set a huge value for `_unlockTime` and get an enormous `stakedTimeBonus`.

## Impact

The attacker can get a huge amount of votes and dominate the voting.

## Code Snippet

https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Staking.sol#L389-L394

https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Staking.sol#L356-L384

## Tool used

Manual Review

## Recommendation

Change to:

```solidity
  function _stakeToken(uint _tokenId, uint _unlockTime) internal returns (uint) {
    if (_unlockTime > 0) {
      unlockTime[_tokenId] = _unlockTime;
      uint time = _unlockTime - block.timestamp;
      uint maxtime = stakingSettings.maxStakeBonusTime;
      uint maxBonus = stakingSettings.maxStakeBonusAmount;
      if (time < stakingSettings.maxStakeBonusTime){
        uint fullStakedTimeBonus = (time * maxBonus) / maxtime;
      }else{
        uint fullStakedTimeBonus = maxBonus;
      }
      stakedTimeBonus[_tokenId] = _tokenId < 10000 ? fullStakedTimeBonus : fullStakedTimeBonus / 2;
    }
```

## Discussion

**zobront**

Fixed: https://github.com/Solidity-Guild/FrankenDAO/pull/13

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | FrankenDAO |
| Report Date | N/A |
| Finders | curiousapple, bin2chen, koxuan, WATCHPUG, Trumpero, John, hansfriese, neumo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/53
- **Contest**: https://app.sherlock.xyz/audits/contests/18

### Keywords for Search

`Min/Max Cap Validation`

