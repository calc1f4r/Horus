---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25321
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto-v2
source_link: https://code4rena.com/reports/2022-06-canto-v2
github_link: https://github.com/code-423n4/2022-06-NewBlockchain-v2-findings/issues/38

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-06] `getBorrowRate` returns rate per year instead of per block

### Overview


A bug was reported in the Plex Engineer Lending Market V2 codebase by Lambda and was also found by Chom. According to the documentation in InterestRateModel, the getBorrowRate function should return the borrow rate per block, however the rate per year is returned for NoteInterest. This would result in completely wrong values. To mitigate this issue, the suggested solution is to return baseRatePerBlock instead. This was confirmed by Nivasan1 (Canto) and Alex the Entreprenerd (judge) commented that the effect of this bug would be a massive loss of value to interest and incorrect yield. Therefore, it was deemed a high severity issue.

### Original Finding Content

_Submitted by Lambda, also found by Chom_

<https://github.com/Plex-Engineer/lending-market-v2/blob/2646a7676b721db8a7754bf5503dcd712eab2f8a/contracts/NoteInterest.sol#L118><br>
<https://github.com/Plex-Engineer/lending-market-v2/blob/2646a7676b721db8a7754bf5503dcd712eab2f8a/contracts/CToken.sol#L209>

According to the documentation in `InterestRateModel`, `getBorrowRate` has to return the borrow rate per block and the function `borrowRatePerBlock` in `CToken` directly returns the value of `getBorrowRate`. However, the rate per year is returned for `NoteInterest`. Therefore, using `NoteInterest` as an interest model will result in completely wrong values.

### Recommended Mitigation Steps

Return `baseRatePerBlock`.

**[nivasan1 (Canto) confirmed](https://github.com/code-423n4/2022-06-canto-v2-findings/issues/38)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-v2-findings/issues/38#issuecomment-1216901711):**
 > The warden has shown that the borrowRate is returning per-year values instead of per-block values.
> 
> The effect of this is that the accounting will be magnified massively.
> 
> While impact should be mostly loss of value to interest and incorrect yield, due to the math being wrong I do agree with High Severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto-v2
- **GitHub**: https://github.com/code-423n4/2022-06-NewBlockchain-v2-findings/issues/38
- **Contest**: https://code4rena.com/reports/2022-06-canto-v2

### Keywords for Search

`vulnerability`

