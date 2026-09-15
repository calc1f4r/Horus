---
# Core Classification
protocol: Superform v2 Periphery
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63093
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf
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
finders_count: 5
finders:
  - MiloTruck
  - Christoph Michel
  - Ethan
  - Noah Marconi
  - Ladboy233
---

## Vulnerability Title

Issues with CREATE2 salt in SuperVaultAggregator.createVault()

### Overview


This report discusses a medium risk vulnerability in the `SuperVaultAggregator` contract. The `createVault()` function deploys contracts using a CREATE2 salt that is based on the parameters and current nonce. However, there are two issues with this implementation. First, using `abi.encodePacked()` can result in collisions when concatenating `name` and `symbol` parameters. Second, not including `msg.sender` in the salt allows different users to deploy contracts to the same address, leading to potential front-running attacks. The recommendation is to use `abi.encode()` instead and to include `msg.sender` in the salt to prevent these issues.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
`SuperVaultAggregator.sol#L128-L137`

## Description
The `SuperVaultAggregator.createVault()` function deploys contracts with a CREATE2 salt as the hash of their parameters and the current nonce. The implementation is as follows:

```solidity
// Create minimal proxies
superVault = VAULT_IMPLEMENTATION.cloneDeterministic(
    keccak256(abi.encodePacked(params.asset, params.name, params.symbol, currentNonce))
);
escrow = ESCROW_IMPLEMENTATION.cloneDeterministic(
    keccak256(abi.encodePacked(params.asset, params.name, params.symbol, currentNonce))
);
strategy = STRATEGY_IMPLEMENTATION.cloneDeterministic(
    keccak256(abi.encodePacked(params.asset, params.name, params.symbol, currentNonce))
);
```

However, there are two issues with this implementation:

1. Using `abi.encodePacked()` could cause collisions in the concatenation of `name` and `symbol`. For example, `abi.encodePacked("AA", "B")` and `abi.encodePacked("A", "AB")` produce the same output.
   
2. Not including `msg.sender` in the salt allows different users to deploy vaults, escrows, or strategies to the same address. This can lead to a problem where a user batches a transaction to `createVault()` alongside another transaction that interacts with the newly deployed contracts. An attacker could front-run the vault deployment and alter its parameters.

### Example Scenario
- Bob batches two transactions:
  - Calls `createVault()` to deploy a vault with `mainStrategist` set to himself. This deploys a vault at address `0x123....`
  - Calls `SuperVault.deposit()` to deposit into the vault at `0x123....`
  
- Alice front-runs his transactions, calling `createVault()` with the same parameters, but with `mainStrategist` set to her address.
  
- Alice's transaction deploys the vault at `0x123....`

- When Bob's transactions are executed, he inadvertently deposits into the vault where Alice is the `mainStrategist`, instead of himself.

## Recommendation
1. Use `abi.encode()` to pack arguments.
2. Include `msg.sender` in the salt.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Superform v2 Periphery |
| Report Date | N/A |
| Finders | MiloTruck, Christoph Michel, Ethan, Noah Marconi, Ladboy233 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf

### Keywords for Search

`vulnerability`

