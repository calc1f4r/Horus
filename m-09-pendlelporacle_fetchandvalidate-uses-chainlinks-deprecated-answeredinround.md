---
# Core Classification
protocol: LoopFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49046
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-loopfi
source_link: https://code4rena.com/reports/2024-07-loopfi
github_link: https://github.com/code-423n4/2024-07-loopfi-findings/issues/235

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

# Audit Details
report_date: unknown
finders_count: 46
finders:
  - 3
  - inh3l
  - 0xAadi
  - zhaojohnson
  - atoko
---

## Vulnerability Title

[M-09] `PendleLPOracle::_fetchAndValidate` uses Chainlink's deprecated `answeredInRound`

### Overview


The PendleLPOracle has a bug where it uses a deprecated function, `answeredInRound`, to get the price of its underlying asset from Chainlink. This results in incorrect prices being displayed. To fix this, the recommended solution is to remove the usage of `answeredInRound` in the `_fetchAndValidate` function. This bug has been confirmed and assessed as an issue with the Oracle.

### Original Finding Content


`PendleLPOracle` uses Chainlink to get the price of Pendle's underlying asset in ETH; this is done using `_fetchAndValidate`. That function uses `answeredInRound`, which is deprecated according to [Chainlink docs](https://docs.chain.link/data-feeds/api-reference#latestrounddata).

> `answeredInRound`:  Deprecated - Previously used when answers could take multiple rounds to be computed.

This results in invalid/wrong prices from Chainlink.

### Recommended Mitigation Steps

Remove the usage of `answeredInRound` in `PendleLPOracle::_fetchAndValidate`.

### Assessed type

Oracle

**[0xtj24 (LoopFi) confirmed](https://github.com/code-423n4/2024-07-loopfi-findings/issues/235#event-14359544567)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LoopFi |
| Report Date | N/A |
| Finders | 3, inh3l, 0xAadi, zhaojohnson, atoko, 4B, web3km, 0xAlix2, Infect3d, grearlake, BiasedMerc, NexusAudits, Rhaydden, y0ng0p3, EPSec, 0xjoaovpsantos, Sungyu, jolah1, emmac002, 0XRolko, Damola0x, unRekt, Sparrow, 0xhacksmithh, 0xBugSlayer, Spearmint, josephxander, crypticdefense, lightoasis, Bauchibred, Bigsam, 0xspryon, 1, 2, pks\_, novamanbg |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-loopfi
- **GitHub**: https://github.com/code-423n4/2024-07-loopfi-findings/issues/235
- **Contest**: https://code4rena.com/reports/2024-07-loopfi

### Keywords for Search

`vulnerability`

