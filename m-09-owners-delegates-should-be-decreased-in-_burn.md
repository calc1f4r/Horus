---
# Core Classification
protocol: Velodrome Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24772
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-05-velodrome
source_link: https://code4rena.com/reports/2022-05-velodrome
github_link: https://github.com/code-423n4/2022-05-velodrome-findings/issues/153

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
  - services
  - yield_aggregator
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-09] Owner's delegates should be decreased in `_burn()`

### Overview


This bug report is about the VotingEscrow contract in the Velodrome project. The problem is that when the function _burn is called, the dstRep array won't get decreased, which opens a griefing attack vector. An attacker can deposit 1 wei of token for the victim, repeated for MAX_DELEGATES times, and the victim can no longer deposit, even if they try to merge or burn their tokenIds. This can also be a problem for regular users, as the dstRep array will continuously grow and can't decrease, eventually reaching the MAX_DELEGATES cap and preventing them from depositing.

The recommendation to solve this issue is to add _moveTokenDelegates(delegates(_to), address(0), _tokenId); to the _burn function. This has been acknowledged by pooltypes (Velodrome) and commented on by Alex the Entreprenerd (judge).

### Original Finding Content

_Submitted by WatchPug_

[VotingEscrow.sol#L517-L528](https://github.com/code-423n4/2022-05-velodrome/blob/7fda97c570b758bbfa7dd6724a336c43d4041740/contracts/contracts/VotingEscrow.sol#L517-L528)<br>

```solidity
function _burn(uint _tokenId) internal {
    require(_isApprovedOrOwner(msg.sender, _tokenId), "caller is not owner nor approved");

    address owner = ownerOf(_tokenId);

    // Clear approval
    approve(address(0), _tokenId);
    // TODO add delegates
    // Remove token
    _removeTokenFrom(msg.sender, _tokenId);
    emit Transfer(owner, address(0), _tokenId);
}
```

[VotingEscrow.sol#L1244-L1248](https://github.com/code-423n4/2022-05-velodrome/blob/7fda97c570b758bbfa7dd6724a336c43d4041740/contracts/contracts/VotingEscrow.sol#L1244-L1248)<br>

```solidity
// All the same plus _tokenId
require(
    dstRepOld.length + 1 <= MAX_DELEGATES,
    "dstRep would have too many tokenIds"
);
```

When `_moveTokenDelegates()`, `dstRep` must not have more than `MAX_DELEGATES`.

However, in `_burn()`, `dstRep` array wont get decreased. This opens a griefing attack vector, in which the attacker can deposit 1 wei of token for the victim, repeated for `MAX_DELEGATES` times, and the victim can no longer deposit, even if they try to merge or burn their tokenIds.

Even for a normal active user, this can be a problem as the `dstRep` array will continuously grow and cant decrease, one day the user won't be able to deposit anymore as they have reached the `MAX_DELEGATES` cap.

### Recommendation

Change to:

```solidity
function _burn(uint _tokenId) internal {
    require(_isApprovedOrOwner(msg.sender, _tokenId), "caller is not owner nor approved");

    address owner = ownerOf(_tokenId);

    // Clear approval
    approve(address(0), _tokenId);
    // remove delegates
    _moveTokenDelegates(delegates(_to), address(0), _tokenId);
    // Remove token
    _removeTokenFrom(msg.sender, _tokenId);
    emit Transfer(owner, address(0), _tokenId);
}
```
**[pooltypes (Velodrome) acknowledged](https://github.com/code-423n4/2022-05-velodrome-findings/issues/153)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-05-velodrome-findings/issues/153#issuecomment-1170422615):**
 > The warden has shown how, in lack of `_moveTokenDelegates(delegates(_to), address(0), _tokenId);` an attacker could deny the ability to deposit tokens in the protocol.
> 
> Because a user could always roll a new address, I agree with Medium Severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Velodrome Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-velodrome
- **GitHub**: https://github.com/code-423n4/2022-05-velodrome-findings/issues/153
- **Contest**: https://code4rena.com/reports/2022-05-velodrome

### Keywords for Search

`vulnerability`

