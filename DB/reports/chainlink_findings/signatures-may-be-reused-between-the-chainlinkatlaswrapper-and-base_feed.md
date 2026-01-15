---
# Core Classification
protocol: Fastlane Atlas
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36826
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
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
  - Riley Holterhus
  - Blockdev
  - Gerard Persoon
---

## Vulnerability Title

Signatures may be reused between the ChainlinkAtlasWrapper and BASE_FEED

### Overview

See description below for full details.

### Original Finding Content

## Security Report

## Severity
Low Risk

## Context
ChainlinkAtlasWrapper.sol#L77-L82

## Description
The ChainlinkAtlasWrapper is intended to be a wrapper of the Chainlink BASE_FEED contract, with the two contracts potentially sharing the same signers and transmitters. Since both contracts have the same arguments and verification logic in the `transmit()` function, it seems that the report and corresponding signatures for one contract can also be used in the other contract. This may not be intended and may add a trust assumption that the transmitter relays information to the correct contract that the signers are expecting.

## Recommendation
Consider adding specific logic in the ChainlinkAtlasWrapper that ensures the submitted report would not also be valid in the BASE_FEED. For example, this can be accomplished by enforcing that `rawObservers` from the following code is equal to `bytes32(0)`:

```solidity
(r.rawReportContext, rawObservers, r.observations) = abi.decode(
    _report, 
    (bytes32, bytes32, int192[])
);
```

This would work because the BASE_FEED would interpret this value as duplicate zero indices (which leads to a revert if there's more than one signer), while the `rawObservers` is otherwise unused in the ChainlinkAtlasWrapper. Therefore, it would be impossible to have one report be valid in both contracts if it was required that `rawObservers == bytes32(0)` in the ChainlinkAtlasWrapper.

## Fastlane
Acknowledged. The issue with using a special `rawObservers` value (or any special change that would break the normal verification of the transmission in the base Chainlink contract) is that this changes the report data, and the hash of the report is what the Chainlink nodes sign when submitting a new price observation. Each signer would need to re-sign a price specifically intended for the Atlas OEV system. So while this would be better security, it would be a more onerous burden on the Chainlink system to enable OEV capture through Atlas. As mentioned in this issue, both the Chainlink and Atlas `transmit()` functions are permissioned, so there are some trust assumptions to fall back on. 

Will acknowledge and leave the related code as it is for now, but in the case that Chainlink nodes are willing to sign special Atlas price observations as well as their usual Chainlink ones, we will implement this safeguard.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Fastlane Atlas |
| Report Date | N/A |
| Finders | Riley Holterhus, Blockdev, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf

### Keywords for Search

`vulnerability`

