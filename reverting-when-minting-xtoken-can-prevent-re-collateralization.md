---
# Core Classification
protocol: AladdinDAO f(x) Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31044
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
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
  - Troy Sargent
  - Robert Schneider
---

## Vulnerability Title

Reverting when minting xToken can prevent re-collateralization

### Overview

This bug report discusses a problem with the treasury function in the AladdinDAO f(x) protocol. The issue occurs when the protocol is in "stability mode" and needs to incentivize the minting of xToken to re-collateralize above 130%. However, the current design does not always allow for the minting of xToken, even though it is necessary for the protocol to recover. This can cause the protocol to collapse. To fix this, the report suggests allowing for the minting of xToken at a conservative price during stability mode and implementing testing to ensure certain actions always succeed.

### Original Finding Content

## Diﬃculty: High

## Type: Undefined Behavior

### Target: 
contracts/f(x)/v2/TreasuryV2.sol

## Description
When the treasury processes the `mintXToken` action, it validates that the oracle price is valid, and, if invalid, it reverts. During stability mode (collateral ratio between 100% and 130%), the protocol is designed to recover by incentivizing the minting of xToken in order to re-collateralize above 130%. Minting xToken may fail, even though it is necessary to recover from stability mode, and cause the protocol to collapse. Instead, the protocol could always permit the minting of xToken during stability mode and handle invalid prices by conservatively pricing the collateral and favoring the protocol’s credit risk health at the expense of the user minting.

```solidity
if (_action == Action.MintFToken || _action == Action.MintXToken) {
    if (!_isValid) revert ErrorInvalidOraclePrice();
}
```

*Figure 18.1: Minting xToken fails if the price is considered invalid (aladdin-v3-contracts/contracts/f(x)/v2/TreasuryV2.sol#648–649)*

## Recommendations
- **Short term**: Consider allowing minting of xToken at a conservative price when the protocol is in stability mode.
- **Long term**: Identify actions that should never fail to succeed, such as those relevant to re-collateralizing the protocol, and implement invariant testing that ensures that they always succeed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | AladdinDAO f(x) Protocol |
| Report Date | N/A |
| Finders | Troy Sargent, Robert Schneider |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

