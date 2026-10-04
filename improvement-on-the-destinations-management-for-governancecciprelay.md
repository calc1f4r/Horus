---
# Core Classification
protocol: Cryptex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52945
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/cc661600-b854-49ec-8d9a-90d164b65f28
source_link: https://cdn.cantina.xyz/reports/cantina_cryptex_february2025.pdf
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
  - Anurag Jain
  - StErMi
---

## Vulnerability Title

Improvement on the destinations management for GovernanceCCIPRelay 

### Overview

See description below for full details.

### Original Finding Content

## GovernanceCCIPRelay Contract Review

## Context
(No context files were provided by the reviewer)

## Description
The `GovernanceCCIPRelay` contract will be the main and only relay deployed on mainnet that will relay all the messages to multiple destination chains. The current implementation of the contracts does only support one destination, meaning that Cryptex will need to deploy multiple instances of this contract, one for each destination chain. Given that this contract is not upgradable, when a fix needs to be applied or improvement has to be made, they will have to re-deploy it for every instance created. 

One possible improvement is to make `GovernanceCCIPRelay` more flexible and manage multiple whitelisted destination chains instead of just one, removing the requirement to deploy multiple instances of this contract.

## Recommendation
The following code is just for example’s sake and should be re-implemented and verified.

1. Remove the following `destinationReceiver` and `destinationChainSelector` state variables.
2. Remove the `setDestinationReceiver` setter.
3. Replace them with `mapping(uint64 destinationChainSelector => DestinationConfig) destinationConfigs;`.
4. Define `struct DestinationConfig` as follows:

    ```solidity
    struct DestinationConfig {
        uint64 destinationChainSelector;
        address destinationReceiver;
        uint256 gasLimit; // if zero use `200_000` which is the Chainlink default one as far as we know from their CCIP Documentation
        bool allowOutOfOrderExecution;
    }
    ```

5. Add all the setters needed to add/update/remove items from the `destinationConfigs`, and also add the needed getters.
6. Add `destinationChainSelector` as an input for `relayMessage` and revert if `destinationChainSelector` does not exist in `destinationConfigs`.
7. Add all the additional checks/requirements needed, like for example being able to pause relaying messages to a specific destination chain or specify different `gasLimit` or `allowOutOfOrderExecution` from the default one.

## Cryptex Implementation
Implemented in PR 169. Summary of changes:

- Added `mapping(uint64 => address) public destinationReceivers;` We don't need a struct as `gasLimit` is configured as a parameter in PR 172. Also, `allowOutOfOrderExecution` is always set to true. By setting it to true, we take it upon us that we don't need ordered execution for our use case.
- The function `addDestinationChains` has been added in place of `setDestinationReceiver` to add new chains.

## Cantina Managed
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Cryptex |
| Report Date | N/A |
| Finders | Anurag Jain, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_cryptex_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/cc661600-b854-49ec-8d9a-90d164b65f28

### Keywords for Search

`vulnerability`

