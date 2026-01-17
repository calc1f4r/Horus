---
# Core Classification
protocol: Altr
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60248
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html
source_link: https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html
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
  - Roman Rohleder
  - Ruben Koch
  - Mostafa Yassin
---

## Vulnerability Title

Privileged Roles and Ownership

### Overview


This bug report explains that certain contracts have state variables that give specific addresses special roles. This can be risky for users. The `owner` address has the power to call certain functions that can affect the pricing, fees, and other aspects of the lending protocol. This means that the fees and terms of a loan can change after it has been accepted by the borrower. The recommendation is to make this information clear to users through public documentation.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `8982d06f5b1f6b5a81171a706b46192aaf68a10b`. The client provided the following explanation:

> https://docs.lucidao.com/dapps/altr-lending/faq - 5th FAQ, https://docs.lucidao.com/dapps/altr-lending/altr-lending/stakeholders-and-roles/admin, https://docs.lucidao.com/dapps/altr-lending/altr-lending/stakeholders-and-roles/treasury-manager.

**File(s) affected:**`Lending.sol`

**Description:** Certain contracts have state variables, e.g. `owner`, which provide certain addresses with privileged roles. Such roles may pose a risk to end-users.

The `owner` address has sole permission to call the following functions:

*   `setPriceIndex()` to update the pricing oracle. Malicious oracles could return incorrect values at the disadvantage of lenders.
*   `setGovernanceTreasury()` to update the address the protocol fees are transferred to.
*   `setRepayGracePeriod()` to update the period under which users can repay their expired loan before being liquidated.
*   `setRepayGraceFee()` to update the fee associated with such a delayed repayment.
*   `setProtocolFee()` to update the fee applied to the borrowed amount.
*   `setLiquidationFee()` to update the fee applied to the borrowed amount.
*   `setBaseOriginationFee()` to update the fee regarding the origination fees of the protocol.
*   `setTokens()` to add token addresses to be requestable for loans.
*   `unsetTokens()` to remove token addresses from that list
*   `setLoanTypes()` to update or add the APRs for certain loan durations.
*   `unsetLoanTypes()` to remove certain loan durations from being requestable for loans.
*   `setFeeReductionFactor()` to update the factor by which to reduce the origination fee given the loan exceeds a range.
*   `setRanges()` to update the origination fee ranges determining how often the `feeReductionFactor` is applied.

While the core interest rate fetched via the aprFromDuration mapping updateable via the `setLoanTypes()` mapping is hard coded at the time the loan is requested, it should be highlighted that in following fee calculations of the loan, the other fees are always fetched from the latest state of the contract, possibly differing from the fees the borrower originally requested the loan for.

So technically, it is possible that accepted loans at the time of repayment face a different set of `originationBaseFee`, `gracePeriodFee`, and `protocolFee`, though reasonable constant maximum values for those fees are enforced, enabling them only to collectively reach a value of 11 %. Also, loans that are within the grace period could become instantly liquidatable if the owner would e.g. suddenly greatly reduce the `gracePeriod`.

**Recommendation:** Clarify the impact of these privileged actions to the end-users via publicly facing documentation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Altr |
| Report Date | N/A |
| Finders | Roman Rohleder, Ruben Koch, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html

### Keywords for Search

`vulnerability`

