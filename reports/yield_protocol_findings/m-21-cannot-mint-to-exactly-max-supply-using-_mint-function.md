---
# Core Classification
protocol: Yieldy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2896
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-yieldy-contest
source_link: https://code4rena.com/reports/2022-06-yieldy
github_link: https://github.com/code-423n4/2022-06-yieldy-findings/issues/200

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
  - liquid_staking
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hansfriese  minhquanym
  - Chom
---

## Vulnerability Title

[M-21] Cannot mint to exactly max supply using `_mint` function

### Overview


This report is about a bug that occurs in the Yieldy.sol contract. The bug prevents the `_mint` function from minting to exactly the maximum supply. This is due to the following line of code: `require(_totalSupply < MAX_SUPPLY, "Max supply");` which should be changed to `require(_totalSupply <= MAX_SUPPLY, "Max supply");`. This issue was discovered manually, without the use of any tools. The impact of this bug is that it prevents the `_mint` function from minting to exactly the maximum supply, which should not be the case. The recommended mitigation step is to change the line of code as stated above.

### Original Finding Content

_Submitted by Chom, also found by hansfriese and minhquanym_

Cannot mint to exactly max supply using `_mint` function.

### Proof of Concept

    require(_totalSupply < MAX_SUPPLY, "Max supply");

if `_totalSupply == MAX_SUPPLY` this assert will be failed and reverted.

But it shouldn't be reverted as `_totalSupply == MAX_SUPPLY` is valid.

### Recommended Mitigation Steps

Change to

    require(_totalSupply <= MAX_SUPPLY, "Max supply");

**[JasoonS (judge) commented](https://github.com/code-423n4/2022-06-yieldy-findings/issues/200#issuecomment-1199257061):**
 > Feels potentially too generous giving this a medium since it isn't clear what the exploit would be, but it is a bug. I'll be generous...

**[toshiSat (Yieldy) acknowledged and commented](https://github.com/code-423n4/2022-06-yieldy-findings/issues/200#issuecomment-1205716867):**
 > Yea we aren't going to implement this one due to nearly every example of rebasing tokens are using this calculation.  It will be very unlikely that total supply ever hits max supply,  so the risk isn't worth the reward for changing it.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yieldy |
| Report Date | N/A |
| Finders | hansfriese  minhquanym, Chom |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-yieldy
- **GitHub**: https://github.com/code-423n4/2022-06-yieldy-findings/issues/200
- **Contest**: https://code4rena.com/contests/2022-06-yieldy-contest

### Keywords for Search

`vulnerability`

