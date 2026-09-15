---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3926
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-04-vader
github_link: https://github.com/code-423n4/2021-04-vader-findings/issues/210

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
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-23] Anyone can curate pools and steal rewards

### Overview


This bug report is about a vulnerability in the Router.curatePool and replacePool functions. These functions do not have any access restriction, which makes it possible for an attacker to get a flash loan of base tokens and replace existing curated pools with their own curated pools. This can be used to manipulate the rewards system, as the attacker can remove rewards from a curated pool and add rewards to their own pool with a custom token they control. To mitigate this vulnerability, it is recommended to prevent replacing curations through flash loans and consider making pool curations DAO-exclusive actions.

### Original Finding Content


The `Router.curatePool` and `replacePool` don't have any access restriction.
An attacker can get a flash loan of base tokens and replace existing curated pools with their own curated pools.

Curated pools determine if a pool receives rewards. An attacker can remove rewards of a curated pool this way and add rewards to their own pool with a custom token they control.
They can then go ahead and game the reward system by repeatedly swapping in their custom pool with useless tokens, withdraw liquidity, and in the end, pay back the base flashloan.

Recommend preventing the replacing of curations through flash loans. Also, consider making pool curations DAO-exclusive actions.

**[strictly-scarce (vader) disputed](https://github.com/code-423n4/2021-04-vader-findings/issues/210#issuecomment-828473380):**
 > Slip-based pools cannot be attacked with flash loans.

**[dmvt (judge) commented](https://github.com/code-423n4/2021-04-vader-findings/issues/210#issuecomment-849131582):**
 > Further comment from @cmichelio:
>
> I can curate my custom token using `curatePool` without using a flashloan or using replacePool by temporarily providing liquidity to the pool without trading in it and getting slip-fee'd. I'm not trading in the pool, and don't think providing/removing liquidity comes with a fee. I think this is still an issue.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-vader
- **GitHub**: https://github.com/code-423n4/2021-04-vader-findings/issues/210
- **Contest**: https://code4rena.com/contests/2021-04-vader-protocol-contest

### Keywords for Search

`vulnerability`

