---
# Core Classification
protocol: Ludex Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52930
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/82ea7f9c-0383-45e9-9630-5863839fa2c5
source_link: https://cdn.cantina.xyz/reports/cantina_riskiit_february2025.pdf
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
finders_count: 2
finders:
  - Cryptara
  - r0bert
---

## Vulnerability Title

Default Provider’s endSequenceNumber Can Lead to Permanent DoS and Sequence Collisions with New Providers 

### Overview


The Pyth Entropy contract has a bug where the same default provider is always used, causing a permanent denial of service for new requests. This can be fixed by updating the contract to use a different provider and ensuring that the sequence number starts higher than any previously used number. It is also recommended to use a unique game key that includes both the provider's address and the sequence number in the games mapping to avoid conflicts. This bug has been fixed in PR 50 by Ludex Labs and has been verified by Cantina Managed.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
In the Pyth Entropy contract, each provider has a finite hash-chain length defined by `endSequenceNumber`. Specifically:

```solidity
uint64 assignedSequenceNumber = providerInfo.sequenceNumber;
if (assignedSequenceNumber >= providerInfo.endSequenceNumber)
    revert EntropyErrors.OutOfRandomness();
providerInfo.sequenceNumber += 1;
```

- As the `RiskItV1_1` contract always uses the same “default provider,” eventually `providerInfo.sequenceNumber` will reach `endSequenceNumber`, causing any new requests to revert with `OutOfRandomness()`. This triggers a permanent DoS on new spins unless the `RiskItV1_1` contract updates its provider.
  
- If then the contract updates to a different provider, it must ensure its `sequenceNumber` starts higher than any previously used sequence number. Otherwise, `RiskItV1_1` might collide with `existing games[sequenceNumber]` reverting with `GameAlreadyResolved` if it sees a repeated `sequenceNumber` from a different provider. Because `RiskItV1_1` indexes games solely by the `sequenceNumber` and doesn’t store “(provider, sequenceNumber)” as a composite key, reusing the same sequence number from a new provider leads to conflicts or reverts.

## Recommendation
- Extend or rotate the provider’s hash chain before reaching `endSequenceNumber`. The provider can call `register` with a fresh chain or use a rotation mechanism to avoid the `OutOfRandomness` revert.
  
- Use a unique game key that includes both the provider’s address and the sequence number in the games mapping, e.g. `games[keccak256(provider, seqNum)]`. That way, different providers can reuse `sequenceNumbers` without colliding.

## Actions Taken
- **Ludex Labs**: Fixed in PR 50.
  
- **Cantina Managed**: Fix ok. A unique game key that includes both the provider’s address and the sequence number is used now in the games mapping.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Ludex Labs |
| Report Date | N/A |
| Finders | Cryptara, r0bert |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_riskiit_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/82ea7f9c-0383-45e9-9630-5863839fa2c5

### Keywords for Search

`vulnerability`

