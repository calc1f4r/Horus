---
# Core Classification
protocol: 0x Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17380
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf
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
finders_count: 4
finders:
  - Gustavo Grieco
  - Robert Tonic
  - Rajeev Gopalakrishna
  - Michael Colburn
---

## Vulnerability Title

Zero fee orders are possible if a user performs transactions with a zero gas price

### Overview


This bug report is about auditing and logging for Exchange contracts. It has been identified as a low difficulty issue. The bug occurs when users submit valid orders with a zero gas price, allowing them to avoid paying fees. This is because the calculation of fees for each transaction is performed in the calculateFillResults function, which uses the gas price selected by the user and the protocolFeeMultiplier coefficient.

The exploit scenario is that the Exchange governance decides to significantly increase the protocolFeeMultiplier to force the collection of higher fees. Alice does not want to pay the increased fees, so she decides to submit her transactions with a gas price equal to zero and process her own transactions as a miner, thus bypassing protocol fee collection.

The recommendation to address this issue is to select a reasonable minimum value for the protocol fee for each order or transaction in the short term. In the long term, the system should not depend on the gas price for the computation of protocol fees, as this would avoid giving miners an economic advantage in the system.

### Original Finding Content

## Auditing and Logging

**Type:** Auditing and Logging  
**Target:** Exchange contracts  

**Difficulty:** Low  

## Description

Users can submit valid orders and avoid paying fees if they use a zero gas price. The computation of fees for each transaction is performed in the `calculateFillResults` function. It uses the gas price selected by the user and the `protocolFeeMultiplier` coefficient.

```solidity
function calculateFillResults (
    LibOrder.Order memory order,
    uint256 takerAssetFilledAmount,
    uint256 protocolFeeMultiplier,
    uint256 gasPrice
)
    internal
    pure
    returns (FillResults memory fillResults)
{
    // Compute proportional transfer amounts
    fillResults.takerAssetFilledAmount = takerAssetFilledAmount;
    fillResults.makerAssetFilledAmount = LibMath.safeGetPartialAmountFloor(
        takerAssetFilledAmount,
        order.takerAssetAmount,
        order.makerAssetAmount
    );
    fillResults.makerFeePaid = LibMath.safeGetPartialAmountFloor(
        takerAssetFilledAmount,
        order.takerAssetAmount,
        order.makerFee
    );
    fillResults.takerFeePaid = LibMath.safeGetPartialAmountFloor(
        takerAssetFilledAmount,
        order.takerAssetAmount,
        order.takerFee
    );
    // Compute the protocol fee that should be paid for a single fill.
    fillResults.protocolFeePaid = gasPrice.safeMul(protocolFeeMultiplier);
    return fillResults;
}
```

_Figure 7.1: The calculateFillResults function._

Since the user completely controls the gas price of their transaction and the price could even be zero, the user could feasibly avoid paying fees.

## Exploit Scenario

The Exchange governance decides to significantly increase `protocolFeeMultiplier` to force the collection of higher fees. Alice does not want to pay increased fees, so she decides to submit her transactions with a gas price equal to zero and process her own transactions as a miner. As a result, she is able to bypass protocol fee collection.

## Recommendation

- **Short term:** Select a reasonable minimum value for the protocol fee for each order or transaction.
- **Long term:** Consider not depending on the gas price for the computation of protocol fees. This will avoid giving miners an economic advantage in the system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | 0x Protocol |
| Report Date | N/A |
| Finders | Gustavo Grieco, Robert Tonic, Rajeev Gopalakrishna, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf

### Keywords for Search

`vulnerability`

