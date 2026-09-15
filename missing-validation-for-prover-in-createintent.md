---
# Core Classification
protocol: Eco Inc
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46238
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/f4ef1cd6-860e-4f58-82de-09751baea324
source_link: https://cdn.cantina.xyz/reports/cantina_eco_december2024.pdf
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
finders_count: 3
finders:
  - 0xRajeev
  - 0xWeiss
  - phaze
---

## Vulnerability Title

Missing validation for prover in createIntent() 

### Overview

See description below for full details.

### Original Finding Content

## Code Review Summary

## Context
`IntentSource.sol#L59-L113`

## Description
The `createIntent()` function accepts a `_prover` address parameter without performing any validation to ensure it is a valid contract address that can prove intent fulfillment. This could lead to intents being created with invalid or non-existent prover addresses, potentially causing these intents to become unverifiable.

Furthermore, the prover's proof type is not included in the intent hash calculation, missing an opportunity to provide additional information about the intended proving mechanism. The `IProver` interface already defines proof types via the `ProofType` enum and includes a `getProofType()` function. Calling this function would serve both as validation of the prover contract's existence and interface compliance while also providing the proof type information that could be included in the intent hash.

## Recommendation
Consider adding prover validation through the `getProofType()` call and including the returned type in the intent hash:

### IntentSource
```solidity
function createIntent(
    uint256 _destinationChainID,
    address _inbox,
    address[] calldata _targets,
    bytes[] calldata _data,
    address[] calldata _rewardTokens,
    uint256[] calldata _rewardAmounts,
    uint256 _expiryTime,
    address _prover
) external payable {
    + // Fetch proof type - this will revert if prover is invalid
    + // or doesn't implement the interface correctly
    + IProver.ProofType proofType = IProver(_prover).getProofType();
    
    bytes32 intermediateHash = keccak256(abi.encode(
        CHAIN_ID,
        _destinationChainID,
        _targets,
        _data,
        _expiryTime,
        _nonce,
        _prover,
        + proofType
    ));
    
    bytes32 intentHash = keccak256(abi.encode(_inbox, intermediateHash));
    // ... rest of function ...
}
```

### Inbox
```solidity
function fulfillStorage(
    uint256 _sourceChainID,
    address[] calldata _targets,
    bytes[] calldata _data,
    uint256 _expiryTime,
    bytes32 _nonce,
    address _claimant,
    bytes32 _expectedHash,
    + IProver.ProofType _proofType
) external payable returns (bytes[] memory) {
    + if (_proofType != IProver.ProofType.Storage) {
    + revert InvalidProverType();
    + }
    // ... rest of function with _proofType included in hash verification ...
}

function fulfillHyperInstant(
    // ... existing parameters ...
    + IProver.ProofType _proofType
) external payable returns (bytes[] memory) {
    + if (_proofType != IProver.ProofType.Hyperlane) {
    + revert InvalidProverType();
    + }
    // ... rest of function with _proofType included in hash verification ...
}
```

### Summary of Changes
1. Validates the prover type on the source chain during intent creation.
2. Includes the proof type in the intent hash.
3. Validates the proof type matches the fulfillment method on the destination chain.

## Eco
Acknowledged. We don't think this change would result in any different behavior from the solver. It is not enough to know that the prover exists or implements the correct interface—the solver must be sure that the prover works as expected, and they can be assured of this either by inspection or by ensuring that the prover's address matches one that we published. Given that inspecting the prover yields the proof type and that our published address list will arrange provers by proof type, we do not feel that this change is necessary.

## Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Eco Inc |
| Report Date | N/A |
| Finders | 0xRajeev, 0xWeiss, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_eco_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/f4ef1cd6-860e-4f58-82de-09751baea324

### Keywords for Search

`vulnerability`

