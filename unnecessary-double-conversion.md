---
# Core Classification
protocol: UMA Oval Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32587
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-oval-audit
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Unnecessary Double Conversion

### Overview

See description below for full details.

### Original Finding Content

The source adapter contracts interact with the incoming oracle interface that is ingested by the Oval system. The destination adapter contracts represent the standardized output interface that the Oval system exposes. In other words, the `ChainlinkSourceAdapter` is responsible for fetching the data from Chainlink, and the `ChainlinkDestinationAdapter` will return this data to the protocols implementing the Oval system. The data returned by `ChainlinkDestinationAdapter` should return the output decimals to match the decimals expected by the protocol. Optionally, if the source oracle's answer is based on a different decimals number than expected, the answer is converted using the [`DecimalLib` library](https://github.com/UMAprotocol/oev-contracts/blob/0f2c18660fc342ced7c7177577432f7d06481684/src/adapters/DecimalLib.sol).


However, within the source and destination contracts of [Chainlink](https://github.com/UMAprotocol/oev-contracts/tree/0f2c18660fc342ced7c7177577432f7d06481684/src/adapters/chainlink), the data is converted twice. Once when fetched by the source adapter and another time when returned by the destination adapter.


For example, when calling [`tryLatestDataAt`](https://github.com/UMAprotocol/oev-contracts/blob/0f2c18660fc342ced7c7177577432f7d06481684/src/adapters/chainlink/ChainlinkSourceAdapter.sol#L34) in the [`ChainlinkSourceAdapter`](https://github.com/UMAprotocol/oev-contracts/blob/0f2c18660fc342ced7c7177577432f7d06481684/src/adapters/chainlink/ChainlinkSourceAdapter.sol), the [answer returned](https://github.com/UMAprotocol/oev-contracts/blob/0f2c18660fc342ced7c7177577432f7d06481684/src/adapters/chainlink/ChainlinkSourceAdapter.sol#L42) is converted from the `sourceDecimals` to the expected output decimals. In the [`ChainlinkDestinationAdapter` contract](https://github.com/UMAprotocol/oev-contracts/blob/0f2c18660fc342ced7c7177577432f7d06481684/src/adapters/chainlink/ChainlinkDestinationAdapter.sol), when calling either [`latestAnswer`](https://github.com/UMAprotocol/oev-contracts/blob/0f2c18660fc342ced7c7177577432f7d06481684/src/adapters/chainlink/ChainlinkDestinationAdapter.sol#L23), [`latestTimestamp`](https://github.com/UMAprotocol/oev-contracts/blob/0f2c18660fc342ced7c7177577432f7d06481684/src/adapters/chainlink/ChainlinkDestinationAdapter.sol#L32), or [`latestRoundData`](https://github.com/UMAprotocol/oev-contracts/blob/0f2c18660fc342ced7c7177577432f7d06481684/src/adapters/chainlink/ChainlinkDestinationAdapter.sol#L46), the answer returned from the `internalLatestData` is converted again.


Moreover, when converting from a higher to lower decimal output and then from lower to higher again, the data returned will be altered and will not match the original answer.


Consider handling the conversion in a single contract to avoid conversion duplication and data loss.


***Update:** Acknowledged, not resolved. The Risk Labs team stated:*



> *We decided to not do anything in response to this issue. Specifically, we want all internal units within the OEVShare contracts to operate at 18 decimals to keep logic consistent and decimal independent within the OEVShare contracts. It also enables us to have different input and output decimals, by mixing and matching sources and destination adapters. Regarding loss of precision and the risk therein: this would only be the case if the input decimals are greater than 18 decimals. None of the feeds we want to use OEVshare on are more than 18 so there is no risk in this regard.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UMA Oval Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uma-oval-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

