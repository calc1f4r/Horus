---
# Core Classification
protocol: LUKSO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25996
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-lukso
source_link: https://code4rena.com/reports/2023-06-lukso
github_link: https://github.com/code-423n4/2023-06-lukso-findings/issues/120

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
  - MiloTruck
---

## Vulnerability Title

[M-04] `LSP8Burnable` extension incorrectly inherits `LSP8IdentifiableDigitalAssetCore`

### Overview


This bug report is about the `LSP8Burnable` contract which is part of the LUKSO project. This contract is supposed to inherit from the `LSP8IdentifiableDigitalAsset` contract, however, it currently inherits from `LSP8IdentifiableDigitalAssetCore`. This issue can be seen by comparing the code in `LSP8Burnable.sol` with the code in `LSP8CappedSupply.sol`, `LSP8CompatibleERC721.sol` and `LSP8Enumerable.sol`. Additionally, the `LSP8BurnableInitAbstract.sol` file is missing in the repository.

If this issue is not fixed, developers who implement their LSP8 token using `LSP8Burnable` will face the following issues. All functionality from `LSP4DigitalAssetMetadata` will be unavailable and as `LSP8Burnable` does not contain a `supportsInterface()` function, it will be incompatible with contracts that use ERC-165.

The recommended mitigation for this issue is to change the inheritance of `LSP8Burnable` from `LSP8IdentifiableDigitalAssetCore` to `LSP8IdentifiableDigitalAsset` and to add a `LSP8BurnableInitAbstract.sol` file that contains an implementation of `LSP8Burnable` which can be used in proxies. This bug report was confirmed by the LUKSO project.

### Original Finding Content


The `LSP8Burnable` contract inherits from `LSP8IdentifiableDigitalAssetCore`:

[LSP8Burnable.sol#L15](https://github.com/code-423n4/2023-06-lukso/blob/main/contracts/LSP8IdentifiableDigitalAsset/extensions/LSP8Burnable.sol#L15)

```solidity
abstract contract LSP8Burnable is LSP8IdentifiableDigitalAssetCore {
```

However, LSP8 extensions are supposed to inherit `LSP8IdentifiableDigitalAsset` instead. This can be inferred by looking at [`LSP8CappedSupply.sol`](https://github.com/code-423n4/2023-06-lukso/blob/main/contracts/LSP8IdentifiableDigitalAsset/extensions/LSP8CappedSupply.sol), [`LSP8CompatibleERC721.sol`](https://github.com/code-423n4/2023-06-lukso/blob/main/contracts/LSP8IdentifiableDigitalAsset/extensions/LSP8CompatibleERC721.sol) and [`LSP8Enumerable.sol`](https://github.com/code-423n4/2023-06-lukso/blob/main/contracts/LSP8IdentifiableDigitalAsset/extensions/LSP8Enumerable.sol):

[LSP8CappedSupply.sol#L13](https://github.com/code-423n4/2023-06-lukso/blob/main/contracts/LSP8IdentifiableDigitalAsset/extensions/LSP8CappedSupply.sol#L13)

```solidity
abstract contract LSP8CappedSupply is LSP8IdentifiableDigitalAsset {
```

Additionally, the `LSP8BurnableInitAbstract.sol` file is missing in the repository.

### Impact

As `LSP8Burnable` does not inherit `LSP8IdentifiableDigitalAsset`, a developer who implements their LSP8 token using `LSP8Burnable` will face the following issues:

*   All functionality from `LSP4DigitalAssetMetadata` will be unavailable.
*   As `LSP8Burnable` does not contain a `supportsInterface()` function, it will be incompatible with contracts that use [ERC-165](https://eips.ethereum.org/EIPS/eip-165).

### Recommended Mitigation

The `LSP8Burnable` contract should inherit `LSP8IdentifiableDigitalAsset` instead:

[LSP8Burnable.sol#L15](https://github.com/code-423n4/2023-06-lukso/blob/main/contracts/LSP8IdentifiableDigitalAsset/extensions/LSP8Burnable.sol#L15)

```diff
-   abstract contract LSP8Burnable is LSP8IdentifiableDigitalAssetCore {
+   abstract contract LSP8Burnable is LSP8IdentifiableDigitalAsset {
```

Secondly, add a `LSP8BurnableInitAbstract.sol` file that contains an implementation of `LSP8Burnable` which can be used in proxies.

**[CJ42 (LUKSO) confirmed](https://github.com/code-423n4/2023-06-lukso-findings/issues/120#issuecomment-1649867493)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LUKSO |
| Report Date | N/A |
| Finders | MiloTruck |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-lukso
- **GitHub**: https://github.com/code-423n4/2023-06-lukso-findings/issues/120
- **Contest**: https://code4rena.com/reports/2023-06-lukso

### Keywords for Search

`vulnerability`

