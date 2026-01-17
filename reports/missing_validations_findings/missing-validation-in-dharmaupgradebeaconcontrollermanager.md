---
# Core Classification
protocol: Dharma Labs Smart Wallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16800
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
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
  - eric.rafaloﬀ@trailofbits.com Dominik Czarnota
  - Eric Rafaloﬀ
---

## Vulnerability Title

Missing validation in DharmaUpgradeBeaconControllerManager

### Overview

See description below for full details.

### Original Finding Content

## Data Validation

**Target:** DharmaSmartWalletImplementationV2.sol

**Difficulty:** Medium

## Description

Within the `DharmaUpgradeBeaconControllerManager` contract, the `armAdharmaContingency` function does not perform adequate validation of its controller and beacon address parameters (Figure 11.1).

```solidity
function armAdharmaContingency (
    address controller, 
    address beacon, 
    bool armed
) external {
    // Determine if 90 days have passed since the last heartbeat.
    (bool expired,) = heartbeatStatus();
    require(
        isOwner() || expired,
        "Only callable by the owner or after 90 days without a heartbeat."
    );
    // Arm (or disarm) the Adharma Contingency.
    _adharma[controller][beacon].armed = armed;
}
```

**Figure 11.1:** The armAdharmaContingency function.

## Exploit Scenario

Due to human error or a bug in a script, the `armAdharmaContingency` function is called with zero addresses, so the contract never becomes “armed” as was expected.

## Recommendation

- **Short term:** Validate that the controller and beacon address parameters are not zero.
- **Long term:** Add additional unit testing to check that invalid inputs are rejected from the `armAdharmaContingency` function.

© 2019 Trail of Bits  
Dharma Labs Smart Wallet Review | 23

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Dharma Labs Smart Wallet |
| Report Date | N/A |
| Finders | eric.rafaloﬀ@trailofbits.com Dominik Czarnota, Eric Rafaloﬀ |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf

### Keywords for Search

`vulnerability`

