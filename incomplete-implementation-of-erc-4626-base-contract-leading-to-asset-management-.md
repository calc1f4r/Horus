---
# Core Classification
protocol: Forta Staking Vault Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32466
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/forta-staking-vault-audit
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
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Incomplete Implementation of ERC-4626 Base Contract Leading to Asset Management and Usability Issues

### Overview


The vault contract, which manages assets, has critical flaws that affect its functionality. The main issue is with the `mint` function, which correctly gives users shares but does not update the total assets and pool holdings. This leads to inaccurate tracking of assets and incorrect calculations for users trying to redeem shares. Another problem is the lack of an override for the `withdraw` function, which can cause transactions to fail and make it difficult for users to interact with the contract. To fix these issues, the `mint` and `withdraw` functions need to be modified to accurately reflect the total assets in the contract. This problem has been resolved in a recent update.

### Original Finding Content

The vault contract's adaptation from the ERC-4626 standard demonstrates critical flaws in asset management and functionality due to incomplete overrides of essential functions. Initially, the primary concern centers around the `mint` function. When users invoke the function, the contract correctly emits shares. However, it fails to update the [\_totalAssets](https://github.com/NethermindEth/forta-staking-vault/blob/ce87cffbf813e27cc83157933760b51fa44a1885/src/FortaStakingVault.sol#L47) variable and the pool's asset holdings. This discrepancy leads to a significant issue: the vault's asset tracking becomes inaccurate, which in turn will result in incorrect calculations when users attempt to redeem their shares.


Similarly, the omission of an override for the `withdraw` function can lead to transactions reverting when users attempt to execute withdrawals. Although this issue has a minor direct impact compared to the asset management flaw, it contributes to a degraded user experience, potentially deterring user interaction with the contract.


Consider modifying the `mint` and `withdraw` functions from the `ERC-4626Upgradeable` contract within the `FortaStakingVault` contract to accurately reflect withdrawn and minted assets in the `_totalAssets` variable.


***Update:** Resolved in [pull request #22](https://github.com/NethermindEth/forta-staking-vault/pull/22).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Forta Staking Vault Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/forta-staking-vault-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

