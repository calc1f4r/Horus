---
# Core Classification
protocol: NFTPort
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3555
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/14
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-nftport-judging/issues/33

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
  - liquidity_manager
  - nft_lending
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - obront
---

## Vulnerability Title

M-10: Missing check for equal length arrays in transferByOwnerBatch and mintByOwnerBatch

### Overview


This bug report is about two functions in the ERC1155 implementation, `transferByOwnerBatch()` and `mintByOwnerBatch()`. These functions do not check whether the lengths of the arrays submitted by the user are equal. This can lead to unexpected results, as the extra values in the other arrays will be ignored. To prevent this issue, a check should be added to both functions to ensure that the lengths of the arrays are equal. This has been fixed in the code, and the check is now in place.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-nftport-judging/issues/33 

## Found by 
obront

## Summary

The `transferByOwnerBatch()` and `mintByOwnerBatch()` functions in the ERC1155 implementation does not check whether the lengths of the arrays submitted are equal. This can lead to unexpected results.

## Vulnerability Detail

In the `transferByOwnerBatch()` function, the user submits three arrays (addresses, ids, and amounts), while in the `mintByOwnerBatch()` function, the user submits four arrays (addresses, ids, amounts, uris).

The expectation is that the user submitting the function will ensure that the indexes of the arrays correspond to the correct values in the other arrays, and thus that the lengths will be the same.

Common practice in such a situation is to verify that the lengths are equal to ensure the user hasn't made an error. In other functions like `burnBatch()`, this verification is done by the underlying ERC1155 function. 

However, in these two functions, we simply iterate through the `ids` array without performing this check, and then call out to the underlying ERC1155 `_safeTransferFrom()`  or `_mint()` functions for each id separately.

## Impact

If the `ids` array is a shorter length than the other arrays, the additional values in the other arrays will be ignored. This could lead to transfers with unexpected results, which would be better served by reverting.

## Code Snippet

https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/ERC1155NFTProduct.sol#L206-L215

https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/ERC1155NFTProduct.sol#L279-L299

## Tool used

Manual Review

## Recommendation

Add a check to the `transferByOwnerBatch()` function that confirms that to, ids, and amounts are all equal length.

```solidity
require(ids.length == to.length, "mismatched array lengths");
require(ids.length == amounts.length, "mismatched array lengths");
```

Add a check to the `mintByOwnerBatch()` function that confirms that to, ids, amounts, and uris are all equal length.

```solidity
require(ids.length == to.length, "mismatched array lengths");
require(ids.length == amounts.length, "mismatched array lengths");
require(ids.length == uris.length, "mismatched array lengths");
```

## Discussion

**hyperspacebunny**

Fixed in https://github.com/nftport/evm-minting-sherlock-fixes/pull/13

**rayn731**

Fixed, checks the arrays' length should be equal.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | NFTPort |
| Report Date | N/A |
| Finders | obront |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-nftport-judging/issues/33
- **Contest**: https://app.sherlock.xyz/audits/contests/14

### Keywords for Search

`vulnerability`

