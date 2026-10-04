---
# Core Classification
protocol: KittenSwap_2025-05-07
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58164
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/KittenSwap-security-review_2025-05-07.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-06] `VotingEscrow._burn` prevents approved spender from using `withdraw()`

### Overview


This bug report discusses a medium severity issue in the code related to the `withdraw`, `merge`, and `split` operations. These operations use a function called `_isApprovedOrOwner` to allow the spender or operator of a `tokenId` to perform actions. However, inside the `_burn` function, the code attempts to remove the token from `msg.sender` instead of the actual `owner`. This prevents the spender or operator from performing these actions on behalf of the owner. 

The recommendation is to provide the `owner` instead of `msg.sender` to the `_removeTokenFrom` operation inside the `_burn` function. This will allow the spender or operator to perform actions on behalf of the owner.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

Inside the `withdraw`, `merge`, and `split` operations, there is a check using `_isApprovedOrOwner`, which allows the `tokenId`'s spender or operator to perform those actions.

```solidity
    function withdraw(uint _tokenId) external nonreentrant {
>>>     assert(_isApprovedOrOwner(msg.sender, _tokenId));
        require(attachments[_tokenId] == 0 && !voted[_tokenId], "attached");

        LockedBalance memory _locked = locked[_tokenId];
        require(block.timestamp >= _locked.end, "The lock didn't expire");
        uint value = uint(int256(_locked.amount));

        locked[_tokenId] = LockedBalance(0, 0);
        uint supply_before = supply;
        supply = supply_before - value;

        // old_locked can have either expired <= timestamp or zero end
        // _locked has only 0 end
        // Both can have >= 0 amount
        _checkpoint(_tokenId, _locked, LockedBalance(0, 0));

        assert(IERC20(token).transfer(msg.sender, value));

        // Burn the NFT
>>>     _burn(_tokenId);

        emit Withdraw(msg.sender, _tokenId, value, block.timestamp);
        emit Supply(supply_before, supply_before - value);
    }
```

However, inside the `_burn` function, it attempts to remove the token from `msg.sender` instead of the actual `owner`.

```solidity
    function _burn(uint _tokenId) internal {
        require(
            _isApprovedOrOwner(msg.sender, _tokenId),
            "caller is not owner nor approved"
        );

        address owner = ownerOf(_tokenId);

        // Clear approval
        approve(address(0), _tokenId);
        // checkpoint for gov
        _moveTokenDelegates(delegates(owner), address(0), _tokenId);
        // Remove token
>>>     _removeTokenFrom(msg.sender, _tokenId);
        emit Transfer(owner, address(0), _tokenId);
    }
```

```solidity
    function _removeTokenFrom(address _from, uint _tokenId) internal {
        // Throws if `_from` is not the current owner
>>>     assert(idToOwner[_tokenId] == _from);
        // Change the owner
        idToOwner[_tokenId] = address(0);
        // Update owner token index tracking
        _removeTokenFromOwnerList(_from, _tokenId);
        // Change count tracking
        ownerToNFTokenCount[_from] -= 1;
    }
```

This will prevent `tokenId`'s spender and operator to perform those actions on behalf of owner.

## Recommendations

Provide `owner` instead of `msg.sender` to `_removeTokenFrom` operation inside `_burn`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | KittenSwap_2025-05-07 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/KittenSwap-security-review_2025-05-07.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

