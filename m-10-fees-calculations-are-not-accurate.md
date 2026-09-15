---
# Core Classification
protocol: Amun
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6532
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-amun-contest
source_link: https://code4rena.com/reports/2021-12-amun
github_link: https://github.com/code-423n4/2021-12-amun-findings/issues/73

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - certora
---

## Vulnerability Title

[M-10] fees calculations are not accurate

### Overview


This bug report is about an issue with the calculation of fees in the Certora system. The issue is that when the fee is calculated and then minted to the feeBeneficiary, the amount minted is lower than it should be. This means that the feeBeneficiary will get less fees than they should. As an example, if the basket assets are worth 1M dollars and the totalSupply is 1M, the result of the calcOutStandingAnnualizedFee should be 100,000 dollars for the feeBeneficiary. However, if 100,000 is minted, the totalSupply will increase to 1,100,000, meaning the feeBeneficiary will only get 90909.09 dollars instead of the 100k they should get.

### Original Finding Content


_Submitted by certora_

after that fee is calculated, it is minted to the feeBeneficiary.
simply minting the exact amount results lower fee than it should be.

#### Impact

feeBeneficiary will get less fees than it should.

#### Proof of Concept

let's assume that the basket assets are worth 1M dollars, and totalSupply = 1M.
the result of `calcOutStandingAnnualizedFee` is 100,00 so the feeBeneficiary should get 100,00 dollars.
however, when minting 100,00 the totalSupply will increase to 1,100,000 so they will own 100000/1100000 &ast; (1M dollars) = 90909.09 dollars instead of 100k

**[loki-sama (Amun) acknowledged](https://github.com/code-423n4/2021-12-amun-findings/issues/73#issuecomment-1004708113):**

> This is mitigated by the feeBeneficiary diluting his own shares if he gets fees on his fees.

**[0xleastwood (Judge) asked](https://github.com/code-423n4/2021-12-amun-findings/issues/73#issuecomment-1019396342):**

> I'm not exactly sure if I understand what the warden is stating here. Could you confirm @loki-sama ?

**[loki-sama (Amun) confirmed](https://github.com/code-423n4/2021-12-amun-findings/issues/73#issuecomment-1020138537):**

> Ok, I myself misunderstood. He is correct that we don't get the full value. When we take a fee of 10% like from his example. What we do is mint 10% of the basket to ourselves. That 10% after minting is not holding 10% of the underling.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Amun |
| Report Date | N/A |
| Finders | certora |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-amun
- **GitHub**: https://github.com/code-423n4/2021-12-amun-findings/issues/73
- **Contest**: https://code4rena.com/contests/2021-12-amun-contest

### Keywords for Search

`vulnerability`

