---
# Core Classification
protocol: Ethereum Reserve Dollar (ERD)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60116
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
source_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
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
finders_count: 3
finders:
  - Ibrahim Abouzied
  - Rabib Islam
  - Hytham Farah
---

## Vulnerability Title

Changing USDE Gas Compensation Causes Discrepancy Between Trove ICRs and TCR

### Overview


This bug report is about a function called `setGasCompensation()` in the `CollateralManager.sol` file. This function allows the owner to change the value of `USDE_GAS_COMPENSATION`, which is used to calculate how much a borrower owes for compensating liquidators. However, if this value is changed, it can cause a discrepancy between the ICR (Individual Collateral Ratio) and TCR (Total Collateral Ratio) of existing troves. This can lead to unexpected consequences such as troves being liquidated sooner or later than expected and the TCR and ICRs being misrepresented. The report suggests three possible solutions to fix this issue, such as preventing the change of USDE gas compensation, not retroactively affecting existing troves, or minting or burning from the gas pool to make up for the discrepancy. The client has marked this issue as "Fixed" and provided a code update. 

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `6c74c1716105a6b9bf25db1b19c35a6fc8a6a243`. The client provided the following explanation:

> GasPool mint or burn when USDE_GAS_COMPENSATION be updated.

**File(s) affected:**`CollateralManager.sol`

**Description:** The function `setGasCompensation()` allows the owner of `CollateralManager` to set the value `USDE_GAS_COMPENSATION`, which is used to determine how much a borrower owes for compensating liquidators for calling liquidation functions. The value of `USDE_GAS_COMPENSATION` is used to determine, upon opening a trove, how much of the issued debt (in the form of USDE) is to be sent to the gas pool to compensate the liquidation of the trove.

Suppose the USDE gas compensation has been increased by calling the function. Now, via `TroveManager.getTroveDebt()` which calculates a trove's debt by summing up a certain amount with the _new_ USDE gas compensation amount, the ICR of **all existing troves** is increased. However, the TCR of the protocol, which calculates the gas compensation portion by relying on the balance of the gas pool, will remain unchanged. The result will be a potentially massive discrepancy between the ICRs and the TCR, whereas in general one should be able to draw a direct formal relationship between the two. Potential consequences of this may include troves being put up for liquidation sooner or later than expected, recovery mode being triggered sooner or later than expected, and the TCR or ICRs of troves being materially misrepresented to users and devs.

**Recommendation:** A few routes could be taken to resolve this issue:

1.   Prevent the possibility of changing USDE gas compensation.
2.   Do not retroactively cause existing troves to have a different debt burden on account of changing the USDE gas compensation amount.
3.   Mint to or burn from the gas pool when changing USDE gas compensation in order to make up for the discrepancy between the ICRs and TCR.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethereum Reserve Dollar (ERD) |
| Report Date | N/A |
| Finders | Ibrahim Abouzied, Rabib Islam, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html

### Keywords for Search

`vulnerability`

