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
solodit_id: 61541
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
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
finders_count: 3
finders:
  - Benjamin Samuels
  - Priyanka Bose
  - Nicolas Donboly
---

## Vulnerability Title

Liquidation mechanism can be permanently disabled by misconﬁgured grace and expiry periods

### Overview


The Lender contract has a bug that can cause liquidations to never happen. This is because the contract does not check if the grace period is greater than or equal to the expiry period during initialization. This means that if the grace period is longer than the expiry period, liquidations will not be possible. This bug could lead to the protocol becoming insolvent due to accumulating bad debt. To fix this, the contract should be updated to ensure that the grace period is always shorter than the expiry period. In the long term, an emergency mechanism should be considered to allow authorized parties to reset critical parameters in case of misconfiguration.

### Original Finding Content

## Diﬃculty: Medium

## Type: Timing

## Description

The Lender contract does not check during initialization whether `grace >= expiry`. If `grace` is greater than or equal to `expiry`, liquidations will never happen.

```solidity
if (health >= 1e27) revert HealthFactorNotBelowThreshold();
if (emergencyHealth >= 1e27) {
    if (block.timestamp <= start + grace) revert GracePeriodNotOver();
    if (block.timestamp >= start + expiry) revert LiquidationExpired();
}
```
*Figure 18.1: Code snippet from `validateLiquidation` function (contracts/lendingPool/libraries/ValidationLogic.sol#L98-L102)*

As shown in figure 18.1, the `validateLiquidation` function requires `block.timestamp` to be both greater than `start + grace` and less than `start + expiry`, which is impossible when `grace >= expiry`. Since there is no way to reset the grace or expiry parameters after the contract is deployed, this misconfiguration would permanently disable the liquidation mechanism.

## Exploit Scenario

An admin deploys the Lender contract with a grace period of two days and an expiry period of one day. When an agent’s position becomes unhealthy and a liquidator initiates liquidation, the system will never allow the liquidation to be executed since the grace period exceeds the expiry period. This prevents timely liquidations and potentially results in protocol insolvency due to accumulating bad debt.

## Recommendations

- **Short term**: Add a validation check in the `initialize` function and any functions that update these parameters to ensure that `grace < expiry`.
  
- **Long term**: Consider implementing an emergency mechanism that allows authorized parties to reset critical parameters in case of misconfiguration.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

