---
# Core Classification
protocol: Trader Joe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1347
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-trader-joe-contest
source_link: https://code4rena.com/reports/2022-01-trader-joe
github_link: https://github.com/code-423n4/2022-01-trader-joe-findings/issues/18

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
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - defsec
---

## Vulnerability Title

[M-14] Incompatibility With Rebasing/Deflationary/Inflationary tokens

### Overview


This bug report is about the TraderJOE protocol not supporting rebasing/deflationary/inflationary tokens. These tokens have a balance that changes during transfers or over time, and the protocol does not have the necessary checks to verify the amount of tokens transferred to contracts before and after the transfer. The proof of concept used for this bug was a code review, and the recommended mitigation steps are to ensure that the balance is checked before and after, add support for such tokens before accepting user-supplied tokens, and consider supporting deflationary/rebasing tokens with extra checks or informing users not to use such tokens if they don't want to lose them.

### Original Finding Content

_Submitted by defsec_

The TraderJOE protocol do not appear to support rebasing/deflationary/inflationary tokens whose balance changes during transfers or over time. The necessary checks include at least verifying the amount of tokens transferred to contracts before and after the actual transfer to infer any fees/interest.

#### Proof of Concept

<https://github.com/code-423n4/2022-01-trader-joe/blob/main/contracts/RocketJoeStaking.sol#L133>

<https://github.com/code-423n4/2022-01-trader-joe/blob/main/contracts/RocketJoeFactory.sol#L132>

#### Recommended Mitigation Steps

*   Ensure that to check previous balance/after balance  equals to amount for any rebasing/inflation/deflation
*   Add support in contracts for such tokens before accepting user-supplied tokens
*   Consider supporting deflationary / rebasing / etc tokens by extra checking the balances before/after or strictly inform your users not to use such tokens if they don't want to lose them.

**[cryptofish7 (Trader Joe) disputed and commented](https://github.com/code-423n4/2022-01-trader-joe-findings/issues/18#issuecomment-1026943303):**
 > It won’t revert as long as token’s balance doesn’t decrease (this never happens).

**[LSDan (judge) increased severity from Low to Medium and commented](https://github.com/code-423n4/2022-01-trader-joe-findings/issues/18#issuecomment-1048747093):**
 > It is possible for someone to unknowingly use this functionality with a token that rebases down during the launch event. Just because you don't support a token type, doesn't mean that the design doesn't exist. This is a medium risk, not a low risk, because there is the potential for external interaction to cause a loss of funds.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Trader Joe |
| Report Date | N/A |
| Finders | defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-trader-joe
- **GitHub**: https://github.com/code-423n4/2022-01-trader-joe-findings/issues/18
- **Contest**: https://code4rena.com/contests/2022-01-trader-joe-contest

### Keywords for Search

`vulnerability`

