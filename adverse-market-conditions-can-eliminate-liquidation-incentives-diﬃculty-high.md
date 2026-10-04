---
# Core Classification
protocol: Opyn Gamma Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18169
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Opyn-Gamma-Protocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Opyn-Gamma-Protocol.pdf
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
finders_count: 2
finders:
  - Dominik Teiml
  - Mike Martel
---

## Vulnerability Title

Adverse market conditions can eliminate liquidation incentives Diﬃculty: High

### Overview


This bug report is about the MarginCalculator.sol contract for the Opyn Gamma Protocol. It has been identified as a high difficulty issue. The issue is that a naked margin vault can be liquidated as market conditions change and the amount of collateral required for a vault with a short position increases. Liquidation processes are carried out via auctions, with a maximum offer price equal to the amount of collateral in the delinquent vault. However, if the prevailing market price for a given option is equal to or in excess of the amount of collateral available at auction, other users may not be incentivized to liquidate the vault. This leaves the Gamma Protocol MarginPool with the obligation, even though it may no longer be secured by collateral. The current solution is to send assets via a donate function.

The exploit scenario is that Eve opens a partially collateralized vault holding an oToken that will be worth more than the current collateral amount when the token expires. Due to adverse market conditions, Eve's vault avoids liquidation and the oToken expires, allowing her to withdraw more funds from the Gamma Protocol MarginPool than she deposited into it.

The recommendations are to consider requiring margin users to pay fees to subsidize the default risk incurred by the Gamma Protocol in the short term, and to add mechanisms that can detect adverse market conditions and take automated actions to minimize their impact on system stability in the long term.

### Original Finding Content

## Type: Auditing and Logging
**Target:** contracts/core/MarginCalculator.sol

**Difficulty:** High

## Description
A naked margin vault can be liquidated as market conditions change and the amount of collateral required for a vault with a short position increases. Liquidation processes are carried out via auctions, with a maximum offer price equal to the amount of collateral in the delinquent vault.

However, if the prevailing market price for a given option is equal to or in excess of the amount of collateral available at auction, other users may not be incentivized to liquidate the vault. The oToken redeem function will still allow the system-wide MarginPool, which holds all collateral assets, to fulfill the obligation, even though the obligation may no longer be secured by collateral.

Currently, the only mechanism for correcting this type of imbalance involves sending assets via a donate function. Instead, Opyn could act as a liquidator of last resort.

## Exploit Scenario
Eve opens a partially collateralized vault holding an oToken that will be worth more than the current collateral amount when the token expires. Because of adverse market conditions such as a systemic price shock, extreme volatility spikes, or oToken illiquidity, Eve’s vault avoids liquidation, and the oToken expires. This allows Eve to withdraw more funds from the Gamma Protocol MarginPool than she deposited into it.

## Recommendations
**Short term**, consider requiring that margin users pay fees to subsidize the default risk incurred by the Gamma Protocol. With this requirement, the system would be similar to other DeFi systems that charge interest or stability fees when a user borrows funds.

**Long term**, consider adding mechanisms that can detect adverse market conditions and take automated actions to minimize those conditions’ impact on system stability.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Opyn Gamma Protocol |
| Report Date | N/A |
| Finders | Dominik Teiml, Mike Martel |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Opyn-Gamma-Protocol.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Opyn-Gamma-Protocol.pdf

### Keywords for Search

`vulnerability`

