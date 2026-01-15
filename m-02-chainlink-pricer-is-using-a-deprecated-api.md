---
# Core Classification
protocol: bunker.finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2215
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-bunkerfinance-contest
source_link: https://code4rena.com/reports/2022-05-bunker
github_link: https://github.com/code-423n4/2022-05-bunker-findings/issues/1

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
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 13
finders:
  - hake
  - IllIllI
  - 0xNazgul
  - tintin
  - cccz
---

## Vulnerability Title

[M-02] Chainlink pricer is using a deprecated API

### Overview


This bug report is about the PriceOracleImplementation.sol code on the Bunker Protocol GitHub repository. According to Chainlink's documentation, the latestAnswer function is deprecated and can suddenly stop working if Chainlink stops supporting deprecated APIs. This can cause the API to return stale data. The recommended mitigation step is to use the latestRoundData function to get the price instead, and to add checks on the return data with proper revert messages if the price is stale or the round is uncomplete.

### Original Finding Content


According to Chainlink's documentation, the latestAnswer function is deprecated. This function might suddenly stop working if Chainlink stop supporting deprecated APIs. And the old API can return stale data.

### Proof of Concept

[PriceOracleImplementation.sol#L29-L30](https://github.com/bunkerfinance/bunker-protocol/blob/752126094691e7457d08fc62a6a5006df59bd2fe/contracts/PriceOracleImplementation.sol#L29-L30)<br>

### Recommended Mitigation Steps

Use the latestRoundData function to get the price instead. Add checks on the return data with proper revert messages if the price is stale or the round is uncomplete
<https://docs.chain.link/docs/price-feeds-api-reference/>

**[bunkerfinance-dev (bunker.finance) confirmed](https://github.com/code-423n4/2022-05-bunker-findings/issues/1)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | bunker.finance |
| Report Date | N/A |
| Finders | hake, IllIllI, 0xNazgul, tintin, cccz, sorrynotsorry, 0xDjango, Ruhum, throttle, kebabsec, oyc_109, 0x1f8b, GimelSec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-bunker
- **GitHub**: https://github.com/code-423n4/2022-05-bunker-findings/issues/1
- **Contest**: https://code4rena.com/contests/2022-05-bunkerfinance-contest

### Keywords for Search

`vulnerability`

