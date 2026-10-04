---
# Core Classification
protocol: Maple Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18097
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/MapleFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/MapleFinance.pdf
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
  - Paweł Płatek
  - Maximilian Krüger
  - Michael Colburn
---

## Vulnerability Title

Missing zero checks

### Overview


This bug report is about data validation in the codebase of the Liquidator.sol, MapleLoan.sol, and MapleProxyFactory.sol contracts. It was discovered that a number of constructors and functions in the codebase do not check if zero is passed in as a parameter. This means that if zero is passed in for one of these parameters, the contract will become unusable and the funds will be locked. The parameters that are not checked for zero are the owner_, collateralAsset_, fundsAsset_, auctioneer_, destination_, borrower_, lender_, and mapleGlobals_ parameters. 

The cost of checking a parameter for the zero value is negligible, costing only half a cent. However, if zero checks were in place, an exploit scenario such as a bug in the front end could be prevented from occurring.

The recommendations for this bug are to add zero checks for the listed parameters and to comprehensively validate all parameters. Additionally, integrate Slither into the CI pipeline to automatically detect functions that lack zero checks. This will make sure that all parameters are checked for zero and prevent any exploit scenarios from occurring.

### Original Finding Content

## Difficulty: High

## Type: Data Validation

### Target:
- `Liquidator.sol`
- `MapleLoan.sol`
- `MapleProxyFactory.sol`

## Description
A number of constructors and functions in the codebase do not revert if zero is passed in for a parameter that should not be set to zero. The following parameters are not checked for the zero value:

### Liquidator contract
- **constructor()**
  - `owner_`
  - `collateralAsset_`
  - `fundsAsset_`
  - `auctioneer_`
  - `destination_`
- **setAuctioneer()**
  - `auctioneer_`

### MapleLoan contract
- **setBorrower()**
  - `borrower_`
- **setLender()**
  - `lender_`

### MapleProxyFactory contract
- **constructor()**
  - `mapleGlobals_`

If zero is passed in for one of those parameters, it will render the contract unusable, leaving its funds locked (and therefore effectively lost) and necessitating an expensive redeployment. For example, if there were a bug in the front end, `MapleLoan.setBorrower` could be called with `address(0)`, rendering the contract unusable and locking its funds in it.

The gas cost of checking a parameter for the zero value is negligible. Since the parameter is usually already on the stack, a zero check consists of a `DUP` opcode (3 gas) and an `ISZERO` opcode (3 gas). Given a high gas price of 200 gwei and an ether price of $4,200, a zero check would cost half a cent.

## Exploit Scenario
A new version of the front end is deployed. A borrower suspects that the address currently used for his or her loan might have been compromised. As a precautionary measure, the borrower decides to transfer ownership of the loan to a new address. However, the new version of the front end contains a bug: the value of an uninitialized variable is used to construct the transaction. As a result, the borrower loses access to the loan contract, and to the collateral, forever. If zero checks had been in place, the transaction would have reverted instead.

## Recommendations
- **Short term**: Add zero checks for the parameters mentioned above and for all other parameters for which zero is not an acceptable value.
- **Long term**: Comprehensively validate all parameters. Avoid relying solely on the validation performed by front-end code, scripts, or other contracts, as a bug in any of those components could prevent it from performing that validation. Additionally, integrate Slither into the CI pipeline to automatically detect functions that lack zero checks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Maple Labs |
| Report Date | N/A |
| Finders | Paweł Płatek, Maximilian Krüger, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/MapleFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/MapleFinance.pdf

### Keywords for Search

`vulnerability`

