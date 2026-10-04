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
solodit_id: 25824
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/435

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
finders_count: 2
finders:
  - evan
  - PaludoX0
---

## Vulnerability Title

[M-08] Public vault strategist reward is not calculated correctly

### Overview


A bug was reported in the Astaria codebase, where the Strategist interest reward is not calculated correctly. The reward is almost always calculated with interestOwed, regardless of the amount paid. This can lead to the Strategist being paid more than they are supposed to, and encourages them to maximize interestOwed and make tiny payments on behalf of the borrower. This can trigger a compound interest vulnerability.

The bug occurs when the LienToken calls beforePayment, which calls _handleStrategistInterestReward, and the amount passed in is the amount of the lien (stack.point.amount), not the amount paid. This should be changed to the amount actually paid, to mitigate the attack.

The bug was confirmed by the sponsor, who said the Strategist reward should be paid only on interest, and if the payment is greater than the interest owing, only mint them based on the interest owed, but if it’s less, then, mint their shares based on the amount.

The tools used to detect the bug were VSCode, and the recommended mitigation steps are to change `stack.point.amount` to `amount`.

### Original Finding Content


<https://github.com/code-423n4/2023-01-astaria/blob/main/src/PublicVault.sol#L597-L609><br>
<https://github.com/code-423n4/2023-01-astaria/blob/main/src/LienToken.sol#L819>

Strategist interest reward is not calculated correctly. The reward will almost always be calculated with interestOwed, regardless of the amount paid.

As a result, the strategist gets paid more than they are supposed to. Even if the borrower hasn't made a single payment, the strategist can make a tiny payment on behalf of the borrower to trigger this calculation.

This also encourages the strategist to maximize interestOwed and make tiny payments on behalf of the borrower. This can trigger a compound interest vulnerability which I've made a separate report about.

### Proof of Concept

As confirmed by the sponsor, the strategist reward is supposed to be "paid on performance and only\@on interest. if the payment that’s being made is greater than the interest owing we only mint them based on the interest owed, but if it’s less, then, mint their shares based on the amount"

However, this is not the case. When LienToken calls beforePayment, which calls \_handleStrategistInterestReward, the amount passed in is the amount of the lien (stack.point.amount), not the amount paid.

### Tools Used

VSCode

### Recommended Mitigation Steps

<https://github.com/code-423n4/2023-01-astaria/blob/main/src/LienToken.sol#L819><br>
I believe `stack.point.amount` should be changed to `amount`.

**[androolloyd (Astaria) commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/435#issuecomment-1406792466):**
 > Since we track payments against the principle via stack.point.amount, then you want to ensure that what were sending them is the correct amount. Lien data doesnt track the balance of a loan, only the max value a lien can have.

**[SantiagoGregory (Astaria) acknowledged](https://github.com/code-423n4/2023-01-astaria-findings/issues/435)**

**[Picodes (judge) commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/435#issuecomment-1439648798):**
 > `stack.point.amount`, which represents the remaining debt amount should be replaced by the amount actually paid to mitigate this attack.



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
| Finders | evan, PaludoX0 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/435
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

