---
# Core Classification
protocol: Behodler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1379
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-behodler-contest
source_link: https://code4rena.com/reports/2022-01-behodler
github_link: https://github.com/code-423n4/2022-01-behodler-findings/issues/230

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
  - cross_chain
  - services
  - cdp
  - dexes
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hyh
---

## Vulnerability Title

[M-14] UniswapHelper.buyFlanAndBurn is a subject to sandwich attacks

### Overview


This bug report describes a vulnerability that can occur when using the function buyFlanAndBurn in the UniswapHelper contract. The vulnerability can be exploited by malicious actors to manipulate prices and cause users to receive fewer Flan tokens than the current market price dictates. The bug report provides a proof of concept for the vulnerability, and recommends two mitigation steps to prevent the vulnerability from occurring in the future. 

The first mitigation step recommended is to add a minimum accepted price as a function argument, so users can limit the effective slippage. The second mitigation step is to add a relative version of the parameter to control percentage based slippage with TWAP Oracle price as a benchmark. These steps should be implemented to prevent malicious actors from manipulating prices and causing users to receive fewer Flan tokens than the current market price dictates.

### Original Finding Content

_Submitted by hyh_

Trades can happen at a manipulated price and end up receiving fewer Flan to be bought than current market price dictates.

For example, at the time a user decides to call `buyFlanAndBurn` Flan trades at 0.8 in the input token terms at the corresponding DEX pool. If the input token holdings are big enough to compensate for pool manipulation costs, the following can happen: Flan buy order will be seen by a malicious bot, that buys Flan, pushing it to 0.9 before UniswapHelper's order comes through, and selling it back right afterwards. This way, given a cumulative impact of the trades on Flan's market price, the input token will be overspent.

This yields direct loss for the system as input token market operations have lesser effect than expected at the expense of contract holdings.

#### Proof of Concept

`buyFlanAndBurn` doesn't control for swap results, executing swaps with exchange pool provided amounts, which can be manipulated:

<https://github.com/code-423n4/2022-01-behodler/blob/main/contracts/UniswapHelper.sol#L231>

#### Recommended Mitigation Steps

Consider adding the minimum accepted price as a function argument so a user can limit the effective slippage, and check that actually received amount is above this accepted minimum.

Also, in the future it will prudent to add a relative version of the parameter to control percentage based slippage with TWAP Oracle price as a benchmark.

**[gititGoro (Behodler) acknowledged and commented](https://github.com/code-423n4/2022-01-behodler-findings/issues/230#issuecomment-1030495237):**
 > You're not wrong but remember that the tokens that can be called here are specifically those that are not listed on Limbo and likely never will be BUT that also have Flan pools. It's unlikely that these pools will ever be significantly large as no incentives are provided for their maintenance.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Behodler |
| Report Date | N/A |
| Finders | hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-behodler
- **GitHub**: https://github.com/code-423n4/2022-01-behodler-findings/issues/230
- **Contest**: https://code4rena.com/contests/2022-01-behodler-contest

### Keywords for Search

`vulnerability`

