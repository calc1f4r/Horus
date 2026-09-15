---
# Core Classification
protocol: Level Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60876
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
source_link: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
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
finders_count: 4
finders:
  - Jeffrey Kam
  - Mustafa Hasan
  - Rabib Islam
  - Guillermo Escobero
---

## Vulnerability Title

Liquidity Can Be Drained Through Price Manipulation

### Overview


The bug report discusses a potential issue with Level Finance, a trading platform that allows users to take leveraged positions on various tokens. The report notes that the size of these positions is currently only limited by the amount of liquidity in the platform's pool, making it vulnerable to economic attacks. The report suggests implementing tranches for liquidity providers (LPs) to limit their exposure to trades conducted with assets with low liquidity. However, this approach is flawed as it assumes that certain assets, like BTC and ETH, will not be manipulated in the future. The report recommends implementing global limits on both short and long positions for all tokens, calculated based on the depth of liquidity on Binance and Coinbase. This would help protect LPs from potential losses and prevent large amounts of risky assets, like CAKE, from being deposited. 

### Original Finding Content

**Update**
Fixed. Global long and short position sizes can now be limited across the range of tokens. However, it is up to the client to correctly set these limits.

**File(s) affected:**`Pool.sol`

**Description:** Level Finance allows traders to take leveraged long and short positions on various tokens, and the size of these positions is limited only by the amount of liquidity stored in the `Pool`. These trades can be executed with zero price impact. The same is the case for the swaps facilitated by the protocol between these tokens. The prices that are honoured by the protocol are produced by oracles referring to Coinbase and Binance, and validated against Chainlink's oracle.

This opens the protocol to an economic attack whereby a trader can open positions on Level Finance, manipulate the oracle prices through action on centralized exchanges, and close the positions.

Level Finance aims to correct for this issue by providing LPs tranches, whereby LPs can limit their exposure to trades conducted in assets with low liquidity on exchanges from which the oracles derive their prices. The underlying assumption is that the prices of certain tokens (e.g. BTC, ETH) are less manipulable than others. Currently, the token considered risky, CAKE, only has allocation within the mezzanine and junior tranches, and has only a 1% target weight across the entire pool.

This single-faceted approach to dealing with the described attack vector is flawed on at least two counts:

1.   The assumption that prices of assets like BTC and ETH will not be manipulated in the future may ultimately be proven false. If so, the up-to-30x leverage provided by Level Finance could allow the opening of positions that, when closed, could lead to serious losses for Level Finance LPs.
2.   Although the target weight for CAKE liquidity is 1% (Level Finance's current CAKE holdings amount to $138,677), depending on the growth of Level Finance, this could lead to substantially larger amounts of CAKE being deposited.

**Recommendation:** Level Finance should impose global limits on both short and long position sizes for all tokens. Ideally, these limits should be decided in a calculated manner, referencing the depth of liquidity on both Binance and Coinbase.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Level Finance |
| Report Date | N/A |
| Finders | Jeffrey Kam, Mustafa Hasan, Rabib Islam, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html

### Keywords for Search

`vulnerability`

