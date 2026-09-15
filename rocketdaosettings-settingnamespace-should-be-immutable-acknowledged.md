---
# Core Classification
protocol: Rocket Pool Atlas (v1.2)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13220
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/01/rocket-pool-atlas-v1.2/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dominik Muhs
  -  Martin Ortner

---

## Vulnerability Title

RocketDAO*Settings - settingNameSpace should be immutable  Acknowledged

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



Acknowledged by the client. Not addressed within [rocket-pool/[email protected]`77d7cca`](https://github.com/rocket-pool/rocketpool/commit/77d7cca65b7c0557cfda078a4fc45f9ac0cc6cc6)



> 
> Acknowledged. We can fix this as we upgrade the related contracts.
> 
> 
> 




#### Description


The `settingNameSpace` in the abstract contract `RocketDAONodeTrustedSettings` is only set on contract deployment. Hence, the fields should be declared immutable to make clear that the settings namespace cannot change after construction.


#### Examples


* `RocketDAONodeTrustedSettings`


**code/contracts/contract/dao/node/settings/RocketDAONodeTrustedSettings.sol:L13-L16**



```
// The namespace for a particular group of settings
bytes32 settingNameSpace;



```
**code/contracts/contract/dao/node/settings/RocketDAONodeTrustedSettings.sol:L25-L30**



```
// Construct
constructor(RocketStorageInterface \_rocketStorageAddress, string memory \_settingNameSpace) RocketBase(\_rocketStorageAddress) {
    // Apply the setting namespace
    settingNameSpace = keccak256(abi.encodePacked("dao.trustednodes.setting.", \_settingNameSpace));
}


```
* `RocketDAOProtocolSettings`


**code/contracts/contract/dao/protocol/settings/RocketDAOProtocolSettings.sol:L13-L14**



```
// The namespace for a particular group of settings
bytes32 settingNameSpace;

```
**code/contracts/contract/dao/protocol/settings/RocketDAOProtocolSettings.sol:L25-L29**



```
// Construct
constructor(RocketStorageInterface \_rocketStorageAddress, string memory \_settingNameSpace) RocketBase(\_rocketStorageAddress) {
    // Apply the setting namespace
    settingNameSpace = keccak256(abi.encodePacked("dao.protocol.setting.", \_settingNameSpace));
}

```
**code/contracts/contract/dao/protocol/settings/RocketDAOProtocolSettingsAuction.sol:L13-L15**



```
constructor(RocketStorageInterface \_rocketStorageAddress) RocketDAOProtocolSettings(\_rocketStorageAddress, "auction") {
    // Set version
    version = 1;

```
#### Recommendation


We recommend using the `immutable` annotation in Solidity (see [Immutable](https://solidity.readthedocs.io/en/latest/contracts.html#immutable)).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Rocket Pool Atlas (v1.2) |
| Report Date | N/A |
| Finders | Dominik Muhs,  Martin Ortner
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/01/rocket-pool-atlas-v1.2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

