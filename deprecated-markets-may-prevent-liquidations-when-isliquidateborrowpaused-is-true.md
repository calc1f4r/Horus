---
# Core Classification
protocol: Evoq
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45924
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2025-01-09-Evoq.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Deprecated Markets May Prevent Liquidations When isLiquidateBorrowPaused Is True

### Overview


This bug report discusses a medium severity issue in the EvoqGovernance contract. Currently, when a market is deprecated using the setIsDeprecated function, the contract checks to make sure borrowing is paused before applying the deprecation flag. However, there is no corresponding check for the isLiquidateBorrowPaused flag, which can prevent liquidators from liquidating borrowers in that market. This can lead to increased risk for the protocol. The recommendation is to modify the function to ensure that isLiquidateBorrowPaused is set to false when deprecating a market. The client has stated that this is intentional, but the recommendation is still to make the change for risk management purposes.

### Original Finding Content

**Severity**: Medium 

**Status**: Acknowledged 

**Context:**

**Contracts Involved:**

EvoqGovernance.sol
setIsDeprecated(address _poolToken, bool _isDeprecated)
EvoqGovernance.sol
setIsLiquidateBorrowPaused(address _poolToken, bool _isPaused)

**Description:** 

Currently, in the EvoqGovernance contract, when deprecating a market using the setIsDeprecated function, the contract ensures that borrowing is paused by checking isBorrowPaused before applying the deprecation flag. However, there is no corresponding check or logic to handle the isLiquidateBorrowPaused flag when a market is deprecated. This omission can lead to scenarios where a market is deprecated, but the isLiquidateBorrowPaused flag remains true, thereby preventing liquidators from liquidating borrowers in that deprecated market.

**Scenario:**

**Deprecating a Market:**

The contract owner calls setIsDeprecated(_poolToken, true) to deprecate a specific market.
The function checks that isBorrowPaused is true before allowing the deprecation.
The market is marked as deprecated by setting marketPauseStatus[_poolToken].isDeprecated = true.

**Impact on Liquidations:**

If isLiquidateBorrowPaused is already true for the deprecated market, liquidators are unable to liquidate borrowers in that market.
This situation undermines the protocol's risk management by allowing borrowers to maintain positions in a deprecated market without the ability to be liquidated, potentially leading to increased systemic risk.

**Recommendation:**

Modify the setIsDeprecated function to ensure that isLiquidateBorrowPaused is set to false when deprecating a market. This ensures that liquidations remain possible even after deprecation.

**Client comment:** 

This logic is intentional. Markets can be deprecated regardless of isLiquidateBorrowPaused is True or False. This gives operator more flexibility to pause/unpause liquidation borrow. For this reason, we prefer to leave things as it is.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Evoq |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2025-01-09-Evoq.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

