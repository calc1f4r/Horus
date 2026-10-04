---
# Core Classification
protocol: Ensuro Strategy Vault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58875
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ensuro-strategy-vault/a4501aea-a0fc-48be-96d4-ee148fdb9c79/index.html
source_link: https://certificate.quantstamp.com/full/ensuro-strategy-vault/a4501aea-a0fc-48be-96d4-ee148fdb9c79/index.html
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
  - Jennifer Wu
  - Ibrahim Abouzied
  - Rabib Islam
---

## Vulnerability Title

Hard-Coded `_price` Can Become Stale and Inaccurate in the Event of a Depeg

### Overview

See description below for full details.

### Original Finding Content

**Update**
The client acknowledged the issue and provided the following explanation:

> The SwapStableInvestStrategy is intented to be used with stablecoins or other situations where the peg is supposed to be strong. Some use cases are investing in USDM (yield bearing T-bill), or converting from Bridged USDC to Native USDC to get better yields on AAVE. In such cases, is hard to anticipate what to do in a depeg situation, so I don't think any code change can improve this situation that much. The current implementation, playing with the maxSlippage allows both panic sell (setting the maxSlippage high and withdrawing all the funds), and ad-hoc pause (setting maxSlippage=0). Also, another alternative to pause might be setting the strategy at the bottom of the deposit and withdraw queues.

**File(s) affected:**`SwapStableInvestStrategy.sol`

**Description:** The `SwapStableInvestStrategy` holds a fixed `_price` for the exchange rate between `_asset` and `_investAsset`. While this is sufficient for closely pegged assets, it becomes a risk if the peg is lost (e.g., stablecoin depegs) or if `_price` remains hard-coded despite market shifts. Users may then encounter large slippage, receive fewer tokens, or lose slippage protection if `_price` no longer matches real conditions. In extreme cases, it may become impossible to withdraw at the assumed `_price` unless `maxSlippage` is raised significantly.

**Recommendation:** Add a pause mechanism or allow a fast update of `_price` if a peg deviation occurs. Continuously monitor market rates and keep `_price` aligned with real conditions. This ensures prompt action in the event of depegging and avoids stale price risks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ensuro Strategy Vault |
| Report Date | N/A |
| Finders | Jennifer Wu, Ibrahim Abouzied, Rabib Islam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ensuro-strategy-vault/a4501aea-a0fc-48be-96d4-ee148fdb9c79/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ensuro-strategy-vault/a4501aea-a0fc-48be-96d4-ee148fdb9c79/index.html

### Keywords for Search

`vulnerability`

