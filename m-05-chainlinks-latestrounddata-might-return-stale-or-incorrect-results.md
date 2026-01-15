---
# Core Classification
protocol: Mochi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42301
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-10-mochi
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/87

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
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-05] Chainlink's `latestRoundData` might return stale or incorrect results

### Overview


A bug has been found in the ChainlinkAdapter contract, which is used to call out to a Chainlink oracle and receive the latestRoundData. This can cause issues if there are problems with Chainlink starting a new round or finding consensus on the new value for the oracle. This can lead to consumers of the contract using outdated or incorrect data. To mitigate this, it is recommended to add certain checks to the contract. References and confirmation of the bug have been provided.

### Original Finding Content

_Submitted by nikitastupin, also found by cmichel, defsec, leastwood, and WatchPug_

#### Proof of Concept
[`ChainlinkAdapter.sol` L49](https://github.com/code-423n4/2021-10-mochi/blob/8458209a52565875d8b2cefcb611c477cefb9253/projects/mochi-cssr/contracts/adapter/ChainlinkAdapter.sol#L49)

The `ChainlinkAdapter` calls out to a Chainlink oracle receiving the `latestRoundData()`. If there is a problem with Chainlink starting a new round and finding consensus on the new value for the oracle (e.g. Chainlink nodes abandon the oracle, chain congestion, vulnerability/attacks on the chainlink system) consumers of this contract may continue using outdated stale or incorrect data (if oracles are unable to submit no new round is started).

#### Recommended Mitigation Steps
Recommend adding the following checks:
```solidity
    ( roundId, rawPrice, , updateTime, answeredInRound ) = AggregatorV3Interface(XXXXX).latestRoundData();
    require(rawPrice > 0, "Chainlink price <= 0");
    require(updateTime != 0, "Incomplete round");
    require(answeredInRound >= roundId, "Stale price");
```
#### References
*   <https://consensys.net/diligence/audits/2021/09/fei-protocol-v2-phase-1/#chainlinkoraclewrapper-latestrounddata-might-return-stale-results>
*   <https://github.com/code-423n4/2021-05-fairside-findings/issues/70>

**[ryuheimat (Mochi) confirmed](https://github.com/code-423n4/2021-10-mochi-findings/issues/87)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/87
- **Contest**: https://code4rena.com/reports/2021-10-mochi

### Keywords for Search

`vulnerability`

