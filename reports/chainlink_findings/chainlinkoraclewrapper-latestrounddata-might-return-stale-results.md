---
# Core Classification
protocol: Fei Protocol v2 Phase 1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13303
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/09/fei-protocol-v2-phase-1/
github_link: none

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
  - liquid_staking
  - bridge
  - yield
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Sergii Kravchenko
  -  Bernhard Gomig

  -  Martin Ortner
  -  Eli Leers
  -  Heiko Fisch
---

## Vulnerability Title

ChainlinkOracleWrapper - latestRoundData might return stale results

### Overview


This bug report is about a problem with the oracle wrapper calls out to a chainlink oracle receiving the `latestRoundData()`. It checks freshness by verifying that the answer is indeed for the last known round, but the returned `updatedAt` timestamp is not checked. This means that if there is a problem with chainlink starting a new round and finding consensus on the new value for the oracle (e.g. chainlink nodes abandon the oracle, chain congestion, vulnerability/attacks on the chainlink system), consumers of this contract may continue using outdated stale data (if oracles are unable to submit no new round is started).

The report provides code snippets from the ChainlinkOracleWrapper.sol file, which shows the functions read() and isOutdated(). The read() function reads the oracle price and checks if it is valid, while the isOutdated() function determines if the read value is stale.

The recommendation is to consider checking the oracle responses `updatedAt` value after calling out to `chainlinkOracle.latestRoundData()` verifying that the result is within an allowed margin of freshness. This will ensure that the data used by the contract is up-to-date and accurate.

### Original Finding Content

#### Description


The oracle wrapper calls out to a chainlink oracle receiving the `latestRoundData()`. It then checks freshness by verifying that the answer is indeed for the last known round. The returned `updatedAt` timestamp is not checked.


If there is a problem with chainlink starting a new round and finding consensus on the new value for the oracle (e.g. chainlink nodes abandon the oracle, chain congestion, vulnerability/attacks on the chainlink system) consumers of this contract may continue using outdated stale data (if oracles are unable to submit no new round is started)


#### Examples


**code/contracts/oracle/ChainlinkOracleWrapper.sol:L49-L58**



```
/// @notice read the oracle price
/// @return oracle price
/// @return true if price is valid
function read() external view override returns (Decimal.D256 memory, bool) {
    (uint80 roundId, int256 price,,, uint80 answeredInRound) = chainlinkOracle.latestRoundData();
    bool valid = !paused() && price > 0 && answeredInRound == roundId;

    Decimal.D256 memory value = Decimal.from(uint256(price)).div(oracleDecimalsNormalizer);
    return (value, valid);
}

```
**code/contracts/oracle/ChainlinkOracleWrapper.sol:L42-L47**



```
/// @notice determine if read value is stale
/// @return true if read value is stale
function isOutdated() external view override returns (bool) {
    (uint80 roundId,,,, uint80 answeredInRound) = chainlinkOracle.latestRoundData();
    return answeredInRound != roundId;
}

```
#### Recommendation


Consider checking the oracle responses `updatedAt` value after calling out to `chainlinkOracle.latestRoundData()` verifying that the result is within an allowed margin of freshness.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Fei Protocol v2 Phase 1 |
| Report Date | N/A |
| Finders | Sergii Kravchenko,  Bernhard Gomig
,  Martin Ortner,  Eli Leers,  Heiko Fisch |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/09/fei-protocol-v2-phase-1/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

