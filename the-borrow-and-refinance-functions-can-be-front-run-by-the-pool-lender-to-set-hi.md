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
solodit_id: 34513
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx
source_link: none
github_link: https://github.com/Cyfrin/2023-07-beedle

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
finders_count: 62
finders:
  - RugpullDetector
  - ni8mare
  - iurii2002
  - HALITUS
  - lealCodes
---

## Vulnerability Title

The `borrow` and `refinance` functions can be front-run by the pool lender to set high interest rates

### Overview


The `borrow` and `refinance` functions in the `Lender` smart contract can be manipulated by the pool lender to set a very high interest rate for the borrower. This can happen because the borrower does not have the option to set a maximum interest rate and the pool lender can change the interest rate using the `setPool` function. This results in the borrower having to pay a much higher interest rate than expected. To fix this, the borrower should be allowed to set a maximum interest rate and the pool should be checked to make sure it meets this requirement. This issue was identified through a manual review of the code. 

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L256">https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L256</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L688">https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L688</a>


## Summary

The pool's `interestRate` is assigned to the loan without the borrower having the possibility to define a maximum value. This allows the pool lender to front-run the borrower by calling the `borrow` or `refinance` function and setting the maximum possible `interestRate` value, i.e., `MAX_INTEREST_RATE`. This results in a very high interest payment for the borrower.

## Vulnerability Details

If a user/borrower calls the `borrow` or `refinance` functions, the pool lender can front-run and change the pool's `interestRate` to an unfavorable (for the borrower) and very high value (e.g., `MAX_INTEREST_RATE`) by using the `setPool` function. This results in a very high interest payment for the borrower, calculated in the [`_calculateInterest`](https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L720) function.

- The `borrow` function assigns the `pool.interestRate` to the loan in [L256](https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L256)
- The `refinance` function updates the loan's auction length to the `pool.interestRate` in [L688](https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L688)

## Impact

Unnecessary and unexpected high interest rate for the borrower.

## Tools Used

Manual Review

## Recommendations

Consider allowing the borrower to define a maximum interest rate when borrowing or refinancing and validate if the pool fulfills this criterion.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beedle - Oracle free perpetual lending |
| Report Date | N/A |
| Finders | RugpullDetector, ni8mare, iurii2002, HALITUS, lealCodes, 0xSwahili, toshii, 0xl00k, CircleLooper, sobieski, JMTT, 0xAsen, tsvetanovv, HChang26, qbs, 0xRstStn, MahdiKarimi, Juntao, InAllHonesty, rafaelnicolau, Silvermist, degensec, leasowillow, Norah, deadrosesxyz, 0xDanielH, Cosine, Bauer, Bernd, 0xbepresent, nicobevi, crippie, Auditism, 0xDetermination, smbv1923, 0xdeth, Madalad, kutu, 0xANJAN143, GoSoul22, gkrastenov, nabeel, Bobface, hlx, Crunch, 0xumarkhatab, pep7siup, BanditSecurity, pengun, ptsanev, ayeslick, ubermensch, Lalanda, aak, 0xanmol, honeymewn |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-beedle
- **Contest**: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx

### Keywords for Search

`vulnerability`

