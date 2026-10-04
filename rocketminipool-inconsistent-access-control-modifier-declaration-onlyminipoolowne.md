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
solodit_id: 13219
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

RocketMinipool - Inconsistent access control modifier declaration onlyMinipoolOwner  Acknowledged

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



Acknowledged by the client. Not addressed within [rocket-pool/[email protected]`77d7cca`](https://github.com/rocket-pool/rocketpool/commit/77d7cca65b7c0557cfda078a4fc45f9ac0cc6cc6)



> 
> Agreed. This would change a lot of contracts just for a minor improvement in readbility.
> 
> 
> 




#### Description


The access control modifier `onlyMinipoolOwner` should be renamed to `onlyMinipoolOwnerOrWithdrawalAddress` to be consistent with the actual check permitting the owner or the withdrawal address to interact with the function. This would also be consistent with other declarations in the codebase.


#### Example


The `onlyMinipoolOwner` modifier in `RocketMinipoolBase` is the same as `onlyMinipoolOwnerOrWithdrawalAddress` in other modules.


**code/contracts/contract/minipool/RocketMinipoolBase.sol:L31-L37**



```
/// @dev Only allow access from the owning node address
modifier onlyMinipoolOwner() {
    // Only the node operator can upgrade
    address withdrawalAddress = rocketStorage.getNodeWithdrawalAddress(nodeAddress);
    require(msg.sender == nodeAddress || msg.sender == withdrawalAddress, "Only the node operator can access this method");
    \_;
}

```
**code/contracts/contract/old/minipool/RocketMinipoolOld.sol:L21-L27**



```
// Only allow access from the owning node address
modifier onlyMinipoolOwner() {
    // Only the node operator can upgrade
    address withdrawalAddress = rocketStorage.getNodeWithdrawalAddress(nodeAddress);
    require(msg.sender == nodeAddress || msg.sender == withdrawalAddress, "Only the node operator can access this method");
    \_;
}

```
Other declarations:


**code/contracts/contract/minipool/RocketMinipoolDelegate.sol:L97-L107**



```
/// @dev Only allow access from the owning node address
modifier onlyMinipoolOwner(address \_nodeAddress) {
    require(\_nodeAddress == nodeAddress, "Invalid minipool owner");
    \_;
}

/// @dev Only allow access from the owning node address or their withdrawal address
modifier onlyMinipoolOwnerOrWithdrawalAddress(address \_nodeAddress) {
    require(\_nodeAddress == nodeAddress || \_nodeAddress == rocketStorage.getNodeWithdrawalAddress(nodeAddress), "Invalid minipool owner");
    \_;
}

```
**code/contracts/contract/old/minipool/RocketMinipoolDelegateOld.sol:L82-L92**



```
// Only allow access from the owning node address
modifier onlyMinipoolOwner(address \_nodeAddress) {
    require(\_nodeAddress == nodeAddress, "Invalid minipool owner");
    \_;
}

// Only allow access from the owning node address or their withdrawal address
modifier onlyMinipoolOwnerOrWithdrawalAddress(address \_nodeAddress) {
    require(\_nodeAddress == nodeAddress || \_nodeAddress == rocketStorage.getNodeWithdrawalAddress(nodeAddress), "Invalid minipool owner");
    \_;
}

```
#### Recommendation


We recommend renaming `RocketMinipoolBase.onlyMinipoolOwner` to `RocketMinipoolBase.onlyMinipoolOwnerOrWithdrawalAddress`.

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

