---
# Core Classification
protocol: Olympus DAO
chain: everychain
category: oracle
vulnerability_type: stale_price

# Attack Vector Details
attack_type: stale_price
affected_component: oracle

# Source Information
source: solodit
solodit_id: 3228
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-08-olympus-dao-contest
source_link: https://code4rena.com/reports/2022-08-olympus
github_link: https://github.com/code-423n4/2022-08-olympus-findings/issues/441

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
  - stale_price
  - oracle
  - chainlink

protocol_categories:
  - liquid_staking
  - yield
  - cross_chain
  - leveraged_farming
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 21
finders:
  - Jujic
  - brgltd
  - pashov
  - 0xNazgul
  - Guardian
---

## Vulnerability Title

[M-24] [NAZ-M1] Chainlink's `latestRoundData` Might Return Stale Results

### Overview


This bug report is about a vulnerability that could lead to loss of funds to end-users. The vulnerability is caused by the use of Chainlink's `latestRoundData` API without a check on `updatedAt`. This could lead to the use of stale prices across various functions. Manual review was used to detect the vulnerability. To mitigate this vulnerability, it is recommended to add checks for stale data, such as checking that the answer to a round is being carried over from a previous round, and that the round is complete. This should ensure that the correct, up-to-date data is used.

### Original Finding Content

_Submitted by 0xNazgul, also found by &#95;&#95;141345&#95;&#95;, 0x1f8b, ak1, brgltd, cccz, csanuragjain, Dravee, Guardian, hyh, IllIllI, itsmeSTYJ, Jujic, Lambda, pashov, peachtea, rbserver, reassor, Sm4rty, TomJ, and zzzitron_

<https://github.com/code-423n4/2022-08-olympus/blob/main/src/modules/PRICE.sol#L161><br>
<https://github.com/code-423n4/2022-08-olympus/blob/main/src/modules/PRICE.sol#L170><br>

Across these contracts, you are using Chainlink's `latestRoundData` API, but there is only a check on `updatedAt`. This could lead to stale prices according to the Chainlink documentation:

*   [Historical Price data](https://docs.chain.link/docs/historical-price-data/#historical-rounds)
*   [Checking Your returned answers](https://docs.chain.link/docs/faq/#how-can-i-check-if-the-answer-to-a-round-is-being-carried-over-from-a-previous-round)

The result of `latestRoundData` API will be used across various functions, therefore, a stale price from Chainlink can lead to loss of funds to end-users.

### Recommended Mitigation Steps

Consider adding the missing checks for stale data.

For example:

```js
(uint80 roundID ,answer,, uint256 timestamp, uint80 answeredInRound) = AggregatorV3Interface(chainLinkAggregatorMap[underlying]).latestRoundData();

require(answer > 0, "Chainlink price <= 0"); 
require(answeredInRound >= roundID, "Stale price");
require(timestamp != 0, "Round not complete");
```

**[Oighty (Olympus) confirmed and commented](https://github.com/code-423n4/2022-08-olympus-findings/issues/441#issuecomment-1238528515):**
 > Agree. We'll add the additional checks.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Olympus DAO |
| Report Date | N/A |
| Finders | Jujic, brgltd, pashov, 0xNazgul, Guardian, rbserver, TomJ, Lambda, itsmeSTYJ, 0x1f8b, Sm4rty, csanuragjain, IllIllI, reassor, cccz, peachtea, zzzitron, ak1, __141345__, Dravee, hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-olympus
- **GitHub**: https://github.com/code-423n4/2022-08-olympus-findings/issues/441
- **Contest**: https://code4rena.com/contests/2022-08-olympus-dao-contest

### Keywords for Search

`Stale Price, Oracle, Chainlink`

