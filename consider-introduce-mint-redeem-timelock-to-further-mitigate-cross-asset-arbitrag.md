---
# Core Classification
protocol: Berachain Honey
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52866
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Honey-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Honey-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 3
finders:
  - Rvierdiiev
  - 0xLadboy
  - Noah Marconi
---

## Vulnerability Title

Consider introduce mint / redeem timelock to further mitigate cross-asset arbitrage

### Overview

See description below for full details.

### Original Finding Content

Severity: Low Risk
Context: HoneyFactory.sol
Description: Protocol is aware that in case when there are multiple asset, user can mint honey with asset A and
redeem asset B.
An user can always enter with one asset and exit with the other.
As a result, any depeg creates an arbitrage opportunity:
• buy depegged asset
• mint at 1:1 honey
• redeem not-depegged assets
Recommendation: While adjusting minting and redeeming fee can partially reducer user's incentive to cross-
asset arbitrage.
It is recommended to introduce mint / redeem timelock to further mitigate the issue. Both adding fee and introduce
timelock can make such arbitrage non-profitable.
Berachain: Acknowledged. We expect honey to have a big user base. As a result a time lock could make many
transactions revert, resulting in a UX not acceptable. Furthermore, the time lock must be short and therefore the
abribtrage can still be executed relatively easily by a sophisticated actor.
Spearbit: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Berachain Honey |
| Report Date | N/A |
| Finders | Rvierdiiev, 0xLadboy, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Honey-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Honey-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

