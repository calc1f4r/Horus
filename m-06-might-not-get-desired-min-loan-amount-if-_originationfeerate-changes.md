---
# Core Classification
protocol: Backed Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1861
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-backed-protocol-contest
source_link: https://code4rena.com/reports/2022-04-backed
github_link: https://github.com/code-423n4/2022-04-backed-findings/issues/28

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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel
  - teryanarmen
---

## Vulnerability Title

[M-06] Might not get desired min loan amount if `_originationFeeRate` changes

### Overview


This bug report is about the code in the NFTLoanFacilitator.sol file at line 309. It has to do with the origination fee rate that admins can update. The issue is that when a borrower creates a loan, they receive the pre-fee amount, not the post-fee amount. This means that if the admin increases the fee, the borrower will receive fewer funds than required and could become homeless as a result. The recommended mitigation steps are to reconsider how the min loan amount works and make it the post-fee amount instead of the pre-fee amount. This would make the amount the borrower receives more intuitive.

### Original Finding Content

_Submitted by cmichel, also found by teryanarmen_

[NFTLoanFacilitator.sol#L309](https://github.com/code-423n4/2022-04-backed/blob/e8015d7c4b295af131f017e646ba1b99c8f608f0/contracts/NFTLoanFacilitator.sol#L309)<br>

Admins can update the origination fee by calling `updateOriginationFeeRate`.
Note that a borrower does not receive their `minLoanAmount` set in `createLoan`, they only receive `(1 - originationFee) * minLoanAmount`, see [`lend`](https://github.com/code-423n4/2022-04-backed/blob/e8015d7c4b295af131f017e646ba1b99c8f608f0/contracts/NFTLoanFacilitator.sol#L159).
Therefore, they need to precalculate the `minLoanAmount` using the **current** origination fee to arrive at the post-fee amount that they actually receive.
If admins then increase the fee, the borrower receives fewer funds than required to cover their rent and might become homeless.

### Recommended Mitigation Steps

Reconsider how the min loan amount works. Imo, this `minLoanAmount` should be the post-fee amount, not the pre-fee amount. It's also more intuitive for the borrower when creating the loan.

**[wilsoncusack (Backed Protocol) disputed and commented](https://github.com/code-423n4/2022-04-backed-findings/issues/28#issuecomment-1090190851):**
 > Won't change, is just how it works.

**[wilsoncusack (Backed Protocol) acknowledged, but disagreed with Medium severity and commented](https://github.com/code-423n4/2022-04-backed-findings/issues/28#issuecomment-1092324481):**
> The only true mitigation here would be to store originationFeeRate in the Loan struct at the time of origination to guarantee a borrower gets the fee rate that was present when they created the loan. But we do not plan to make this change.

**[wilsoncusack (Backed Protocol) resolved and commented](https://github.com/code-423n4/2022-04-backed-findings/issues/28#issuecomment-1097468240):**
 > Decided to fix because we could do so without too much gas.

**[gzeon (judge) commented](https://github.com/code-423n4/2022-04-backed-findings/issues/28#issuecomment-1100102896):**
 > Sponsor confirmed with fix.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Backed Protocol |
| Report Date | N/A |
| Finders | cmichel, teryanarmen |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-backed
- **GitHub**: https://github.com/code-423n4/2022-04-backed-findings/issues/28
- **Contest**: https://code4rena.com/contests/2022-04-backed-protocol-contest

### Keywords for Search

`vulnerability`

