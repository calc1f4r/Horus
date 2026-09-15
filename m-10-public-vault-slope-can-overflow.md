---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25826
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/418

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - evan
---

## Vulnerability Title

[M-10] Public vault slope can overflow

### Overview


This bug report is about an overflow issue in the "PublicVault.sol" and "LienToken.sol" files of the Astaria project. This overflow occurs in the "afterPayment" function due to unchecked addition, which can result in incorrect values for "totalAssets" and large fluctuations in "slope".

To demonstrate the issue, a proof of concept was created using a normal 18 decimal ERC20 token. After 5 loans of 1000 tokens, all with the maximum interest rate of 63419583966, the slope will overflow. The tools used for this proof of concept was VSCode.

The recommended mitigation steps for this issue is to remove the unchecked block and consider increasing the bits used for slope. This bug was confirmed by SantiagoGregory (Astaria).

### Original Finding Content


<https://github.com/code-423n4/2023-01-astaria/blob/main/src/PublicVault.sol#L562-L568><br>
<https://github.com/code-423n4/2023-01-astaria/blob/57c2fe33c1d57bc2814bfd23592417fc4d5bf7de/src/LienToken.sol#L702-L704>

The slope of public vault can overflow in the afterPayment function due to unchecked addition. When this happens, totalAssets will not be correct. This can also result in underflows in slope updates elsewhere, causing large fluctuations in slope and totalAssets.

### Proof of Concept

Assume the token is a normal 18 decimal ERC20 token.<br>
After 5 loans of 1000 tokens, all with the maximum interest rate of 63419583966, the slope will overflow.<br>
`5 * 1000 * 63419583966 / 2^48 = 1.1265581173`

### Tools Used

VSCode

### Recommended Mitigation Steps

Remove the unchecked block. Also, I think 48 bits might not be enough for slope.

**[SantiagoGregory (Astaria) confirmed](https://github.com/code-423n4/2023-01-astaria-findings/issues/418)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | evan |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/418
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

