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
solodit_id: 42351
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-11-vader
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/151

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

[M-15] Lacking Validation Of Chainlink' Oracle Queries

### Overview


The bug report states that the `TwapOracle.consult()` function is missing important checks to ensure that the round is complete and the price returned is valid. This can lead to unexpected results and cause problems in other parts of the protocol. Additionally, the `GasThrottle.validateGas()` function uses a method that does not have enough checks for outdated data. The report recommends using a different method to avoid this issue. The bug was found through a manual code review and the use of Chainlink best practices. To fix the issue, the report suggests adding validations to the `TwapOracle.consult()` and `GasThrottle.validateGas()` functions and using a different method, `latestRoundData()`, instead of the current method, `latestAnswer()`. The team behind the protocol has confirmed the bug and has already removed the problematic code and redesigned the oracle module.

### Original Finding Content

_Submitted by leastwood_

#### Impact

`TwapOracle.consult()` is missing additional validations to ensure that the round is complete and has returned a valid/expected price. The `consult()` improperly casts an `int256 price` to `uint256` without first checking the value. As a result, the variable may underflow and return an unexpected result, potentially causing further issues in other areas of the protocol that rely on this function.

Additionally, the `GasThrottle.validateGas()` modifier utilises Chainlink's `latestAnswer()` function which lacks additional checks for stale data. The `latestRoundData()` function facilitates additional checks and should be used over `latestAnswer()`.

#### Proof of Concept

- <https://github.com/code-423n4/2021-11-vader/blob/main/contracts/twap/TwapOracle.sol#L134-L150>
- <https://github.com/code-423n4/2021-11-vader/blob/main/contracts/dex/utils/GasThrottle.sol#L15>
- <https://docs.chain.link/docs/faq/#how-can-i-check-if-the-answer-to-a-round-is-being-carried-over-from-a-previous-round>

#### Tools Used

Manual code review.
Chainlink best practices.

#### Recommended Mitigation Steps

Consider validating the output of `latestRoundData()` to match the following code snippet:

         (
            uint80 roundID,
            int256 price,
            ,
            uint256 updateTime,
            uint80 answeredInRound
          ) = ETH_CHAINLINK.latestRoundData();
          require(
              answeredInRound >= roundID,
              "Chainlink Price Stale"
          );
          require(price > 0, "Chainlink Malfunction");
          require(updateTime != 0, "Incomplete round");

This needs to be updated in `TwapOracle.consult()` and in `GasThrottle.validateGas()`. The latter instance should have the `latestAnswer()` function replaced with `latestRoundData()` in order to avoid stale data.

**[SamSteinGG (Vader) confirmed](https://github.com/code-423n4/2021-11-vader-findings/issues/151)** 
>The TWAP oracle module has been completely removed and redesigned from scratch as LBTwap that is subject of the new audit.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/151
- **Contest**: https://code4rena.com/reports/2021-11-vader

### Keywords for Search

`vulnerability`

