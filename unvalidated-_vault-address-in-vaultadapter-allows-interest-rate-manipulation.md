---
# Core Classification
protocol: CAP Labs Covered Agent Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61535
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
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
  - Benjamin Samuels
  - Priyanka Bose
  - Nicolas Donboly
---

## Vulnerability Title

Unvalidated _vault address in VaultAdapter allows interest rate manipulation

### Overview


This report describes a bug in the `VaultAdapter.rate` function, which accepts an unvalidated address and makes external calls to it without verifying its legitimacy. This can be exploited by an attacker who supplies a malicious contract as the address, allowing them to manipulate critical storage values that determine interest rates. This can cause borrowers to pay excessive interest. To fix this issue, it is recommended to implement access control or an allowlist mechanism in the short term, and add comprehensive input validation in the long term.

### Original Finding Content

## Diﬃculty: Medium

## Type: Data Validation

## Description
The `VaultAdapter.rate` function accepts an unvalidated `_vault` address and makes external calls to it without verifying that it is a legitimate vault. An attacker can supply a malicious contract as the vault address, which would allow manipulation of critical storage values (`$.utilizationData[_asset].index`, `$.utilizationData[_asset].lastUpdate`, and `$.utilizationData[_asset].utilizationMultiplier`) that determine interest rates throughout the protocol, as shown in Figure 12.1.

```solidity
function rate(address _vault, address _asset) external returns (uint256 latestAnswer) {
    VaultAdapterStorage storage $ = getVaultAdapterStorage();
    uint256 elapsed;
    uint256 utilization;
    if (block.timestamp > $.utilizationData[_asset].lastUpdate) {
        uint256 index = IVault(_vault).currentUtilizationIndex(_asset);
        elapsed = block.timestamp - $.utilizationData[_asset].lastUpdate;
        /// Use average utilization except on the first rate update
        if (elapsed != block.timestamp) {
            utilization = (index - $.utilizationData[_asset].index) / elapsed;
        } else {
            utilization = IVault(_vault).utilization(_asset);
        }
        $.utilizationData[_asset].index = index;
        $.utilizationData[_asset].lastUpdate = block.timestamp;
    } else {
        utilization = IVault(_vault).utilization(_asset);
    }
    latestAnswer = _applySlopes(_asset, utilization, elapsed);
}
```

**Figure 12.1:** `contracts/oracle/libraries/VaultAdapter.sol#L26-L49`

## Exploit Scenario
An attacker deploys a malicious contract implementing the `IVault` interface. They call the `VaultAdapter.rate` function with their malicious contract as the `_vault` parameter, which returns crafted values from the `currentUtilizationIndex` and `utilization` methods. This manipulates storage values in `VaultAdapter`, artificially inflating interest rates returned by `_applySlopes`. The inflated rates propagate through `RateOracle.utilizationRate` to `InterestDebtToken.nextInterestRate`, causing borrowers to pay excessive interest.

## Recommendations
- **Short term:** Implement access control on the `rate` function or add an allowlist mechanism to validate vault addresses before making external calls to them.
- **Long term:** Add comprehensive input validation throughout the codebase to prevent similar issues in other functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | CAP Labs Covered Agent Protocol |
| Report Date | N/A |
| Finders | Benjamin Samuels, Priyanka Bose, Nicolas Donboly |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

