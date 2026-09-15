---
# Core Classification
protocol: Yearn Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28435
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/SNX/README.md#1-sandwich-attack-on-user-withdrawal
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

"Sandwich attack" on user withdrawal

### Overview


This bug report is about a vulnerability in a strategy using an Automated Market Maker (AMM) decentralized exchange (DEX) to swap SNX to SUSD. This vulnerability is known as the "sandwich attack". Although the conditions for this vulnerability to be exploited are rare, it is recommended to protect AMM DEX swap operations with a slippage technique. A slippage technique is a way of ensuring that transactions are successful by allowing a certain amount of price fluctuation, which can help to prevent the "sandwich attack".

### Original Finding Content

##### Description
In some rare conditions, the strategy is using AMM DEX to [swap SNX to SUSD](https://github.com/jmonteer/yearnV2-strat-SNX-staking/blob/91b839df4a350d80cb583795bccafe0836fdb732/contracts/Strategy.sol#L348) inside of the user-handled transaction. This is vulnerable to the "sandwich attack".

##### Recommendation
Although vulnerability conditions are rare and hard to exploit, it is recommended to protect AMM DEX swap operations with slippage technique.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Yearn Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/SNX/README.md#1-sandwich-attack-on-user-withdrawal
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

