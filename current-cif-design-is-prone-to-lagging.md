---
# Core Classification
protocol: Buck Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64795
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Buck-Labs-Spearbit-Security-Review-January-2026.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Buck-Labs-Spearbit-Security-Review-January-2026.pdf
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
  - R0bert
  - Sujith Somraaj
  - T1moh
---

## Vulnerability Title

Current CIF design is prone to lagging

### Overview


This bug report discusses a medium risk issue with a function called `publishAttestation()` in a smart contract called `CollateralAttestationV2.sol`. The function is used to update a variable called `V` and is expected to be called by an admin. However, there is a problem with how another variable called `cashInFlight` is updated, which can lead to an overestimation of the total assets and an incorrect calculation of the collateral ratio. This can result in a less strict price cap check and potential price fluctuations. The recommendation is to update `cashInFlight` in the same transaction as `publishAttestation()`, but the team acknowledges that this may not completely solve the issue. They also mention that this bug will only have a significant impact when the collateral ratio is below the price, which is not currently the case.

### Original Finding Content

## Severity: Medium Risk

## Context
- `CollateralAttestationV2.sol#L201-L205`
- `CollateralAttestationV2.sol#L241-L249`
- `CollateralAttestationV2.sol#L254-L257`

## Description
`cashInFlow` was introduced to reflect funds that are no longer in `LiquidityReserve`, but not yet in Alpaca Finance (V) and vice versa. V is updated in the function `publishAttestation()`:

```solidity
function publishAttestation(uint256 _V, uint256 _HC, uint256 _attestedTimestamp) external onlyRole(ATTESTOR_ROLE) {
    // ...
    V = _V; // <<<
    HC = _HC;
    lastAttestationTime = block.timestamp;
    attestationMeasurementTime = _attestedTimestamp;
}
```

The admin is expected to call the function `setCashInFlight()` to decrease `cashInFlight`:

```solidity
/// @notice Set cash-in-flight amount (admin clears when cash arrives)
/// @param amount New CIF amount (18 decimals) - typically 0 to clear // <<<
function setCashInFlight(uint256 amount) external onlyRole(ADMIN_ROLE) {
    cashInFlight = amount;
    emit CashInFlightSet(amount);
}
```

Here is how the admin is expected to update `cashInFlight`:

- **CIF Flow (works for BOTH directions)**:
  - Outgoing (Reserve → Alpaca): `LiquidityReserve` calls `addCashInFlight()` on withdrawal
  - Incoming (Alpaca → Reserve): Admin calls `addCashInFlight()` when dividend wire initiated
  - Admin clears CIF via `setCashInFlight(0)` when cash arrives at destination

Such behavior introduces a situation where `cashInFlight` is overestimated:
- Alpaca → Reserve: When wire is initiated, V is old, but the amount is already added to `cashInFlight`.
- Alpaca → Reserve: When V is new, funds have arrived, but the amount is still in `cashInFlight`.
- Reserve → Alpaca: When V is new, but the amount is still in `cashInFlight`.

It means that `totalAssets` is higher than the actual value and therefore it overestimates the `Collateral Ratio`. This means that the price cap check is less strict:

```solidity
function _computeCAPPrice() internal view returns (uint256 price) {
    // ...
    // Cap by collateral ratio if undercollateralized
    uint256 cr = getCollateralRatio();
    if (cr < price) {
        price = cr;
    }
    return price;
}
```

If cap check indeed limits the price, then in that period price will instantly drop. And again, instantly rise after admin action.

## Recommendation
It's hard to solve the issue completely. Intuitively, it should update `cashInFlight` in the same transaction as `publishAttestation()`. But this way lagging is still possible on Alpaca → Reserve, when USDC has already arrived but `cashInFlight` is not decreased.

**Buck Labs:** Acknowledged. There's not much we can do about it. Operationally, we need it in order for our status to stay “collateralized” while moving money around. The good news is that it only matters when the CR is < price. Right now we're (truly, no CIF) over-collateralized at a 1.68 ratio, which will continue to shrink as we grow, but it keeps a healthy enough buffer so that the scenario where we face this is rare until we're above like, 100M market cap or something. 

Anyways, if we're near under-collateralization, we'll be at a heightened operational posture and manually coordinating attestations and cash in flight transactions carefully.

**Cantina Managed:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Buck Labs |
| Report Date | N/A |
| Finders | R0bert, Sujith Somraaj, T1moh |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Buck-Labs-Spearbit-Security-Review-January-2026.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Buck-Labs-Spearbit-Security-Review-January-2026.pdf

### Keywords for Search

`vulnerability`

