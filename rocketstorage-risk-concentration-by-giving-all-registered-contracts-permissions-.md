---
# Core Classification
protocol: Rocketpool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13437
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/04/rocketpool/
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
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Martin Ortner
  - Dominik Muhs
  -  David Oz Kashi
---

## Vulnerability Title

RocketStorage - Risk concentration by giving all registered contracts permissions to change any settings in RocketStorage  Acknowledged

### Overview


This bug report is about the access control list (ACL) for the centralized RocketStorage, which allows any registered contract to change settings that belong to other parts of the system. This could lead to malicious contracts overriding settings in the system, which would give the attacker control over the complete system. The code snippets provided show that any contract can set addresses and integers in the storage, regardless of their namespace.

The recommended solution is to only allow contracts to change settings related to their namespace. This would reduce the attack surface and gas usage, while still allowing upgrades.

### Original Finding Content

#### Resolution



The client provided the following statement:



> 
> We’ve looked at adding access control contracts using namespaces, but the increase in gas usage would be significant and could hinder upgrades.
> 
> 
> 




#### Description


The ACL for changing settings in the centralized `RocketStorage` allows any registered contract (listed under `contract.exists`) to change settings that belong to other parts of the system.


The concern is that if someone finds a way to add their malicious contract to the registered contact list, they will override any setting in the system. The storage is authoritative when checking certain ACLs. Being able to set any value might allow an attacker to gain control of the complete system. Allowing any contract to overwrite other contracts' settings dramatically increases the attack surface.


#### Examples


**rocketpool-2.5-Tokenomics-updates/contracts/contract/RocketStorage.sol:L24-L32**



```
modifier onlyLatestRocketNetworkContract() {
    // The owner and other contracts are only allowed to set the storage upon deployment to register the initial contracts/settings, afterwards their direct access is disabled
    if (boolStorage[keccak256(abi.encodePacked("contract.storage.initialised"))] == true) {
        // Make sure the access is permitted to only contracts in our Dapp
        require(boolStorage[keccak256(abi.encodePacked("contract.exists", msg.sender))], "Invalid or outdated network contract");
    }
    \_;
}


```
**rocketpool-2.5-Tokenomics-updates/contracts/contract/RocketStorage.sol:L78-L85**



```
function setAddress(bytes32 \_key, address \_value) onlyLatestRocketNetworkContract override external {
    addressStorage[\_key] = \_value;
}

/// @param \_key The key for the record
function setUint(bytes32 \_key, uint \_value) onlyLatestRocketNetworkContract override external {
    uIntStorage[\_key] = \_value;
}

```
#### Recommendation


Allow contracts to only change settings related to their namespace.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Rocketpool |
| Report Date | N/A |
| Finders | Martin Ortner, Dominik Muhs,  David Oz Kashi |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/04/rocketpool/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

