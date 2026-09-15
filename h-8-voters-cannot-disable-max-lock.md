---
# Core Classification
protocol: Velocimeter
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36750
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/442
source_link: none
github_link: https://github.com/sherlock-audit/2024-06-velocimeter-judging/issues/257

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
finders_count: 11
finders:
  - 0xpiken
  - bughuntoor
  - bin2chen
  - HackTrace
  - pashap9990
---

## Vulnerability Title

H-8: voters cannot disable max lock

### Overview


This bug report discusses an issue where voters are unable to disable the maximum lock on their assets in the Velocimeter protocol. This means that their voting power will not decrease but they are unable to withdraw their assets. The report includes a detailed explanation of how the bug occurs and the impact it has on users. The code snippet and tool used for the review are also provided. The report recommends a code change to fix the bug and mentions that the protocol team has already addressed the issue in their code. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-06-velocimeter-judging/issues/257 

## Found by 
0xpiken, 1nc0gn170, Chinmay, HackTrace, Kirkeelee, bin2chen, bughuntoor, coffiasd, eeshenggoh, jovi, pashap9990
## Summary
Voters can enable maxLock and this causes their voting power wouldn't decrease but they cannot disable maxLock

## Vulnerability Detail
**Textual PoC:**
Let's assume three voters lock their assets in ve,hence three nfts will be minted[1,2,3] and after that they [enable maxLock](https://github.com/sherlock-audit/2024-06-velocimeter/blob/main/v4-contracts/contracts/VotingEscrow.sol#L883)

**Initial values**
max_locked_nfts corresponding values:



| index 0 | index 1 | index 2 |
| -------- | -------- | -------- |
| 1     | 2     | 3     |

maxLockIdToIndex corresponding values:

| index 1 | index 2 | index 3 |
| -------- | -------- | -------- |
| 1     | 2     | 3     |
 
 when owner of nft 3 want to disable maxLock he has to call `VotingEscrow::disable_max_lock`  in result :
**variable's values from line 897 til 901:**
* index = 2
* maxLockIdToIndex[3] = 0
* max_locked_nfts[2] = 3

max_locked_nfts corresponding values:



| index 0 | index 1 | index 2 |
| -------- | -------- | -------- |
| 1     | 2     | 3     |

maxLockIdToIndex corresponding values:

| index 1 | index 2 | index 3 |
| -------- | -------- | -------- |
| 1     | 2     | 0     |

finally
* maxLockIdToIndex[max_locked_nfts[2]] => maxLockIdToIndex[3] = 2 + 1
* last element of max_locked_nfts will be deleted

**Coded PoC:**

```solidity
    function testEnableAndDisableMaxLock() external {
        flowDaiPair.approve(address(escrow), TOKEN_1);
        uint256 lockDuration = 7 * 24 * 3600; // 1 week
        escrow.create_lock(400, lockDuration);
        escrow.create_lock(400, lockDuration);
        escrow.create_lock(400, lockDuration);

        assertEq(escrow.currentTokenId(), 3);
        escrow.enable_max_lock(1);
        escrow.enable_max_lock(2);
        escrow.enable_max_lock(3);


        assertEq(escrow.maxLockIdToIndex(1), 1);
        assertEq(escrow.maxLockIdToIndex(2), 2);
        assertEq(escrow.maxLockIdToIndex(3), 3);

        assertEq(escrow.max_locked_nfts(0), 1);
        assertEq(escrow.max_locked_nfts(1), 2);
        assertEq(escrow.max_locked_nfts(2), 3);

        escrow.disable_max_lock(3);

        assertEq(escrow.maxLockIdToIndex(1), 1);
        assertEq(escrow.maxLockIdToIndex(2), 2);
        assertEq(escrow.maxLockIdToIndex(3), 3);//mockLockIdToIndex has to be zero 

        assertEq(escrow.max_locked_nfts(0), 1);
        assertEq(escrow.max_locked_nfts(1), 2);
    }
```



## Impact
Voters cannot withdraw their assets from ve because every time they call `VotingEscrow::withdraw` their lockEnd will be decrease

## Code Snippet
https://github.com/sherlock-audit/2024-06-velocimeter/blob/main/v4-contracts/contracts/VotingEscrow.sol#L904

## Tool used

Manual Review

## Recommendation
```diff
    function disable_max_lock(uint _tokenId) external {
        assert(_isApprovedOrOwner(msg.sender, _tokenId));
        require(maxLockIdToIndex[_tokenId] != 0,"disabled");

        uint index =  maxLockIdToIndex[_tokenId] - 1;
        maxLockIdToIndex[_tokenId] = 0;

         // Move the last element into the place to delete
        max_locked_nfts[index] = max_locked_nfts[max_locked_nfts.length - 1];

+         if (index != max_locked_nfts.length - 1) {
+             uint lastTokenId = max_locked_nfts[max_locked_nfts.length - 1];
+             max_locked_nfts[index] = lastTokenId;
+             maxLockIdToIndex[lastTokenId] = index + 1;
+         }
        
+         maxLockIdToIndex[max_locked_nfts[index]] = 0;
        

-       maxLockIdToIndex[max_locked_nfts[index]] = index + 1;//@audit maxLockIdToIndex computes wrongly when lps want to disable last element in array
        
        // Remove the last element
        max_locked_nfts.pop();
    }
```




## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/Velocimeter/v4-contracts/pull/12

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Velocimeter |
| Report Date | N/A |
| Finders | 0xpiken, bughuntoor, bin2chen, HackTrace, pashap9990, 1nc0gn170, jovi, coffiasd, Chinmay, eeshenggoh, Kirkeelee |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-06-velocimeter-judging/issues/257
- **Contest**: https://app.sherlock.xyz/audits/contests/442

### Keywords for Search

`vulnerability`

