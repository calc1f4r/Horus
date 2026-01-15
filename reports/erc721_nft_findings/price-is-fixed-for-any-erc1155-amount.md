---
# Core Classification
protocol: Limit Break
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37078
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-11-Limit Break.md
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

Price is fixed for any ERC1155 amount

### Overview


This report discusses a bug found in the CPortModule.sol code that affects the sale of ERC1155 tokens. The bug causes the buyer to pay the same price for any amount of tokens they request, regardless of the actual price. This is due to an error in the code that assigns the quantity of tokens before calculating the correct price. The recommended solution is to assign the quantity after calculating the price to ensure the correct amount is paid by the buyer. This bug has been resolved.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

CPortModule.sol - In the scenario of listing ERC1155 via protocol ERC1155_FILL_PARTIAL, the taker pays the same price for any requestedAmount they demand of a given tokenId.

This is because of a bug in the following code snippet:

```solidity
if (quantityToFill != saleDetails.amount) {
    saleDetails.amount = quantityToFill;
    saleDetails.itemPrice = saleDetails.itemPrice / saleDetails.amount * quantityToFill;
}
```
Occuring in functions: `_executeOrderBuySide()` & `_executeOrderSellSide()` and their overloads. As `saleDetails.amount` is assigned to quantityToFill before calculating the correct itemPrice that is to be proportional with the quantityToFill. According to this snippet the itemPrice is just fixed for any quantityToFill.

**Recommendation** 

saleDetails.amount should be assigned to quantityToFill after calculating the itemPrice that is to be paid by buyer.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Limit Break |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-11-Limit Break.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

