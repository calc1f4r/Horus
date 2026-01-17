---
# Core Classification
protocol: Conic Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29912
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Conic%20Finance/Conic%20Finance%20v2/README.md#2-curvelporacle-is-not-working
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

`CurveLPOracle` is not working

### Overview


The bug report is about an issue with a sequence of code in the `GenericOracle.getUSDPrice` function. The first oracle in the sequence, `_chainlinkOracle`, is causing a problem because there is already a different oracle, `crvUSD`, being used on the mainnet. This means that the `CurveLPOracle` will never be used. The report suggests that the order of the oracles should be changed to prioritize the use of `customOracles` first.

### Original Finding Content

##### Description

- https://github.com/ConicFinance/protocol/blob/7a66d26ef84f93059a811a189655e17c11d95f5c/contracts/oracles/GenericOracle.sol#L34

`_chainlinkOracle` is the first in sequence in `GenericOracle.getUSDPrice`. 

Since there is already a `crvUSD` oracle on the mainnet, `CurveLPOracle` will never be used. Current `Aggregator` on mainnet for `crvUSD`: `0x145f040dbCDFf4cBe8dEBBd58861296012fCB269` (https://data.chain.link/ethereum/mainnet/stablecoins/crvusd-usd).

##### Recommendation
We recommended reprioritising the selection of Oracles (`customOracles` should be first). If necessary

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Conic Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Conic%20Finance/Conic%20Finance%20v2/README.md#2-curvelporacle-is-not-working
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

