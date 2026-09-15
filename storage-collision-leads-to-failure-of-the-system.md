---
# Core Classification
protocol: zkSync Layer 1 Diff Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10382
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/zksync-layer-1-diff-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Storage collision leads to failure of the system

### Overview


A bug was discovered in the `Storage.sol` file, which is part of the Diamond proxy pattern. The `AppStorage` struct in this file keeps track of all stored values for the layer 1 system and contained two structs - `DiamondCutStorage` and `UpgradeStorage`. It was discovered that the two structs had different sizes, resulting in a storage collision and a potential system failure. This could lead to the operator losing the governor privilege and the former security council members becoming validators, with all stored block info being lost.

A possible solution was to re-initialize the `AppStorage` during the upgrade process, however, this was not feasible from a gas consumption perspective and required an off-chain data collection. An alternative solution was to leave the former struct as is and only append new data to the end of the `AppStorage` struct, while thoroughly documenting that the `DiamondCutStorage` must remain a member of `AppStorage`. Additionally, a machine-readable artefact was created to describe the deployed `AppStorage` layout and a check was integrated in the CI system. The bug was resolved in commit [cd417be].

### Original Finding Content

In the `Storage.sol` file, the `AppStorage` struct keeps track of all stored values for the layer 1 system as part of the Diamond proxy pattern. The first entry of this struct is the [`DiamondCutStorage` struct](https://github.com/matter-labs/zksync-2-dev/blob/0e5a8d527d727d7e2a0b7c4474678bc6155bd826/contracts/ethereum/contracts/zksync/Storage.sol#L17-L25) for the deployed code version and the [`UpgradeStorage` struct](https://github.com/matter-labs/zksync-2-dev/blob/534dc37c7b86753803a31b836f78896d18372e7e/contracts/ethereum/contracts/zksync/Storage.sol#L25-L32) for the audited and to-be-upgraded version. Both are used to track upgrade data for the `DiamondCut` facet.


As seen by [comparing their entries](https://github.com/matter-labs/zksync-2-dev/compare/0e5a8d527d727d7e2a0b7c4474678bc6155bd826..534dc37c7b86753803a31b836f78896d18372e7e#diff-f4fda146188d8689f16b86230a78504746799415e0d55768e1931068dd58c0ddL17-R75), the structs have changed in size. Originally, `DiamondCutStorage` occupied 7 storage slots, while `UpgradeStorage` only occupies 2. Respectively, the slots of all following variables in the `AppStorage` struct shift, thereby resulting in a storage collision. Due to this desynchronization of storage, the entire system functionality would break and come to a halt.


For instance, the new `governor` address slot would match the former `lastDiamondFreezeTimestamp` value. Hence, by applying the upgrade, the operator loses the governor privilege. As such, the ability to perform further upgrades is lost and no other mechanism of recovery is present in the system. Moreover, the new `verifier` mapping would match the old `securityCouncilMembers` mapping. Thus, former council members would become validators. Since all stored block info would be lost, the validators could not commit any new blocks anyways.


In order to apply the upgrade in spite of the storage collision, one could re-initialize the `AppStorage` during the initialization stage of the *same exact* Diamond upgrade. However, properly overwriting the mappings does not seem feasible from a gas consumption perspective. Additionally, it requires a diligent off-chain data collection of all mapping data in need of overwrites. In conclusion, missing this opportunity is very probably and likely to fail.


Consider leaving the former struct as is and only appending new data to the end of the `AppStorage` struct. Thoroughly document that while `DiamondCutStorage` is unused, it must remain a member of `AppStorage`. Additionally, create a machine-readable artefact describing the deployed `AppStorage` layout, and integrate a check against it in your CI system.


***Update**: Resolved in commit [cd417be](https://github.com/matter-labs/zksync-2-dev/pull/1166/commits/cd417be91ef2cae083f3d01ca6b8e9d3e7118187)*.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | zkSync Layer 1 Diff Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/zksync-layer-1-diff-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

