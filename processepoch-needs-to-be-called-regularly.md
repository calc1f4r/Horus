---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7295
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - business_logic

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

processEpoch() needs to be called regularly

### Overview


This bug report is about a high-risk issue in the PublicVault.sol code. If the processEpoch() endpoint is not called regularly, the currentEpoch value will lag behind the expected value, causing errors in calculations related to epochs and timestamps. To fix this issue, Public Vaults need to create a mechanism to ensure that processEpoch() is called regularly, possibly using relayers or off-chain bots. Additionally, the vault should be topped up with assets and/or the current withdraw proxy to ensure that the full amount of withdraw reserves can be transferred to the withdraw proxy. Lastly, the current epoch should not just be incremented by one, but by an amount depending on the amount of time passed since the last call to processEpoch(). Both Astaria and Spearbit have acknowledged the recommendation.

### Original Finding Content

## Severity: High Risk

## Context
- PublicVault.sol#L247
- PublicVault.sol#L320

## Description
If the `processEpoch()` endpoint does not get called regularly (especially close to the epoch boundaries), the updated `currentEpoch` would lag behind the actual expected value, and this will introduce arithmetic errors in formulas regarding epochs and timestamps.

## Recommendation
Thus, public vaults need to create a mechanism so that the `processEpoch()` gets called regularly, maybe using relayers or off-chain bots. Also, if there are any outstanding withdraw reserves, the vault needs to be topped up with assets (and/or the current withdraw proxy) so that the full amount of withdraw reserves can be transferred to the withdraw proxy from the epoch before using `transferWithdrawReserve`. Otherwise, the processing of epochs would be halted, and if this halt continues for more than one epoch length, inaccuracies in the epoch number will be introduced into the system.

Another mechanism that can be introduced into the system is incrementing the current epoch not just by one but by an amount depending on the time passed since the last call to the `processEpoch()` or the timestamp of the current epoch.

## Acknowledgements
**Astaria:** Acknowledged.  
**Spearbit:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

