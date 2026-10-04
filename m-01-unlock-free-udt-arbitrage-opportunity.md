---
# Core Classification
protocol: Unlock Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1077
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-unlock-protocol-contest
source_link: https://code4rena.com/reports/2021-11-unlock
github_link: https://github.com/code-423n4/2021-11-unlock-findings/issues/70

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
  - services
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - itsmeSTYJ
---

## Vulnerability Title

[M-01] Unlock: free UDT arbitrage opportunity

### Overview


This bug report is about an exploit related to Uniswap v2. It is possible for a malicious user to purchase many keys across many locks for the UDT token that is distributed to the referrer and sell them on some other exchanges where the price of UDT is higher. This is made possible because of the over dependency on a single price oracle and the flawed UDT token distribution logic. To mitigate this, it is recommended to use the average of multiple oracle sources so that the price of UDT tokens (from Unlock.sol's PoV) reacts faster and to base UDT token distribution on the duration of key ownership.

### Original Finding Content

_Submitted by itsmeSTYJ_

Uniswap v2 made oracle attacks much more expensive to execute (since it needs to be manipulated over X number of blocks) however its biggest drawback is that it reacts slow to price volatility (depends on how far back you look). Depending on a single oracle is still very risky and can be exploited given the correct conditions.

Assuming the ideal conditions, it is possible to purchase many keys across many locks for the UDT token that is distributed to the referrer and sell them on some other exchanges where the price of UDT is higher; high enough such that the malicious user can still profit even after requesting for a refund (w/ or w/o a free trial).

#### Proof of Concept

This exploit is made possible because of:

*   the over dependency on a single price oracle
*   UDT token distribution logic is flawed

The following assumptions has to be true for this attack to work:

1.  price of UDT on an exchange is much higher than that from the price retrieved from the `uniswapOracle`.
2.  Since the price retrieved by `udtOracle.updateAndConsult()` only updates once per day, it is slow to react to the volatility of UDT price movements.
3.  Malicious user creates a lock and buys many keys across multiple addresses.
4.  Malicious user sells these UDT tokens on the exchanges w/ the higher price.
5.  Malicious user requests for a refund on the keys owned.
6.  Repeat until it is no longer profitable i.e. price on other exchanges become close to parity with the price retrieved by the `uniswapOracle`.

#### Recommended Mitigation Steps

*   Use the average of multiple oracle sources so that the price of UDT tokens (from `Unlock.sol`'s PoV) reacts faster.
*   UDT tokens distributed based on the duration of key ownership.

**[julien51 (Unlock Protocol) disagreed with severity and commented](https://github.com/code-423n4/2021-11-unlock-findings/issues/70#issuecomment-1004137608):**
 > As you noted this is pretty theoretical and given that the amount of UDT minted is capped to the gas spent, the user will need to 1) purchase a LOT of keys and 2) cancel them all and 3) find an exchange where the price is significantly different. 

**[0xleastwood (judge) commented](https://github.com/code-423n4/2021-11-unlock-findings/issues/70#issuecomment-1010535323):**
 > Nice find!
> 
> While, I do agree this is a difficult attack to perform, it is still a valid way of extracting value from the protocol. Hence, I believe this should be kept as `medium`.
> 
> `
> 2 — Med (M): vulns have a risk of 2 and are considered “Medium” severity when assets are not at direct risk, but the function of the protocol or its availability could be impacted, or leak value with a hypothetical attack path with stated assumptions, but external requirements.
> `

**[julien51 (Unlock Protocol) commented](https://github.com/code-423n4/2021-11-unlock-findings/issues/70#issuecomment-1068788560):**
 > We will mitigate this in an upcoming upgrade by moving to Uniswap v3 for our oracles. 





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Unlock Protocol |
| Report Date | N/A |
| Finders | itsmeSTYJ |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-unlock
- **GitHub**: https://github.com/code-423n4/2021-11-unlock-findings/issues/70
- **Contest**: https://code4rena.com/contests/2021-11-unlock-protocol-contest

### Keywords for Search

`vulnerability`

