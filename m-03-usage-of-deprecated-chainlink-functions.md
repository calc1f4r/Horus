---
# Core Classification
protocol: Rolla
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1688
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-rolla-contest
source_link: https://code4rena.com/reports/2022-03-rolla
github_link: https://github.com/code-423n4/2022-03-rolla-findings/issues/17

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
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - cccz
  - WatchPug
  - Ruhum
  - 0x1f8b
---

## Vulnerability Title

[M-03] Usage of deprecated Chainlink functions

### Overview


This bug report is about the Chainlink functions `latestAnswer()` and `getAnswer()` being deprecated. This means that they should no longer be used in the code. Instead, the functions `latestRoundData()` and `getRoundData()` should be used. To verify this, one can go to the Etherscan website and search for `latestAnswer()` or `getAnswer()` to find the deprecation notice. The recommended mitigation step for this issue is to switch to `latestRoundData()` as described in the Chainlink documentation.

### Original Finding Content

_Submitted by Ruhum, also found by 0x1f8b, cccz, and WatchPug_

The Chainlink functions `latestAnswer()` and `getAnswer()` are deprecated. Instead, use the [`latestRoundData()`](https://docs.chain.link/docs/price-feeds-api-reference/#latestrounddata) and [`getRoundData()`](https://docs.chain.link/docs/price-feeds-api-reference/#getrounddata) functions.

### Proof of Concept

[ChainlinkOracleManager.sol#L120](https://github.com/code-423n4/2022-03-rolla/blob/main/quant-protocol/contracts/pricing/oracle/ChainlinkOracleManager.sol#L120)<br>

[ChainlinkFixedTimeOracleManager.sol#L81](https://github.com/code-423n4/2022-03-rolla/blob/main/quant-protocol/contracts/pricing/oracle/ChainlinkFixedTimeOracleManager.sol#L81)<br>

[ChainlinkFixedTimeOracleManager.sol#L84](https://github.com/code-423n4/2022-03-rolla/blob/main/quant-protocol/contracts/pricing/oracle/ChainlinkFixedTimeOracleManager.sol#L84)<br>

Go to <https://etherscan.io/address/0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419#code> and search for `latestAnswer()` or `getAnswer()`. You'll find the deprecation notice.

### Recommended Mitigation Steps

Switch to `latestRoundData()` as described [here](https://docs.chain.link/docs/price-feeds-api-reference/#latestrounddata).

**[0xca11 (Rolla) confirmed, resolved, and commented](https://github.com/code-423n4/2022-03-rolla-findings/issues/17#issuecomment-1102151105):**
 > Fixed in [RollaProject/quant-protocol#89](https://github.com/RollaProject/quant-protocol/pull/89).


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Rolla |
| Report Date | N/A |
| Finders | cccz, WatchPug, Ruhum, 0x1f8b |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-rolla
- **GitHub**: https://github.com/code-423n4/2022-03-rolla-findings/issues/17
- **Contest**: https://code4rena.com/contests/2022-03-rolla-contest

### Keywords for Search

`vulnerability`

