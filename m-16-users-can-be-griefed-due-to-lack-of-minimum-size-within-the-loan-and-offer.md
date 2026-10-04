---
# Core Classification
protocol: Debita Finance V3
chain: everychain
category: uncategorized
vulnerability_type: grief_attack

# Attack Vector Details
attack_type: grief_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44244
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/627
source_link: none
github_link: https://github.com/sherlock-audit/2024-10-debita-judging/issues/557

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.50
financial_impact: medium

# Scoring
quality_score: 2.5
rarity_score: 3

# Context Tags
tags:
  - grief_attack

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - xiaoming90
---

## Vulnerability Title

M-16: Users can be griefed due to lack of minimum size within the Loan and Offer

### Overview


This bug report discusses an issue with the Loan and Offer feature in a financial protocol called Debita. The problem is that there is no minimum size requirement for loans and offers, which allows malicious users to create numerous small or tiny loans and offers, causing grief to both borrowers and lenders. This can result in difficulties for borrowers to pay their debt or claim collateral, and for lenders to perform necessary actions like claiming interest or auctioning off defaulted collateral. The impact of this bug is significant, as it can cause users to incur high gas fees and be vulnerable to griefing attacks. To mitigate this issue, the report suggests implementing a minimum size requirement for loans and offers.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-10-debita-judging/issues/557 

## Found by 
xiaoming90
### Summary

_No response_

### Root Cause

_No response_

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

Assume that Bob creates a borrow offer with 10000 AERO as collateral to borrow 10000 USDC at the price/ratio of 1 AERO:1 USDC for simplicity's sake.

Malicious aggregator (aggregator is a public role and anyone can match orders) can perform griefing attacks against Bob.

The malicious aggregator can create many individual loans OR many loans with many offers within it, OR a combination of both. Each loan and offer will be small or tiny and consist of Bob's borrow order. This can be done because the protocol does not enforce any restriction on the minimum size of the loan or offer.

As a result, Bob's borrow offer could be broken down into countless (e.g., thousands or millions) of loans and offers. As a result, Bob will not be able to keep track of all the loans and offers belonging to him and will have issues paying the debt or claiming collateral.

This issue is also relevant to the lenders, and the impact is even more serious as lenders have to perform more actions against loans and offers, such as claiming debt, claiming interest, claiming collateral, or auctioning off defaulted collateral etc.

In addition, it also requires lenders and borrowers to pay a significant amount of gas fees in order to carry out the actions mentioned previously.

As a result, this effectively allows malicious aggregators to grief lenders and borrowers.

https://github.com/sherlock-audit/2024-11-debita-finance-v3/blob/main/Debita-V3-Contracts/contracts/DebitaV3Aggregator.sol#L167

### Impact

Malicious aggregators to grief lenders and borrowers.

### PoC

_No response_

### Mitigation

Having a maximum number of offers (e.g., 100) within a single Loan is insufficient to guard against this attack because malicious aggregators can simply work around this restriction by creating more loans.

Thus, it is recommended to impose the minimum size for each loan and/or offer, so that malicious aggregators cannot create many small/tiny loans and offers to grief the users.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2.5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Debita Finance V3 |
| Report Date | N/A |
| Finders | xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-10-debita-judging/issues/557
- **Contest**: https://app.sherlock.xyz/audits/contests/627

### Keywords for Search

`Grief Attack`

