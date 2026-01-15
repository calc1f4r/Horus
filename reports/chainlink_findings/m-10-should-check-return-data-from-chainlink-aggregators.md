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
solodit_id: 1029
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/120

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
finders_count: 1
finders:
  - defsec
---

## Vulnerability Title

[M-10] SHOULD CHECK RETURN DATA FROM CHAINLINK AGGREGATORS

### Overview


This bug report is about the consult function in the contract TwapOracle.sol. This function fetches the asset price from a Chainlink aggregator using the latestRoundData function. However, this function does not check the timeStamp, which results in stale prices. If there is a problem with chainlink starting a new round and finding consensus on the new value for the oracle, consumers of this contract may continue using outdated stale data. 

The recommended mitigation steps to fix this bug include adding checks on the return data with proper revert messages if the price is stale or the round is incomplete. It is also recommended to check the oracle responses updatedAt value after calling out to chainlinkOracle.latestRoundData() verifying that the result is within an allowed margin of freshness.

### Original Finding Content

_Submitted by defsec_

#### Impact

The consult function in the contract TwapOracle.sol fetches the asset price from a Chainlink aggregator using the latestRoundData function. However, there are no checks on timeStamp, resulting in stale prices. The oracle wrapper calls out to a chainlink oracle receiving the latestRoundData(). It then checks freshness by verifying that the answer is indeed for the last known round. The returned updatedAt timestamp is not checked.

If there is a problem with chainlink starting a new round and finding consensus on the new value for the oracle (e.g. chainlink nodes abandon the oracle, chain congestion, vulnerability/attacks on the chainlink system) consumers of this contract may continue using outdated stale data (if oracles are unable to submit no new round is started)

#### Proof of Concept

1.  Navigate to "<https://github.com/code-423n4/2021-11-vader/blob/607d2b9e253d59c782e921bfc2951184d3f65825/contracts/twap/TwapOracle.sol#L141>" contract.

2.  consult function does not check timestamp on the latestRoundData.

#### Tools Used

None

#### Recommended Mitigation Steps

Consider to add checks on the return data with proper revert messages if the price is stale or the round is incomplete, for example:

    (uint80 roundID, int256 price, , uint256 timeStamp, uint80 answeredInRound) = ETH_CHAINLINK.latestRoundData();
    require(timeStamp != 0, "...");

Consider checking the oracle responses updatedAt value after calling out to chainlinkOracle.latestRoundData() verifying that the result is within an allowed margin of freshness.

- <https://docs.chain.link/docs/faq/#how-can-i-check-if-the-answer-to-a-round-is-being-carried-over-from-a-previous-round>

- <https://blog.openzeppelin.com/secure-smart-contract-guidelines-the-dangers-of-price-oracles/>

**[SamSteinGG (Vader) confirmed](https://github.com/code-423n4/2021-11-vader-findings/issues/120)**
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
| Finders | defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/120
- **Contest**: https://code4rena.com/contests/2021-11-vader-protocol-contest

### Keywords for Search

`vulnerability`

