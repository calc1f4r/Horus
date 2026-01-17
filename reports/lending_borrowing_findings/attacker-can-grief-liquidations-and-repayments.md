---
# Core Classification
protocol: Creditswap
chain: everychain
category: economic
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37096
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
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
  - liquidation
  - grief_attack
  - front-running

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Attacker Can Grief Liquidations And Repayments

### Overview


This bug report discusses a critical issue in the liquidation and repayment functions of a loan protocol. The bug occurs when an attacker manipulates the liquidation process by sending a small amount of debt tokens to the vault, causing a discrepancy between the debt amount and the token balance. This makes it impossible for the protocol to liquidate the loan or for the debtor to repay it, resulting in significant losses for the protocol. The recommendation is to implement an internal accounting system or change the condition for reverting the function to prevent this issue.

### Original Finding Content

**Severity** - Critical

**Status** - Resolved 

**Description**

To liquidate an unhealthy loan position the liquidate() function inside CreditorNFT can be called by anyone where the debtAmount of debt token is paid out by the liquidator.
This function in turn calls the liquidate function of LoanVault at L133.

Inside LoanVault.sol’s liquidate() it is checked if the debtAmount (initial debt amount when loan was created) is now equal to the balance of debt token in the vault , if not revert (L163)

An attacker can see a liquidation() call in the mempool and ->

a.) Frontruns this call to send the lowest amount of debt token to the vault , say 1
b.) Now when the liquidator tries to liquidate he sends out debtAmount of tokens to the vault , let’s say they were 100
c.) It is checked that debt amount and balance of debt token balance in the vault is equal
d.) But they are not since there are a total of 101 debt tokens now , liquidation reverts.

Due to this the vault/loan position can never be liquidated and the protocol will continue to incur huge losses as the collateral value falls down.

The same problem lies in repay functionality , at L150 in LoanVault.sol it will revert due to the same case as above and make it impossible for a debtor to repay their loan , resulting in forced liquidations.

**Recommendation**:

Have an internal accounting system or change the condition to if the balance in the vault is less than debt amount, then revert instead of a strict equality.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Creditswap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Liquidation, Grief Attack, Front-Running`

