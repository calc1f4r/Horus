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
solodit_id: 52860
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

V2: Mint and Redeem rates initialize to 0 allowing for 100% fee

### Overview

See description below for full details.

### Original Finding Content

Severity: Low Risk
Context: HoneyFactory.sol#L125-L136, HoneyFactory.sol#L139-L150, HoneyFactory.sol#L216-L225,
HoneyFactory.sol#L495-L496, HoneyFactory.sol#L481
Description: HoneyFactory.setRedeemRate allows the MANAGER_ROLE to set what proportion of shares being
redeemed remain after fees applied. The bounds are strictly enforced to be between 98% and 100% to restrict
fees to a maximum of 2% total.
HoneyFactory.createVault does not initialize redeemRates[asset] making the default 0. This pushes the unini-
tialized fee to be 100% (significantly above the intended cap of 2%).
A similar issue occurs for mintRates[asset] .
Recommendation: Similar to priceFeedMaxDelay , lowerPegOffsets , and upperPegOffsets , setting redeem-
Rates[asset]‘ to sound defaults (or no fees at all) would solve the unitialized value issue.
A less gas efficient but more strict safeguard may be added on mint and redeem to ensure fees are not in excess
of the 2% cap.
Berachain: Acknowledged.
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

