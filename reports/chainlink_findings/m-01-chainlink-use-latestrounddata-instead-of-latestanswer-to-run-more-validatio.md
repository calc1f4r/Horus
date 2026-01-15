---
# Core Classification
protocol: Wild Credit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42244
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-07-wildcredit
source_link: https://code4rena.com/reports/2021-07-wildcredit
github_link: https://github.com/code-423n4/2021-07-wildcredit-findings/issues/75

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-01] Chainlink - Use `latestRoundData` instead of `latestAnswer` to run more validations

### Overview


The bug report is about an issue with the `UniswapV3Oracle.sol` code, which is used to get the last WETH price. The current method being used, `latestAnswer`, only returns the last value but does not check if the data is fresh. This can cause problems as the data may not be up to date. The report suggests using the `latestRoundData` method instead, which allows for extra validations to be run. The report also mentions that the Chainlink documentation has more information on this issue. The bug has been confirmed by a user named talegift and commented on by ghoul-sol, who has raised the risk level to medium due to the potential consequences of incorrect price data. 

### Original Finding Content

_Submitted by a_delamo, also found by 0xRajeev, cmichel, greiart, and shw_

`UniswapV3Oracle.sol` is calling `latestAnswer` to get the last WETH price. This method will return the last value, but you won't be able to check if the data is fresh.
On the other hand, calling the method `latestRoundData` allow you to run some extra validations

```solidity
  (
    roundId,
    rawPrice,
    ,
    updateTime,
    answeredInRound
  ) = AggregatorV3Interface(XXXXX).latestRoundData();
  require(rawPrice > 0, "Chainlink price <= 0");
  require(updateTime != 0, "Incomplete round");
  require(answeredInRound >= roundId, "Stale price");
```

See the chainlink [documentation](https://docs.chain.link/docs/faq/#how-can-i-check-if-the-answer-to-a-round-is-being-carried-over-from-a-previous-round) for more information.

**[talegift (Wild Credit) confirmed](https://github.com/code-423n4/2021-07-wildcredit-findings/issues/75)**

**[ghoul-sol (Judge) commented](https://github.com/code-423n4/2021-07-wildcredit-findings/issues/75#issuecomment-890584877):**
 > Since slate prices could have quite serious consequences, I'll bump it to medium risk.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Wild Credit |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-wildcredit
- **GitHub**: https://github.com/code-423n4/2021-07-wildcredit-findings/issues/75
- **Contest**: https://code4rena.com/reports/2021-07-wildcredit

### Keywords for Search

`vulnerability`

