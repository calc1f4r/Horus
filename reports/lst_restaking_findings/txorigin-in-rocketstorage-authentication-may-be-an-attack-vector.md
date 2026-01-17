---
# Core Classification
protocol: Rocket Pool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16558
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf
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
finders_count: 3
finders:
  - Dominik Teiml
  - Devashish Tomar
  - Maximilian Krüger
---

## Vulnerability Title

tx.origin in RocketStorage authentication may be an attack vector

### Overview


This bug report involves a data validation issue in the RocketStorage contract. This contract contains functions that are protected by the onlyLatestRocketNetworkContract modifier, which has a switch that is disabled when the system is in the initialization phase. If the system is in the initialization phase, any call that originates from the guardian account will be trusted.

Exploit Scenario: Eve creates a malicious airdrop contract, and Alice, the Rocket Pool system’s guardian, calls it. The contract then calls RocketStorage and makes a critical storage update. After the updated value has been initialized, Alice sets storageInit to true, but the storage value set in the update persists, increasing the risk of a critical vulnerability.

Recommendations: In the short term, it is recommended to clearly document the fact that during the initialization period, the guardian may not call any external contracts; nor may any system contract that the guardian calls make calls to untrusted parties. In the long term, it is recommended to document all of the system’s assumptions, both in the portions of code in which they are realized and in all places in which they affect stakeholders’ operations.

### Original Finding Content

## Difficulty: Medium

## Type: Data Validation

## Description
The RocketStorage contract contains all system storage values and the functions through which other contracts write to them. To prevent unauthorized calls, these functions are protected by the `onlyLatestRocketNetworkContract` modifier.

```solidity
function setUint(bytes32 _key, uint _value) onlyLatestRocketNetworkContract override external {
    assembly {
        sstore (_key, _value)
    }
}
```
*Figure 6.1: RocketStorage.sol#L205-209*

The contract also contains a `storageInit` flag that is set to true when the system values have been initialized.

```solidity
function setDeployedStatus() external {
    // Only guardian can lock this down
    require(msg.sender == guardian, "Is not guardian account");
    // Set it now
    storageInit = true;
}
```
*Figure 6.2: RocketStorage.sol#L89-L94*

The `onlyLatestRocketNetworkContract` modifier has a switch and is disabled when the system is in the initialization phase.

```solidity
modifier onlyLatestRocketNetworkContract() {
    if (storageInit == true) {
        // Make sure the access is permitted to only contracts in our Dapp
        require(_getBool(keccak256(abi.encodePacked("contract.exists", msg.sender))),
        "Invalid or outdated network contract");
    } else {
        // Only Dapp and the guardian account are allowed access during initialization.
        // tx.origin is only safe to use in this case for deployment since no external
        contracts are interacted with
        require((
            tx.origin == guardian
            _getBool(keccak256(abi.encodePacked("contract.exists", msg.sender))) ||
        ), "Invalid or outdated network contract attempting access during deployment");
    }
    _;
}
```
*Figure 6.3: RocketStorage.sol#L36-L48*

If the system is still in the initialization phase, any call that originates from the guardian account will be trusted.

## Exploit Scenario
Eve creates a malicious airdrop contract, and Alice, the Rocket Pool system’s guardian, calls it. The contract then calls RocketStorage and makes a critical storage update. After the updated value has been initialized, Alice sets `storageInit` to true, but the storage value set in the update persists, increasing the risk of a critical vulnerability.

## Recommendations
- **Short term**: Clearly document the fact that during the initialization period, the guardian may not call any external contracts; nor may any system contract that the guardian calls make calls to untrusted parties.
- **Long term**: Document all of the system’s assumptions, both in the portions of code in which they are realized and in all places in which they affect stakeholders’ operations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Rocket Pool |
| Report Date | N/A |
| Finders | Dominik Teiml, Devashish Tomar, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf

### Keywords for Search

`vulnerability`

