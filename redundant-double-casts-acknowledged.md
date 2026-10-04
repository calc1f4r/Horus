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
solodit_id: 13215
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

Redundant double casts  Acknowledged

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



The client acknowledges the finding and provided the following statement:



> 
> Acknowledged. These contracts are non-upgradable.
> 
> 
> 




#### Description


`_rocketStorageAddress`  is already of contract type `RocketStorageInterface`.


**code/contracts/contract/RocketBase.sol:L78-L82**



```
/// @dev Set the main Rocket Storage address
constructor(RocketStorageInterface \_rocketStorageAddress) {
    // Update the contract address
    rocketStorage = RocketStorageInterface(\_rocketStorageAddress);
}

```
`_tokenAddress`  is already of contract type `ERC20Burnable`.


**code/contracts/contract/RocketVault.sol:L132-L138**



```
function burnToken(ERC20Burnable \_tokenAddress, uint256 \_amount) override external onlyLatestNetworkContract {
    // Get contract key
    bytes32 contractKey = keccak256(abi.encodePacked(getContractName(msg.sender), \_tokenAddress));
    // Update balances
    tokenBalances[contractKey] = tokenBalances[contractKey].sub(\_amount);
    // Get the token ERC20 instance
    ERC20Burnable tokenContract = ERC20Burnable(\_tokenAddress);

```
`_rocketTokenRPLFixedSupplyAddress` is already of contract type `IERC20`.


**code/contracts/contract/token/RocketTokenRPL.sol:L47-L51**



```
constructor(RocketStorageInterface \_rocketStorageAddress, IERC20 \_rocketTokenRPLFixedSupplyAddress) RocketBase(\_rocketStorageAddress) ERC20("Rocket Pool Protocol", "RPL") {
    // Version
    version = 1;
    // Set the mainnet RPL fixed supply token address
    rplFixedSupplyContract = IERC20(\_rocketTokenRPLFixedSupplyAddress);

```
#### Recommendation


We recommend removing the unnecessary double casts and copies of local variables.

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

