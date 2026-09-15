---
# Core Classification
protocol: Tracer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25491
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-06-tracer
source_link: https://code4rena.com/reports/2021-06-tracer
github_link: https://github.com/code-423n4/2021-06-tracer-findings/issues/104

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
  - derivatives

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] Deflationary tokens are not supported

### Overview


This bug report is about ERC20 tokens that may make certain customizations to their ERC20 contracts. One type of these tokens is deflationary tokens that charge a certain fee for every `transfer()` or `transferFrom()` and this fee is not taken into account when using the `deposit()` functions of `Insurance` and `TracerPerpetualSwaps`. This means that the user is credited the full amount without the taxes (`userBalance.position.quote`). 

The possible mitigation suggested is to measure the asset change right before and after the asset-transferring functions. The severity of the bug was initially marked as medium risk, however, it was later downgraded to low risk by raymogg (Tracer) as it falls outside of the trust model and should be communicated to users explicitly.

### Original Finding Content

_Submitted by cmichel, also found by s1m0 and 0xRajeev_

There are ERC20 tokens that may make certain customizations to their ERC20 contracts.
One type of these tokens is deflationary tokens that charge a certain fee for every `transfer()` or `transferFrom()`.

The `deposit()` functions of `Insurance` and `TracerPerpetualSwaps` assume that the external ERC20 balance of the contract increases by the same amount as the `amount` parameter of the `transferFrom`.

The user is credited the full amount without the taxes (`userBalance.position.quote`).

Recommend as one possible mitigation, measuring the asset change right before and after the asset-transferring functions.

**[raymogg (Tracer) confirmed but disagreed with severity](https://github.com/code-423n4/2021-06-tracer-findings/issues/104#issuecomment-873757118):**
 > Most likely not a medium risk as you can do a lot more nasty things than just use rebasing tokens. Since the owner of a market can set their own quote token, this token could be a token they control the supply of allowing them to arbitrarily transfer tokens between accounts, etc.
>
> As such, this sort of falls outside of our trust model. Market creators should use tokens that behave as "standard" ERC20s. We will make a not that rebasing and deflationary tokens should not be used as quote tokens without weird behaviour.
>
> Would be better as a low or informational issue due to this.

**[cemozerr (Judge) downgraded severity from 2 to 1](https://github.com/code-423n4/2021-06-tracer-findings/issues/104#issuecomment-882104304):**
 > Marking this as low risk as it seems to fall outside of the trust model, yet important enough to communicate to users explicitly.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-tracer
- **GitHub**: https://github.com/code-423n4/2021-06-tracer-findings/issues/104
- **Contest**: https://code4rena.com/reports/2021-06-tracer

### Keywords for Search

`vulnerability`

