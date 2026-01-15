---
# Core Classification
protocol: Sudoswap LSSVM2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18280
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
github_link: none

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
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

Function token() ofcloneERC1155ERC20Pair() reads from wrong location

### Overview


This bug report is related to LSSVMPairERC20.sol and LSSVMPairCloner.sol. The function token() was loading the token data from position 81, however, it should have been loading it from position 93. This caused the code to not work correctly. The code was updated in PR#21 so that the function token() reads the last 20 bytes, which solved the issue. This was verified by Spearbit.

### Original Finding Content

## Severity: High Risk

## Context
- **Files:** LSSVMPairERC20.sol#L26-L31, LSSVMPairCloner.sol#L359-L436

## Description
The function `token()` loads the token data from position 81. However, on ERC1155 pairs, it should load it from position 93. Currently, it doesn't retrieve the right values, and the code won't function correctly.

### Code References
- **LSSVMPair.sol:**
  - `_factory := shr(0x60, calldataload(sub(calldatasize(), paramsLength)))`
  - `_bondingCurve := shr(0x60, calldataload(add(sub(calldatasize(), paramsLength), 20))) , !`
  - `_nft := shr(0x60, calldataload(add(sub(calldatasize(), paramsLength), 40))) , !`
  - `_poolType := shr(0xf8, calldataload(add(sub(calldatasize(), paramsLength), 60))) , !`
  
- **LSSVMPairERC1155.sol:**
  - `id := calldataload(add(sub(calldatasize(), paramsLength), 61))`
  
- **LSSVMPairERC721.sol:**
  - `_propertyChecker := shr(0x60, calldataload(add(sub(calldatasize(), paramsLength), 61))) , !`
  
- **LSSVMPairERC20.sol:**
  - `_token := shr(0x60, calldataload(add(sub(calldatasize(), paramsLength), 81))) , !`

### Assembly Code Sample
```assembly
function cloneERC1155ERC20Pair(... ) ... {
assembly {
...
mstore(add(ptr, 0x3e), shl(0x60, factory)) // position 0 - 20 bytes
mstore(add(ptr, 0x52), shl(0x60, bondingCurve)) // position 20 - 20 bytes
mstore(add(ptr, 0x66), shl(0x60, nft)) // position 40 - 20 bytes
mstore8(add(ptr, 0x7a), poolType) // position 60 - 1 bytes
mstore(add(ptr, 0x7b), nftId) // position 61 - 32 bytes
mstore(add(ptr, 0x9b), shl(0x60, token)) // position 93 - 20 bytes
...
}
}
```

## Recommendation
After the review has started, the function `token()` has been updated to read the last 20 bytes. See PR#21.

## Status
- **Sudorandom Labs:** Solved in PR#21.
- **Spearbit:** Verified that this is fixed by PR#21.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap LSSVM2 |
| Report Date | N/A |
| Finders | Gerard Persoon, Shodan, Rajeev, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

