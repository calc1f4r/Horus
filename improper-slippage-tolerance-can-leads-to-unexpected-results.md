---
# Core Classification
protocol: Paribus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37389
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-Paribus.md
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

Improper slippage tolerance can leads to unexpected results

### Overview


This bug report discusses an issue with the `FlashloanLiquidator.executeOperation` function. This function is used for liquidating a debt position and can only be triggered by an Aave pool after receiving a flash loan. The problem is that if a user chooses to receive underlying tokens as a reward, the function may not provide any reward if the price is manipulated. Similarly, if the user wants a specific asset as a reward, they may receive less than expected due to potential manipulation of the underlying pool. The recommendation is to allow users to set their own slippage tolerance, which would be a percentage value of the swapped assets. This would help prevent these issues from occurring.

### Original Finding Content

**Severity**: Medium

**Status**:  Resolved

**Description**

The `FlashloanLiquidator.executeOperation` function is called when a flash loan is made and can only be triggered by an Aave pool after receiving flashloan. The purpose of this function is to perform the liquidation of a specified debt position, which was previously calculated by getting a price from a Chainlink feed. 
If the user chooses to get underlying tokens as reward, the function swaps the amount intended to repay the debt, allowing for providing the entire seized amount as an input amount during the swap. This can result in no reward for a liquidator if the price is manipulated. 
Alternatively, If the user wants  to get an choosen asset as a reward, the function swaps all the flash loaned assets, setting the amountOutMin parameter as totalDebt + 1. However, due to potential  manipulation of the underlying pool, liquidators may receive fewer assets than expected.

**Recommendation**: 

In both cases users should be able to provide their own slippage tolerance, set as a percentage value of swapped assets.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Paribus |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-Paribus.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

