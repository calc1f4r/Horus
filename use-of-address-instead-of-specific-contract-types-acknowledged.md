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
solodit_id: 13214
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

Use of address instead of specific contract types  Acknowledged

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



The client acknowledges the finding, removed the unnecessary casts from `canReduceBondAmount` and `voteCancelReduction` with <https://github.com/rocket-pool/rocketpool/tree/77d7cca65b7c0557cfda078a4fc45f9ac0cc6cc6,> and provided the following statement:



> 
> Acknowledged. We will migrate to this pattern as we upgrade contracts.
> 
> 
> 




#### Description


Rather than using a low-level address type and then casting to the safer contract type, it’s better to use the best type available by default so the compiler can eventually check for type safety and contract existence and only downcast to less secure low-level types (`address`) when necessary.


#### Examples


`RocketStorageInterface _rocketStorage` should be declared in the arguments, removing the need to cast the address explicitly.


**code/contracts/contract/minipool/RocketMinipoolBase.sol:L39-L47**



```
/// @notice Sets up starting delegate contract and then delegates initialisation to it
function initialise(address \_rocketStorage, address \_nodeAddress) external override notSelf {
    // Check input
    require(\_nodeAddress != address(0), "Invalid node address");
    require(storageState == StorageState.Undefined, "Already initialised");
    // Set storage state to uninitialised
    storageState = StorageState.Uninitialised;
    // Set rocketStorage
    rocketStorage = RocketStorageInterface(\_rocketStorage);

```
`RocketMinipoolInterface _minipoolAddress` should be declared in the arguments, removing the need to cast the address explicitly. Downcast to low-level address if needed. The event can be redeclared with the contract type.


**code/contracts/contract/minipool/RocketMinipoolBondReducer.sol:L33-L34**



```
function beginReduceBondAmount(address \_minipoolAddress, uint256 \_newBondAmount) override external onlyLatestContract("rocketMinipoolBondReducer", address(this)) {
    RocketMinipoolInterface minipool = RocketMinipoolInterface(\_minipoolAddress);

```
**code/contracts/contract/minipool/RocketMinipoolBondReducer.sol:L69-L76**



```
/// @notice Returns whether owner of given minipool can reduce bond amount given the waiting period constraint
/// @param \_minipoolAddress Address of the minipool
function canReduceBondAmount(address \_minipoolAddress) override public view returns (bool) {
    RocketMinipoolInterface minipool = RocketMinipoolInterface(\_minipoolAddress);
    RocketDAONodeTrustedSettingsMinipoolInterface rocketDAONodeTrustedSettingsMinipool = RocketDAONodeTrustedSettingsMinipoolInterface(getContractAddress("rocketDAONodeTrustedSettingsMinipool"));
    uint256 reduceBondTime = getUint(keccak256(abi.encodePacked("minipool.bond.reduction.time", \_minipoolAddress)));
    return rocketDAONodeTrustedSettingsMinipool.isWithinBondReductionWindow(block.timestamp.sub(reduceBondTime));
}

```
**code/contracts/contract/minipool/RocketMinipoolBondReducer.sol:L80-L84**



```
function voteCancelReduction(address \_minipoolAddress) override external onlyTrustedNode(msg.sender) onlyLatestContract("rocketMinipoolBondReducer", address(this)) {
    // Prevent calling if consensus has already been reached
    require(!getReduceBondCancelled(\_minipoolAddress), "Already cancelled");
    // Get contracts
    RocketMinipoolInterface minipool = RocketMinipoolInterface(\_minipoolAddress);

```
Note that `abi.encode*(contractType)` assumes `address` for contract types by default. An explicit downcast is not required.



```
 »  Test example = Test(0x5B38Da6a701c568545dCfcB03FcB875f56beddC4)
 »  abi.encodePacked("hi", example)
0x68695b38da6a701c568545dcfcb03fcb875f56beddc4
 »  abi.encodePacked("hi", address(example))
0x68695b38da6a701c568545dcfcb03fcb875f56beddc4

```
More examples of `address _minipool` declarations:


**code/contracts/contract/minipool/RocketMinipoolManager.sol:L449-L455**



```
/// @dev Internal logic to set a minipool's pubkey
/// @param \_pubkey The pubkey to set for the calling minipool
function \_setMinipoolPubkey(address \_minipool, bytes calldata \_pubkey) private {
    // Load contracts
    AddressSetStorageInterface addressSetStorage = AddressSetStorageInterface(getContractAddress("addressSetStorage"));
    // Initialize minipool & get properties
    RocketMinipoolInterface minipool = RocketMinipoolInterface(\_minipool);

```
**code/contracts/contract/minipool/RocketMinipoolManager.sol:L474-L478**



```
function getMinipoolDetails(address \_minipoolAddress) override external view returns (MinipoolDetails memory) {
    // Get contracts
    RocketMinipoolInterface minipoolInterface = RocketMinipoolInterface(\_minipoolAddress);
    RocketMinipoolBase minipool = RocketMinipoolBase(payable(\_minipoolAddress));
    RocketNetworkPenaltiesInterface rocketNetworkPenalties = RocketNetworkPenaltiesInterface(getContractAddress("rocketNetworkPenalties"));

```
More examples of `RocketStorageInterface _rocketStorage` casts:


**code/contracts/contract/node/RocketNodeDistributor.sol:L8-L13**



```
contract RocketNodeDistributor is RocketNodeDistributorStorageLayout {
    bytes32 immutable distributorStorageKey;

    constructor(address \_nodeAddress, address \_rocketStorage) {
        rocketStorage = RocketStorageInterface(\_rocketStorage);
        nodeAddress = \_nodeAddress;

```
#### Recommendation


We recommend using more specific types instead of `address` where possible. Downcast if necessary. This goes for parameter types as well as state variable types.

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

