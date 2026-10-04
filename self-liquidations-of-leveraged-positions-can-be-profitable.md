---
# Core Classification
protocol: Euler Labs - EVK
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35944
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-EVK-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-EVK-April-2024.pdf
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
finders_count: 5
finders:
  - Christos Pap
  - M4rio.eth
  - Christoph Michel
  - David Chaparro
  - Emanuele Ricci
---

## Vulnerability Title

Self-liquidations of leveraged positions can be profitable

### Overview


This bug report discusses a high-risk vulnerability in the Liquidation.sol code, specifically at line 127. The bug allows an attacker to manipulate the price oracle and profit from a leveraged position by sandwiching a price update. This can be done by taking a flashloan, max-borrowing the debt token, and then performing the price update before liquidating themselves. The attack is profitable when the collateral balance is seized to repay the flashloan, while repaying less debt assets than borrowed. This difference is the profit. The attack is also risk-free if using oracle adapters like Redstone and Pyth, as the user can update or choose the price. This can be done in a single transaction batch. The attack can be made more profitable by using smaller liquidations and can leave bad debt for the protocol. The report provides an example of how the attack can be performed and the calculations for determining profitability. 

### Original Finding Content

## High Risk Vulnerability in Liquidation.sol

**Severity:** High Risk  
**Context:** Liquidation.sol#L127  
**Description:** An attacker can perform the following attack by sandwiching a price oracle update:

1. Taking on a leveraged position by flashloaning collateral and max-borrowing the debt token.
2. Performing the price update.
3. Liquidating themselves (from another subaccount).

**Profitability:** The attack is profitable when the entire collateral balance is seized (to repay the flashloan) while repaying fewer debt assets than assets that were borrowed. This difference of maxBorrowAssets - maxRepayAssets of debt assets is the profit.

### Calculations
- **Discount Factor:** `df = 1 - discount`
- **Collateral Price Before Update:**  
  `collateralPrice_0 = price before the oracle update`
  
- **Collateral Price After Update:**  
  `collateralPrice_1 = collateralPrice_0 * (1 - priceDrop)`

- **Maximum Debt Asset Borrowed:**  
  `maxBorrowAssets = LTV_borrow * collateralBalance * collateralPrice_0 / debtPrice`

- **Seized Assets Calculation:**  
  `seizedAssets = repayValue / discountFactor / collateralPrice_1`  
  `= (repayAssets * debtPrice) / discountFactor / collateralPrice_1`

- **Maximum Repay Assets for Seizing Full Collateral Balance:**  
  `maxRepayAssets = collateralBalance * discountFactor * collateralPrice_1 / debtPrice`

- **Profitability Condition:**  
  Profitable if the following inequality holds:  
  `maxBorrowAssets > maxRepayAssets`  
  `LTV_borrow * collateralBalance * collateralPrice_0 / debtPrice > collateralBalance * discountFactor * collateralPrice_1 / debtPrice`  
  `<=> LTV_borrow > discountFactor * (1 - priceDrop)`

**Note:** The discount factor is set to `max(hs_liquidation, 0.8)`. The attack is profitable if an attacker can sandwich a price oracle update that would result in `LTV_borrow > discountFactor * (1 - priceDrop)`.

Some oracle adapters, like Redstone and Pyth, allow users to update or even choose a preferable price. In this case, the attack could even be performed in a single transaction batch for risk-free profit.

### Additional Note
Using several smaller liquidations can increase the overall liquidation discount and lead to a more profitable attack. A profitable attack also leaves bad debt for the protocol.

See this Notebook for further profitability analysis.

### Example
- **LTV_borrow = LTV_liquidation = 90%**
- **Oracle quotes 1 collateral at $1 (and debt is fixed at $1)**

**Steps to Execute:**

1. Sandwich collateral oracle price update to $0.90:
   1. Flashloan 1000 collateral and build a position of (1000 collateral, 900 debt) at `LTV_borrow`.
   2. Oracle sets collateral price to $0.90. (e.g., Redstone / Pyth require the user to trigger the update.)
   3. Liquidate self by repaying `maxRepayAssets = 810`.

- **Discount Factor Calculation:**  
  `discountFactor = healthscore_liquidation = collateralBalance * collateralPrice_1 * LTV_liquidation / debtValue = 0.90`

- **Calculated Values:**
  - `maxBorrowAssets: 900`
  - `maxRepayAssets: 810`
  - `seizedAssets: maxRepayAssets * debtPrice / discountFactor / collateralPrice_1 = 810D * 1$/D / 0.9`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Euler Labs - EVK |
| Report Date | N/A |
| Finders | Christos Pap, M4rio.eth, Christoph Michel, David Chaparro, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-EVK-April-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-EVK-April-2024.pdf

### Keywords for Search

`vulnerability`

