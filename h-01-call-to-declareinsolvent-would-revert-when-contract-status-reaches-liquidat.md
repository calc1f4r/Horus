---
# Core Classification
protocol: Debt DAO
chain: everychain
category: logic
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6235
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-debt-dao-contest
source_link: https://code4rena.com/reports/2022-11-debtdao
github_link: https://github.com/code-423n4/2022-11-debtdao-findings/issues/69

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - liquidation
  - business_logic

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - payments
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - PaludoX0
  - cryptphi
  - ayeslick
  - Ch_301
  - adriro
---

## Vulnerability Title

[H-01] Call to declareInsolvent() would revert when contract status reaches liquidation point after repayment of credit position 1

### Overview


This bug report concerns the LineOfCredit contract, which is used to manage a line of credit for a borrower. The bug occurs when the borrower pays back the loan for a credit position, and the contract status is set to LIQUIDATABLE. In this case, the call to declareInsolvent() by the arbiter would revert, as the whileBorrowing() modifier check does not pass. This is because the ids array index shift in the call to  stepQ() shifts ids[1] to ids[0], thus making the condition for `credits[ids[0]].principal == 0` be true, causing the revert.

To reproduce the bug, the LineOfCredit contract must be set up and 5 lenders must have deposited into the contract. The borrower (Alice) then borrows credit from these 5 credit positions, including by calling LineOfCredit.borrow() for the position ids. Later, Alice pays back the loan for  credit position id 1 just before the contract gets liquidated. When the contract status is set to LIQUIDATABLE, no loan is drawn on credit position 0 and the arbiter calls declareInsolvent(), causing the call to revert.

The recommended mitigation step for this bug is to review and amend the modifier whileBorrowing().

### Original Finding Content

## Lines of code

https://github.com/debtdao/Line-of-Credit/blob/audit/code4rena-2022-11-03/contracts/modules/credit/LineOfCredit.sol#L143
https://github.com/debtdao/Line-of-Credit/blob/audit/code4rena-2022-11-03/contracts/modules/credit/LineOfCredit.sol#L83-L86


## Vulnerability details

## Impact
The modifier `whileBorrowing()` is used along in the call to LineOfCredit.declareInsolvent(). However this check reverts when count == 0 or `credits[ids[0]].principal == 0` . Within the contract, any lender can add credit which adds an entry in credits array, credits[ids]. 

Assume, when borrower chooses lender positions including credits[ids[0]] to draw on, and repays back the loan fully for credits[ids[1]], then the call to declareInsolvent() by the arbiter would revert since it does not pass the `whileBorrowing()` modifier check due to the ids array index shift in the call to  stepQ(), which would shift ids[1] to ids[0], thereby making the condition for `credits[ids[0]].principal == 0` be true causing the revert.



## Proof of Concept
1. LineOfCredit contract is set up and 5 lenders have deposited into the contract.
2. Alice, the borrower borrows credit from these 5 credit positions including by calling LineOfCredit.borrow() for the position ids.
3. Later Alice pays back the loan for  credit position id 1 just before the contract gets liquidated
4. At the point where ids.stepQ() is called in _repay(), position 1 is moved to ids[0]
4. When contract status is LIQUIDATABLE, no loan drawn on credit position 0 and arbiter calls declareInsolvent() , the call would revert since `credits[ids[0]].principal == 0`

## Tools Used
Manual review

## Recommended Mitigation Steps
The modifier whileBorrowing() would need to be reviewed and amended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Debt DAO |
| Report Date | N/A |
| Finders | PaludoX0, cryptphi, ayeslick, Ch_301, adriro, perseverancesuccess |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-debtdao
- **GitHub**: https://github.com/code-423n4/2022-11-debtdao-findings/issues/69
- **Contest**: https://code4rena.com/contests/2022-11-debt-dao-contest

### Keywords for Search

`Liquidation, Business Logic`

