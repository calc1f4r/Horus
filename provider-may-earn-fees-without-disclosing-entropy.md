---
# Core Classification
protocol: Pyth Data Association Entropy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37883
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf
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
  - Tjaden Hess
  - Elvis Skoždopolj
---

## Vulnerability Title

Provider may earn fees without disclosing entropy

### Overview

See description below for full details.

### Original Finding Content

## Target: Entropy.sol

## Description

Entropy providers may set a configurable fee as compensation for providing the entropy. However, they may collect the fee without disclosing their entropy to the user and thus collect fees simply by registering once and then going offline. Users must pay the provider fee as part of submitting a request, at which point the funds are immediately available for withdrawal by the provider, as demonstrated in figure 12.1.

```solidity
function request (
    address provider,
    bytes32 userCommitment,
    bool useBlockHash
) public payable override returns (uint64 assignedSequenceNumber) {
    ...
    // Check that fees were paid and increment the pyth / provider balances.
    uint128 requiredFee = getFee(provider);
    if (msg.value < requiredFee) revert EntropyErrors.InsufficientFee();
    providerInfo.accruedFeesInWei += providerInfo.feeInWei;
    _state.accruedPythFeesInWei += (SafeCast.toUint128(msg.value) - providerInfo.feeInWei);
    ...
}
```

Figure 12.1: Fees are credited immediately upon submission of a request.  
( pyth-crosschain/target_chains/ethereum/contracts/contracts/entropy/Entropy.sol#176–198 )

Because fees are credited to the provider immediately, there is little financial incentive to keep the Fortuna service online.

## Exploit Scenario

Alice registers a provider with the Entropy service, setting a 0.01 ETH fee for entropy. As a cost-saving measure, Alice does not pay for redundant or high-availability hosting infrastructure for the Fortuna service. An NFT protocol uses Alice as the entropy provider for a randomized mint. Alice’s Fortuna server goes down for several hours, causing users to miss the 256-block revelation window for block hash–based entropy. Alice, however, still collects the fees from the randomness that she never provided.

## Recommendations

- Short term: Lock user funds upon submission of a request, but credit the funds to the provider only upon completion of the reveal operation.
- Long term: Consider allowing providers to submit entropy seeds on their own behalf and collect fees if the user goes offline.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Pyth Data Association Entropy |
| Report Date | N/A |
| Finders | Tjaden Hess, Elvis Skoždopolj |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf

### Keywords for Search

`vulnerability`

