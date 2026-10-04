---
# Core Classification
protocol: Coinbase Liquid Staking Token Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10521
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/coinbase-liquid-staking-token-audit/
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
  - OpenZeppelin
---

## Vulnerability Title

[M01] Insufficient allowance of the callers can prevent the update of exchange rate

### Overview


The RateLimit contract allows the owner to configure the allowance of the caller, which decreases when the caller mints new tokens or updates the exchange rate. A rare scenario can occur where the allowance of all of the callers is insufficient to update the exchange rate, which could impact the trading of staked tokens. The severity of this issue depends on the number of callers and their setup parameters. Coinbase acknowledges this risk and will have a cold key with sufficient allowance to account for all exchange rate updates. However, Coinbase's on-chain exchange rate may become out of date in the event of a loss of funds due to slashing of staked ETH, as the staked ETH slashing period happens over the course of several weeks. To prevent this from happening, Coinbase should ensure that there is a sufficient number of callers interacting with the system and that they have enough allowance to maintain the health of the system.

### Original Finding Content

The owner of the `RateLimit` contract configures the allowance of the `caller` which decreases as when the caller mints new tokens or updates the exchange rate and it increases up to a `maxAllowance` parameter with a time schedule dictated by the rate limit functionality.


A rare scenario can happen where the allowance of all of the callers is insufficient to update the exchange rate, and the replenishment of allowance needs a long wait time. Given the volatility of the crypto market, if the exchange rate is not updated timely, systems and protocols depending on it can be dramatically affected and the trading of the staked tokens could be impacted.


The severity of this issue depends on the number of callers or which schedules and parameters are meant to be setup for callers. At the time of this audit, there is no documentation stating the number of callers and their setup parameters which are intended to interact with the system. The lesser number of callers or larger intervals with low allowances, the more likelihood of this situation can occur. We recommend to ensure that, at all times, there are sufficient number of callers interacting with the system and they have enough allowance to maintain the health of the system.


***Update:** Acknowledged.*



> Coinbase acknowledges this risk and will have a cold key that has sufficient allowance to account for all exchange rate updates at all times. Coinbase’s on-chain exchange rate may become out of date in the event of a loss of funds due to slashing of staked ETH, as the staked ETH slashing period happens over the course of several weeks, and we cannot know the extent of loss until the end of that period.
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Coinbase Liquid Staking Token Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/coinbase-liquid-staking-token-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

