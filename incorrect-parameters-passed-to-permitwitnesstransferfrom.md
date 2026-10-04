---
# Core Classification
protocol: Across Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56766
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Incorrect Parameters Passed to permitWitnessTransferFrom

### Overview


The `PERMIT2_ORDER_TYPE` variable in the `ERC7683Across` contract is supposed to define the type of data used for the `witness` parameter in the `permitWitnessTransferFrom` function. However, it currently specifies the wrong data type and does not take into account certain members of the `GaslessCrossChainOrder` and `AcrossOrderData` structs. This causes the `CROSS_CHAIN_ORDER_TYPE` variable to have an incorrect encoding and violates the `EIP-712` and `Permit2` standards. The issue has been resolved in a recent pull request.

### Original Finding Content

The [`PERMIT2_ORDER_TYPE` variable](https://github.com/across-protocol/contracts/blob/108be77c29a3861c64bdf66209ac6735a6a87090/contracts/erc7683/ERC7683Across.sol#L67) stores the witness data type string, which is supposed to be passed as the `witnessTypeString` parameter to the `permitWitnessTransferFrom` function of the `Permit2` contract. As such, this variable is supposed to define the typed data that the `witness` parameter passed to that function was hashed from. However, it instead [specifies](https://github.com/across-protocol/contracts/blob/108be77c29a3861c64bdf66209ac6735a6a87090/contracts/erc7683/ERC7683Across.sol#L70) that the `witness` parameter has been hashed from the `CrossChainOrder` type, whereas in reality, [it was hashed from the `GaslessCrossChainOrder` type](https://github.com/across-protocol/contracts/blob/108be77c29a3861c64bdf66209ac6735a6a87090/contracts/erc7683/ERC7683OrderDepositor.sol#L331).

Moreover, the `witness` parameter specified is incorrect as the [`orderDataType`](https://github.com/across-protocol/contracts/blob/108be77c29a3861c64bdf66209ac6735a6a87090/contracts/erc7683/ERC7683.sol#L22) member of the `GaslessCrossChainOrder` struct is not taken into account when [calculating it](https://github.com/across-protocol/contracts/blob/108be77c29a3861c64bdf66209ac6735a6a87090/contracts/erc7683/ERC7683Across.sol#L80-L91). The same is true for the [`exclusiveRelayer`](https://github.com/across-protocol/contracts/blob/108be77c29a3861c64bdf66209ac6735a6a87090/contracts/erc7683/ERC7683Across.sol#L15) and [`depositNonce`](https://github.com/across-protocol/contracts/blob/7641fbf38b661e02fc00f3b33d7e587c6dc5f06f/contracts/erc7683/ERC7683Across.sol#L16) members of the `AcrossOrderData` struct, which are [not included](https://github.com/across-protocol/contracts/blob/7641fbf38b661e02fc00f3b33d7e587c6dc5f06f/contracts/erc7683/ERC7683Across.sol#L106-L107) in the calculation of its hash. Furthermore, the `CROSS_CHAIN_ORDER_TYPE` variable used to create the `witness` contains an incorrect encoding of the [`GaslessCrossChainOrder` struct](https://github.com/across-protocol/contracts/blob/108be77c29a3861c64bdf66209ac6735a6a87090/contracts/erc7683/ERC7683.sol#L6) as the [`originChainId` member](https://github.com/across-protocol/contracts/blob/108be77c29a3861c64bdf66209ac6735a6a87090/contracts/erc7683/ERC7683Across.sol#L55) is specified to be of type `uint32` instead of `uint64`.

Consider correcting the errors described above in order to maintain compliance with `EIP-712` and `Permit2`.

***Update:** Resolved in [pull request #745](https://github.com/across-protocol/contracts/pull/745) at commit [b1b5904](https://github.com/across-protocol/contracts/pull/745/commits/b1b5904d992b5840efa73211707804dd690a01ed) and at commit [98c761e](https://github.com/across-protocol/contracts/commit/98c761ee9ca3a496b4a368bdf12743d727644138). The team stated:*

> *There have been some changes to ERC7682 during the audit, so these fixes are split between two commits. The first commit (and the attached PR) addresses the first paragraph and all of the second paragraph except for `depositNonce` and swapping `originChainId` to a uint64. The `depositNonce` has since been removed, and the origin chains now match as a result of the second commit.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

