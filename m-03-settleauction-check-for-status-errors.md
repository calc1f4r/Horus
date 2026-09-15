---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25819
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/582

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - bin2chen
  - kaden
---

## Vulnerability Title

[M-03] `settleAuction()` Check for status errors

### Overview


This bug report is about the ClearingHouse.safeTransferFrom() function in the CollateralToken.sol code. The function is supposed to execute successfully even if there is no bid, but the code has a miswritten check that prevents this from happening. The normal logic should be that the collateralIdToAuction is equal to bytes32(0) OR the owner of the tokenId is equal to the ClearingHouse. The recommended mitigation step is to replace the miswritten code with the correct code, so that the function can execute successfully. The bug was confirmed by androolloyd (Astaria) and commented on by Picodes (judge), who determined the severity of the bug to be of medium despite the lack of clear impact.

### Original Finding Content


<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/CollateralToken.sol#L526-L534>

ClearingHouse.safeTransferFrom() to execute successfully even if there is no bid.

### Proof of Concept

settleAuction is called at the end of the auction and will check if the status is legal

```solidity

  function settleAuction(uint256 collateralId) public {
    if (
      s.collateralIdToAuction[collateralId] == bytes32(0) &&
      ERC721(s.idToUnderlying[collateralId].tokenContract).ownerOf(
        s.idToUnderlying[collateralId].tokenId
      ) !=
      s.clearingHouse[collateralId]
    ) {
      revert InvalidCollateralState(InvalidCollateralStates.NO_AUCTION);
    }
```

This check seems to be miswritten，The normal logic would be

```solidity
s.collateralIdToAuction[collateralId] == bytes32(0) || ERC721(s.idToUnderlying[collateralId].tokenContract).ownerOf(
        s.idToUnderlying[collateralId].tokenId
      ) == s.clearingHouse[collateralId]
```

This causes ClearingHouse.safeTransferFrom() to execute successfully even if there is no bid.

### Recommended Mitigation Steps

```solidity

  function settleAuction(uint256 collateralId) public {
    if (
-     s.collateralIdToAuction[collateralId] == bytes32(0) &&
-    ERC721(s.idToUnderlying[collateralId].tokenContract).ownerOf(
-        s.idToUnderlying[collateralId].tokenId
-      ) !=
-      s.clearingHouse[collateralId]
+      s.collateralIdToAuction[collateralId] == bytes32(0) || 
+       ERC721(s.idToUnderlying[collateralId].tokenContract).ownerOf(s.idToUnderlying[collateralId].tokenId
+      ) == 
+      s.clearingHouse[collateralId]
    ) {
      revert InvalidCollateralState(InvalidCollateralStates.NO_AUCTION);
    }
```

**[androolloyd (Astaria) confirmed](https://github.com/code-423n4/2023-01-astaria-findings/issues/582)**

**[Picodes (judge) commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/582#issuecomment-1439153219):**
 > Keeping medium severity despite the lack of clear impact, the lack of clear impact being due to flaws in the flow before these lines.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | bin2chen, kaden |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/582
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

