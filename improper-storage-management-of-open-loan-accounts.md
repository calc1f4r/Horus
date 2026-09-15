---
# Core Classification
protocol: Synthetix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19669
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Improper Storage Management of Open Loan Accounts

### Overview


A bug was found in the openLoan() function on line 342, which causes the associated account address to be added to the accountsWithOpenLoans array regardless of whether the account already has a loan/is already included in the array. This can lead to an account being listed more than once in the array. Additionally, a malicious actor can exploit the unbound storage array in accountsSynthLoans by issuing a large number of loans with the same borrower, and trying to close one of them, which could result in a denial of service condition. 

The development team implemented the recommendations to change the storeLoan function to only push the account to the accountsWithOpenLoans array if the loan to be stored is the first one for that particular account, and to introduce a limit to the number of loans each account can have.

### Original Finding Content

## Description

When loans are open, the associated account address gets added to the `accountsWithOpenLoans` array regardless of whether the account already has a loan/is already included in the array (see `storeLoan()` function called by the `openLoan()` function on line [342]).

As a result, consider the following scenario:
- Alice opens `loanA`, Bob opens `loanB`, and Alice opens `loanC` and `loanD`.
- The `accountsWithOpenLoans` array will be `[Alice, Bob, Alice, Alice]`.
- When Alice closes `loanA`, the function `_removeFromOpenLoanAccounts` doesn’t get called, as Alice still has `loanC` and `loanD`.
- When Alice closes `loanC` and `loanD`, the `accountsWithOpenLoans` array will be `[Alice, Bob, Alice]`.

Additionally, it is possible for a malicious actor to create a denial of service condition exploiting the unbound storage array in `accountsSynthLoans` via the following scenario:
1. Use an issue limit of 5000 ETH, and a minimum loan size of 1 ETH (current contract defaults);
2. Issue 1200 loans with 1 ETH as collateral for each one of them, from the same borrower;
3. Try to close loan number `1199`, and watch the transaction fail due to a gas cost higher than the block gas limit (set to 10 million gas, the mainnet network value at the time of writing).

Refer to our test `test/EtherCollateral-gas-tests.js` for a proof-of-concept.

## Recommendations
- Consider changing the `storeLoan` function to only push the account to the `accountsWithOpenLoans` array if the loan to be stored is the first one for that particular account.
- Introduce a limit to the number of loans each account can have.

## Resolution
The development team implemented the recommendations above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Synthetix |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf

### Keywords for Search

`vulnerability`

