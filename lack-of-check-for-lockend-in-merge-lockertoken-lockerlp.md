---
# Core Classification
protocol: ZeroLend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38289
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/zerolend-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/ZeroLend/28885%20-%20%5bSC%20-%20Medium%5d%20Lack%20of%20check%20for%20Lockend%20in%20merge%20LockerToken%20....md

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
  - offside0011
---

## Vulnerability Title

Lack of check for Lock.end in merge LockerToken && LockerLp

### Overview


The bug report is about a vulnerability in the governance smart contract of a project called ZeroLend. This vulnerability allows an attacker to manipulate the voting results in the governance system, resulting in a change from the intended outcome. The vulnerability occurs when two Locker NFTs are merged, and the resulting NFT has a time range that exceeds the preset maximum time, increasing its locking power. The issue lies in the lack of strict restrictions on the start and end times of the NFTs, which allows an attacker to manipulate the final NFT's time span. This amplifies the NFT's power in the governance system, giving the attacker an advantage in voting. The report includes a proof of concept and references to the affected code in the project's GitHub repository. 

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/zerolend/governance

Impacts:
- Manipulation of governance voting result deviating from voted outcome and resulting in a direct change from intended effect of original results

## Description
## Brief/Intro
When merging two Locker NFTs, there were no strict restrictions on the start and end times of the two NFTs. This resulted in the final merged NFT having a time range that exceeded the preset maximum time, consequently increasing the locking power.

## Vulnerability Details
In the file BaseLocker.sol, the maximum time that an NFT can be set is externally passed in. For LockerToken, it is set as 4 * 365 * 86400, and for LockerLP, it is 365 * 86400. The staking duration is crucial for the final power calculation. In the _calculatePower function, the formula is ((lock.end - lock.start) * lock.amount) / MAXTIME;. Therefore, there are strict restrictions in both the _createLock and increaseUnlockTime functions to ensure that the time span(lock.end - lock.start) of an NFT does not exceed MAXTIME.


In the merge function, two NFTs can be combined, and the end time is selected from the later time of the two NFTs. In the _depositFor function, there is no further check on the time span. 

Taking LockerLP as an example, suppose an attacker initially stakes an NFT (NFT1) for 1 year, then, after a month, stakes another NFT (NFT2) for 1 year. The attacker then calls the merge function, 
```
merge(NFT2, NFT1);
```
In the merge function, 
```
uint256 end = _locked0.end >= _locked1.end
    ? _locked0.end
    : _locked1.end;
```
selects the time of the later NFT and assigns it to the second parameter "to", which is NFT1. At this point, the final NFT has a start of NFT1's start and an end of NFT2's end, resulting in a time span of 1 year and 1 month. In the final calculation of _calculatePower, the returned formula is 
```
function _calculatePower(
    LockedBalance memory lock
) internal view returns (uint256) {
     return ((lock.end - lock.start) * lock.amount) / MAXTIME;
}
```
, which amplifies the nft's Power.

## Impact Details
Amplifying the power of a locker in the governance

## References
https://github.com/zerolend/governance/blob/main/contracts/locker/BaseLocker.sol#L183



## Proof of Concept (Take LockerLP as Example)
1. call createLockFor, _lockDuration = 4 * 365 * 86400 return nftid=1
2. vm.wrap(block.timestamp + 86400 * 30)
3. call createLockFor, _lockDuration = 4 * 365 * 86400 return nftid=2
4. merge(2, 1)# 2 is burned and locker(1).end = locker(2).end

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | ZeroLend |
| Report Date | N/A |
| Finders | offside0011 |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/ZeroLend/28885%20-%20%5bSC%20-%20Medium%5d%20Lack%20of%20check%20for%20Lockend%20in%20merge%20LockerToken%20....md
- **Contest**: https://immunefi.com/bounty/zerolend-boost/

### Keywords for Search

`vulnerability`

