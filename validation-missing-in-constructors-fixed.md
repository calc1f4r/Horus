---
# Core Classification
protocol: Linea ENS
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34974
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2024/06/linea-ens/
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
finders_count: 0
finders:
---

## Vulnerability Title

Validation Missing in Constructors ✓ Fixed

### Overview


This bug report discusses an issue with the NameWrapper and ETHRegistrarController contracts in the linea-resolver project. The problem has been fixed in a recent pull request, but there are still some issues that need to be addressed. In the constructor of the ETHRegistrarController contract, the parameters pohVerifier and pohRegistrationManager are not checked against a zero address. Additionally, in both the NameWrapper and ETHRegistrarController contracts, the base node and base domain are not properly validated, which could lead to conflicts with the L1 ENS system. The report recommends adding missing validations in the constructors of these contracts.

### Original Finding Content

#### Resolution



 The problem has been fixed in the [PR\#164](https://github.com/Consensys/linea-resolver/pull/164/files) . However in the NameWrapper contract there is a `hardhat/console.sol` import, which should be removed.
 

#### Description


In the constructor of contract `ETHRegistrarController` , the parameters `pohVerifier` and `pohRegistrationManager` are not checked against zero address.
In contract `NameWrapper` and `ETHRegistrarController`, the base node(`baseNode`) and base domain(`baseDomain`) are not validated to ensure they are neither ETH\_NODE nor ROOT\_NODE, nor are they checked for being empty. Additionally, the baseNode is expected to be the namehash of the baseDomain. However these validations are missing in the constructors of both contracts. As a result if invalid base node or base domain is set, it could lead to the registration of invalid ENS names, causing conflicts in name resolution with the L1 ENS system.


#### Examples


**packages/l2\-contracts/contracts/ethregistrar/ETHRegistrarController.sol:L130\-L148**



```
) ReverseClaimer(_ens, msg.sender) {
    if (_maxCommitmentAge <= _minCommitmentAge) {
        revert MaxCommitmentAgeTooLow();
    }

    if (_maxCommitmentAge > block.timestamp) {
        revert MaxCommitmentAgeTooHigh();
    }

    base = _base;
    prices = _prices;
    minCommitmentAge = _minCommitmentAge;
    maxCommitmentAge = _maxCommitmentAge;
    reverseRegistrar = _reverseRegistrar;
    nameWrapper = _nameWrapper;
    pohVerifier = _pohVerifier;
    pohRegistrationManager = _pohRegistrationManager;
    baseNode = _baseNode;
    baseDomain = _baseDomain;

```
**packages/l2\-contracts/contracts/wrapper/NameWrapper.sol:L77\-L101**



```
baseNode = _baseNode;

/* Burn PARENT_CANNOT_CONTROL and CANNOT_UNWRAP fuses for ROOT_NODE, ETH_NODE and baseNode and set expiry to max */

_setData(
    uint256(_baseNode),
    address(0),
    uint32(PARENT_CANNOT_CONTROL | CANNOT_UNWRAP),
    MAX_EXPIRY
);
_setData(
    uint256(ETH_NODE),
    address(0),
    uint32(PARENT_CANNOT_CONTROL | CANNOT_UNWRAP),
    MAX_EXPIRY
);
_setData(
    uint256(ROOT_NODE),
    address(0),
    uint32(PARENT_CANNOT_CONTROL | CANNOT_UNWRAP),
    MAX_EXPIRY
);
names[ROOT_NODE] = "\x00";
names[ETH_NODE] = "\x03eth\x00";
names[_baseNode] = _baseNodeDnsEncoded;

```
#### Recommendation


Add missing validations in the constructor of `NameWrapper` and `ETHRegistrarController` contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Linea ENS |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2024/06/linea-ens/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

