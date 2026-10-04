---
# Core Classification
protocol: Revert Lend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32290
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-revert-lend
source_link: https://code4rena.com/reports/2024-03-revert-lend
github_link: https://github.com/code-423n4/2024-03-revert-lend-findings/issues/53

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
finders_count: 1
finders:
  - 0xjuan
---

## Vulnerability Title

[M-24] Incorrect liquidation fee calculation during underwater liquidation, disincentivizing liquidators to participate

### Overview


This bug report highlights an issue with the calculation of the liquidation fee in the Revert Lend protocol. The code currently calculates the fee as 10% of the full value of a position, instead of 10% of the debt as stated in the whitepaper. This means that as the full value decreases, the liquidation fee also decreases, which goes against the intended design of the protocol. The recommended mitigation steps involve changing the code to ensure the liquidation fee is always equal to 10% of the debt. The severity of this bug has been assessed as Medium, as it disrupts certain designs in the economic model. The bug has been confirmed and mitigated by the Revert team.

### Original Finding Content


As stated in the [Revert Lend Whitepaper](https://github.com/revert-finance/lend-whitepaper/blob/main/Revert_Lend-wp.pdf), the liquidation fee for underwater positions is supposed to be 10% of the debt. However, the code within `V3Vault::_calculateLiquidation` (shown below) calculates the liquidation fee as 10% of the `fullValue` rather than 10% of the `debt`.

```solidity
        } else {
            // all position value
            liquidationValue = fullValue;


            uint256 penaltyValue = fullValue * (Q32 - MAX_LIQUIDATION_PENALTY_X32) / Q32;
            liquidatorCost = penaltyValue;
            reserveCost = debt - penaltyValue;
        }
```

> Note: `fullValue * (Q32 - MAX_LIQUIDATION_PENALTY_X32) / Q32;` is equivalent to `fullValue * 90%`.

The code snippet is [here](https://github.com/code-423n4/2024-03-revert-lend/blob/main/src/V3Vault.sol#L1112-L1119).

### Impact

As the `fullValue` decreases below `debt` (since the position is underwater), liquidators are less-and-less incentivised to liquidate the position. This is because as `fullValue` decreases, the liquidation fee (10% of `fullValue`) also decreases.

This goes against the protocol's intention (stated in the whitepaper) that the liquidation fee will be fixed at 10% of the debt for underwater positions, breaking core protocol functionality.

### Proof of Concept

[Code snippet from `V3Vault._calculateLiquidation`](<https://github.com/code-423n4/2024-03-revert-lend/blob/435b054f9ad2404173f36f0f74a5096c894b12b7/src/V3Vault.sol#L1112-L1119>).

### Recommended Mitigation Steps

Ensure that the liquidation fee is equal to 10% of the debt. Make the following changes in `V3Vault::_calculateLiquidation()`:

```diff
else {
-// all position value
-liquidationValue = fullValue;


-uint256 penaltyValue = fullValue * (Q32 - MAX_LIQUIDATION_PENALTY_X32) / Q32;
-liquidatorCost = penaltyValue;
-reserveCost = debt - penaltyValue;

+uint256 penalty = debt * (MAX_LIQUIDATION_PENALTY_X32) / Q32; //[10% of debt]
+liquidatorCost = fullValue - penalty;
+liquidationValue = fullValue;
+reserveCost = debt - liquidatorCost; // Remaining to pay. 
}   
```

### Assessed type

Error

**[kalinbas (Revert) confirmed, but disagreed with severity and commented](https://github.com/code-423n4/2024-03-revert-lend-findings/issues/53#issuecomment-2021429312):**
 > Low severity.


**[ronnyx2017 (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2024-03-revert-lend-findings/issues/53#issuecomment-2028499772):**
 > According to the C4 rules, Medium is appropriate, as this disrupts certain designs in the economic model.

**[Revert mitigated](https://github.com/code-423n4/2024-04-revert-mitigation?tab=readme-ov-file#scope):**
> PR [here](https://github.com/revert-finance/lend/pull/7) - fixed calculation.

**Status:** Mitigation Confirmed. Full details in reports from [thank_you](https://github.com/code-423n4/2024-04-revert-mitigation-findings/issues/98), [b0g0](https://github.com/code-423n4/2024-04-revert-mitigation-findings/issues/57) and [ktg](https://github.com/code-423n4/2024-04-revert-mitigation-findings/issues/25).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Revert Lend |
| Report Date | N/A |
| Finders | 0xjuan |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-revert-lend
- **GitHub**: https://github.com/code-423n4/2024-03-revert-lend-findings/issues/53
- **Contest**: https://code4rena.com/reports/2024-03-revert-lend

### Keywords for Search

`vulnerability`

