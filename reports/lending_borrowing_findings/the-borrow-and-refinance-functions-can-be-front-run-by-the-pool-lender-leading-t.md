---
# Core Classification
protocol: Beedle - Oracle free perpetual lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34523
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx
source_link: none
github_link: https://github.com/Cyfrin/2023-07-beedle

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
  - 0xbepresent
  - pep7siup
  - Bernd
---

## Vulnerability Title

The `borrow` and `refinance` functions can be front-run by the pool lender leading to collateral being seized in the next block

### Overview


The report highlights a bug in the `borrow` and `refinance` functions of the `Lender` contract. This bug can be exploited by the pool lender to seize the borrower's collateral in the next block. The vulnerability is caused by the pool's `auctionLength` being assigned without the borrower's input, allowing the lender to set a very short value and start an auction for the loan. This can result in the borrower losing their collateral. The report recommends allowing the borrower to define a minimum auction length and setting a reasonable minimum value for the auction length to prevent this issue. 

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L259">https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L259</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L694">https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L694</a>


## Summary

The pool's `auctionLength` is assigned to the loan without the borrower having the possibility to define a minimum value. This allows the pool lender to front-run the borrower by calling the `borrow` or `refinance` function and setting a very short `auctionLength` value. Resulting in the collateral being seized in the next block.

## Vulnerability Details

If a user/borrower calls the `borrow` or `refinance` functions, the pool lender can front-run and change the pool's `auctionLength` to an unfavorable (for the borrower) and very small value (e.g., `1`) by using the `setPool` function. Subsequently, the lender of the pool can start the auction for the loan. Due to the short `auctionLength`, the auction will end in the next block. This allows the lender (or basically anyone) to seize the collateral in the next block.

- The `borrow` function assigns the `pool.auctionLength` to the loan in [L259](https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L259)
- The `refinance` function updates the loan's auction length to the `pool.auctionLength` in [L694](https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L694)

## Impact

The pool lender can seize the loan's collateral almost immediately (specifically, in the next block), causing a loss to the borrower.

## Tools Used

Manual Review

## Recommendations

Consider allowing the borrower to define a minimum auction length when borrowing or refinancing and validate if the pool fulfills this criterion. Additionally, consider adding a reasonable minimum value for the auction length (e.g., 1 hour or 1 day) to allow the borrower to act appropriately.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beedle - Oracle free perpetual lending |
| Report Date | N/A |
| Finders | 0xbepresent, pep7siup, Bernd |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-beedle
- **Contest**: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx

### Keywords for Search

`vulnerability`

