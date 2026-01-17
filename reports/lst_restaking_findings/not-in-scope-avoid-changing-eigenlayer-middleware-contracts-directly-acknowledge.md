---
# Core Classification
protocol: Aligned Layer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38373
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2024/08/aligned-layer/
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
finders_count: 2
finders:
  - Martin Ortner
  -  George Kobakhidze
                        
---

## Vulnerability Title

[Not-in-Scope] Avoid Changing Eigenlayer-Middleware Contracts Directly  Acknowledged

### Overview


This bug report addresses changes that are needed to implement Aligned contracts. These changes affect certain functions, such as `BLSSignatureChecker.checkSignatures`, `RegistryCoordinator.registerOperator`, and `RegistryCoordinator.initialize`, which are non-virtual functions in the Layr-Labs created contracts. The report suggests that a fork is the simplest option to make these changes, but the Aligned team should be cautious and careful during upgrades if and when Layr-Labs contracts are updated.

The report also mentions that the Aligned team has provided a draft patch for review, but advises against directly patching the audited Layr-Labs repository. This is because the patch makes very protocol-specific changes that deviate from how eigenlayer-middleware is meant to be used. Additionally, the patch adds a `Whitelist` contract that lacks clear visibility specifiers and does not emit events when addresses are added or removed from the whitelist. The report recommends subclassing the original `RegistryCoordinator` to add the patched whitelisting features, rather than patching the source contract in the foreign-maintained repository. It also suggests avoiding reformatting the codebase, as it may make it difficult to compare future versions of the aligned version with the original.

The report concludes by recommending that the Aligned team avoid making direct modifications to third-party codebases like the Layr-Labs repository. Instead, they should import the required components, subclass when necessary, and override functionality within the Aligned codebase. This approach will ensure compatibility with the original API, reduce maintenance complexity, and ensure alignment with eigenlayer documentation and future updates.

### Original Finding Content

#### Resolution



The implementation of Aligned contracts requires changes in logic of functions such as:


* `BLSSignatureChecker.checkSignatures`
* `RegistryCoordinator.registerOperator`
* `RegistryCoordinator.initialize`
* Contract constructors
Which are non\-virtual functions in the Layr\-Labs created contracts. As a result, it won’t be possible to override them, and a fork is the simplest option. However, the Aligned team should take note that this approach should be done cautiously, and significant care should be applied during upgrades if and when Layr\-Labs contracts are updated.




#### Description


The Aligned team has indicated that they rely on eigenlayer\-middleware patches to implement whitelisting features in the Registry Coordinator. The team provided a [draft patch](https://github.com/Layr-Labs/eigenlayer-middleware/pull/295/files) for review. However, we advise against directly patching the audited Layr\-Labs repository for the following reasons:


* [src/BLSSignatureChecker.sol](https://github.com/Layr-Labs/eigenlayer-middleware/pull/295/files#diff-bea9ae8c6cafebda0b71c4e92d5420b35cada7b08fd33c6e06e307350dd362da) and [src/interfaces/IBLSSignatureChecker.sol](https://github.com/Layr-Labs/eigenlayer-middleware/pull/295/files#diff-682d35381822f196fb40851c97cd4ee664b7a45cd0ae656f06bd14d8315db103) change the function signature of `checkSignatures` to exclude `quorumNumbers` as they are hardcoded to `ALIGNED_QUORUM_NUMBER`. This is a very protocol\-specific changeset that changes the Layer\-Labs API which should be avoided by all costs as this will be very hard to maintain when trying to update to newer eigenlayer\-middleware releases (i.e. security updates, etc.). Hardcoding the quorums to `ALIGNED_QUORUM_NUMBER` (hex 0x00\) diverges from how eigenlayer\-middleware is meant to be used.
* [src/Whitelist.sol](https://github.com/Layr-Labs/eigenlayer-middleware/pull/295/files#diff-c3ccd4844f0ce2b00ac83b490f0bdf0dcb59e250eaaea6478ef8c008c0dbe067) adds a `Whitelist` contract. The contract lacks clear visibility specifiers for the internal `whitelist` mapping (defaults to internal). Adding/Removing addresses from/to whitelist does not yield any events although it is an important administrative action (monitoring/trail of events). The contract should be `abstract` as it is meant to be inherited by other contracts.
* [src/RegistryCoordinator.sol](https://github.com/Layr-Labs/eigenlayer-middleware/pull/295/files#diff-a76428044d34fa4218c81701c5ad3602e1d0484b6eefbe7fbfb8350fa5eb6559) patches the stock `RegistryCoordinator` inside the eigenlayer repository (!) to include Whitelist functionality. Instead of patching the source contract in the foreign\-maintained repository, it would be much better to sub\-class the RegistryCoordinator by building an `AlignedRegistryCoordinator` that inherits from the original `RegistryCoordinator` overriding functionality with the patched whitelisting features. Furthermore, the changeset changes/shortens error messages emitted by the stock `RegistryCoordinator` which basically makes the contract diverge from the original API and specification. This may be problematic as the contract does not match the eigenlayer API documentation anymore.
* In general, reformatting the codebase may make it increasingly hard to diff future versions of the aligned version from the upstream.


#### Recommendation


Avoid making direct modifications to third\-party codebases like the Layr\-Labs repository. Instead, import the required components, subclass where necessary, and override functionality within the Aligned codebase. This approach preserves compatibility with the original API, reduces maintenance complexity, and ensures alignment with eigenlayer documentation and future updates.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Aligned Layer |
| Report Date | N/A |
| Finders | Martin Ortner,  George Kobakhidze
                         |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2024/08/aligned-layer/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

