---
# Core Classification
protocol: Stakewise - v3 Vaults / EthFoxVault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33838
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2024/03/stakewise-v3-vaults-/-ethfoxvault/
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
  -  Valentin Quelquejay
                        
  - Martin Ortner
---

## Vulnerability Title

VaultsRegistry Allows Owner to Bypass VaultFactory  Acknowledged

### Overview


The report discusses an issue with the VaultRegistry, which is a system that registers approved Vaults. The problem is that the owner of the registry has the ability to add Vaults that have not been created by an approved VaultFactory. This undermines the guarantee that only approved Factories can register Vaults. It is recommended to enforce that all Vaults are created with an approved factory and to ensure that everyone understands the implications of allowing the owner to add Vaults out-of-band.

### Original Finding Content

#### Resolution



 Acknowledged - By Design. While a registry owner (StakeWise DAO) can register factories, and these factories, in turn, can register vaults, adding vaults out-of-band doesn’t increase trust in the system.
 

#### Description


Creating a Vault with an approved VaultFactory ensures that only approved implementations of Vaults can be registered with the system. For example, when a Vault Owner creates a new Vault via `VaultFactory.createVault()` the function deploys a proxy pointing to a fixed implementation. Additionally, the newly added Vault address is registered with the VaultRegistry. Only approved factories are allowed to register Vaults with the `VaultRegistry.addVault()`.


However, the guarantee that only approved Factories (with approved implementations) can register Vaults is undermined by permissions the VaultRegistry owner has. They can unilaterally register Vaults that have not been created by the VaultFactory.


It is not clear if the registered Vault is actually a vault contract (or even EOA), nor if it’s been properly initialized within one transaction (see [issue 4.5](#front-running-vulnerability-during-initialization-of-vault-contracts)) as it can be registered out of band by the owner.


#### Examples


**contracts/vaults/VaultsRegistry.sol:L31-L37**



```
/// @inheritdoc IVaultsRegistry
function addVault(address vault) external override {
  if (!factories[msg.sender] && msg.sender != owner()) revert Errors.AccessDenied();

  vaults[vault] = true;
  emit VaultAdded(msg.sender, vault);
}

```
#### Recommendation


Ensure and provide guarantees on the origin of Vaults by enforcing that they’ve been created with an approved factory. If the owner is a multi-sig or DAO, ensure that everyone understands the implications of allowing the owner to add vaults to the registry out-of-band (`SharedMevRewards`) and the scrutiny required to avoid that a malicious Vault is added to the registry.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Stakewise - v3 Vaults / EthFoxVault |
| Report Date | N/A |
| Finders |  Valentin Quelquejay
                        , Martin Ortner |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2024/03/stakewise-v3-vaults-/-ethfoxvault/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

