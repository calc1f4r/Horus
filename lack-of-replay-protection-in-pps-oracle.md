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
solodit_id: 63079
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Superform-v2-periphery-Spearbit-Security-Review-June-2025.pdf
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
finders_count: 5
finders:
  - MiloTruck
  - Christoph Michel
  - Ethan
  - Noah Marconi
  - Ladboy233
---

## Vulnerability Title

Lack of replay protection in PPS oracle

### Overview


This bug report highlights a security vulnerability in the `ECDSAPPSOracle` signature schema. The lack of a nonce in the schema makes it susceptible to replay attacks, which can disrupt the share accounting in `SuperVault` and `SuperVaultStrategy`. The report recommends updating the message hash computation and utilizing `_domainSeparatorV4()` before signing to include `block.chainid` and `address(this)` in the signature schema. This will help mitigate the vulnerability.

### Original Finding Content

## Security Analysis Report

## Severity: High Risk

### Context
`ECDSAPPSOracle.sol#L127-L147`

### Description
The `ECDSAPPSOracle` signature schema does not include a nonce, which makes it vulnerable to replay attacks once enough validators (more than the `quorumRequirement`) sign the price update. A malicious user can exploit this by pushing an outdated PPS price, thereby disrupting the share accounting in both `SuperVault` and `SuperVaultStrategy` through signature replay.

- Create message hash with all parameters:
  - If any are incorrect, the message hash will differ, and the derived signer address will be incorrect, resulting in a revert.

```solidity
bytes32 messageHash = keccak256(abi.encodePacked(strategy, pps, ppsStdev, validatorSet, totalValidators, timestamp));
bytes32 ethSignedMessageHash = messageHash.toEthSignedMessageHash();
```

Additionally, the signature schema lacks `block.chainid` and `address(this)`. If the strategy address is deployed across two blockchains, a malicious user can again push the outdated PPS price and break the share accounting in `SuperVault` and `SuperVaultStrategy` via a cross-chain signature replay.

### Recommendation
To mitigate this vulnerability, update the message hash computation as follows:

```solidity
// Existing code
bytes32 messageHash = keccak256(abi.encodePacked(strategy, pps, ppsStdev, validatorSet, totalValidators, timestamp));

// Recommended update
bytes32 messageHash = keccak256(abi.encodePacked(strategy, pps, ppsStdev, validatorSet, totalValidators, timestamp, nonces++));
```

Before signing, utilize `_domainSeparatorV4()` to include `block.chainid` and `address(this)` in the signature schema.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

