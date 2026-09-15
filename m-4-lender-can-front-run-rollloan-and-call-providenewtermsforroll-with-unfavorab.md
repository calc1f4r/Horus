---
# Core Classification
protocol: Cooler Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26360
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/107
source_link: none
github_link: https://github.com/sherlock-audit/2023-08-cooler-judging/issues/243

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
finders_count: 13
finders:
  - james\_wu
  - sy
  - 0xbepresent
  - radevauditor
  - pep7siup
---

## Vulnerability Title

M-4: Lender can front-run `rollLoan` and call `provideNewTermsForRoll` with unfavorable terms

### Overview


A bug was identified in the Cooler smart contract that allows a lender to front-run a user's transaction and call the `provideNewTermsForRoll` function with unfavorable terms. This can occur when a user borrows from a lender, the lender proposes new suitable terms, and the user accepts them by calling the `rollLoan` function. The lender can then see the pending transaction in the mempool and front-run the user's transaction by making a new call to `provideNewTermsForRoll` with an extremely high interest rate, resulting in the user accepting unfavorable terms. This could lead to the user overpaying interest.

The bug was found through manual review, and the code snippets can be found at https://github.com/sherlock-audit/2023-08-cooler/blob/main/Cooler/src/Cooler.sol#L192 and https://github.com/sherlock-audit/2023-08-cooler/blob/main/Cooler/src/Cooler.sol#L282.

A recommendation was made to let the user pass a parameter consisting of the max interest rate they are willing to accept when calling `rollLoan` to prevent such incidents. This issue is now moot as the `rollLoan` function no longer exists.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-08-cooler-judging/issues/243 

## Found by 
0xbepresent, Breeje, banditx0x, cats, deadrxsezzz, detectiveking, evilakela, harisnabeel, james\_wu, pep7siup, radevauditor, sandy, ubl4nk
Lender can front-run `rollLoan` and result in borrower accepting unfavorable terms.

## Vulnerability Detail
After a loan is created, the lender can provide new loan terms via `provideNewTermsForRoll`. If they are reasonable, the user can then accept them. However this opens up a risky scenario: 
1. User A borrows from lender B 
2. Lender B proposes new suitable terms 
3. User A sees them and calls `rollLoan` to accept them
4. Lender B is waiting for this and sees the pending transaction in the mempool
5. Lender B front-runs user A's transaction and makes a new call to `provideNewTermsForRoll` will an extremely high interest rate
6. User A's transaction now executes and they've accepted unfavorable terms with extremely high interest rate

## Impact
User may get mislead in to accepting unfavorable terms and overpaying interest 

## Code Snippet
https://github.com/sherlock-audit/2023-08-cooler/blob/main/Cooler/src/Cooler.sol#L192
https://github.com/sherlock-audit/2023-08-cooler/blob/main/Cooler/src/Cooler.sol#L282

## Tool used

Manual Review

## Recommendation
When calling `rollLoan` let the user pass a parameter consisting of the max interest rate they are willing to accept to prevent from such incidents.





## Discussion

**0xRusowsky**

- https://github.com/ohmzeus/Cooler/pull/63

**jkoppel**

This is moot because rollLoan no longer exists.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Cooler Update |
| Report Date | N/A |
| Finders | james\_wu, sy, 0xbepresent, radevauditor, pep7siup, bitx0x, harisnabeel, deadrxsezzz, detectiveking, cats, Breeje, evilakela, ubl4nk |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-08-cooler-judging/issues/243
- **Contest**: https://app.sherlock.xyz/audits/contests/107

### Keywords for Search

`vulnerability`

