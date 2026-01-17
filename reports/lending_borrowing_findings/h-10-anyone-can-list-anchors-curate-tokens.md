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
solodit_id: 3913
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-04-vader
github_link: https://github.com/code-423n4/2021-04-vader-findings/issues/211

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

[H-10] Anyone can list anchors / curate tokens

### Overview


This bug report is about the vulnerability in the `Router.listAnchor` function, which can be called by anyone and tokens can be added with just a simple check. This allows anyone to remove rewards from a curated pool and add rewards to their own pool with a token they control. The impact of this vulnerability is that attackers can manipulate the anchor price and launch other attacks by withdrawing the liquidity.

The recommended mitigation steps to address this vulnerability is to revisit the `_isAnchor[token] = true;` statement in `addLiquidity` and make `listAnchor` / `replaceAnchor` DAO-only functions that are flash-loan secure. Additionally, one should use time-weighted prices for these pools for the bounds check.

### Original Finding Content


The `Router.listAnchor` function can be called by anyone and tokens can be added. The only check is that `require(iPOOLS(POOLS).isAnchor(token));` but this can easily be set by calling `Pools.addLiquidity(VADER, token, _)` once even without actually sending any tokens to the contract. This makes it an essentially useless check.

This only works initially as long as the `anchorLimit` has not been reached yet.
However, the `replaceAnchor` can be used in the same way and flash loans can be used to get around the liquidity restrictions and push another anchor token out of the price range as these checks use the current reserves.

Anchored pools are automatically curated pools and determine if a pool receives rewards. An attacker can remove rewards of a curated pool this way and add rewards to their own pool with a custom token they control.

After a pool has been anchored through flash loans, liquidity can be withdrawn which could make the anchor price easy to manipulate in the next block and launch other attacks.

Recommend revisiting the `_isAnchor[token] = true;` statement in `addLiquidity`, it seems strange without any further checks.
Consider making `listAnchor` / `replaceAnchor` DAO-only functions and make them flash-loan secure.
One should probably use time-weighted prices for these pools for the bounds check.

**[strictly-scarce (vader) disputed](https://github.com/code-423n4/2021-04-vader-findings/issues/211#issuecomment-828472672):**
 > The protocol is intended to be launched with 5 anchors so it can only be attacked by using `replaceAnchor()`, in which case slip-based fees apply for attacks and thwart the attack path.



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
- **GitHub**: https://github.com/code-423n4/2021-04-vader-findings/issues/211
- **Contest**: https://code4rena.com/contests/2021-04-vader-protocol-contest

### Keywords for Search

`vulnerability`

