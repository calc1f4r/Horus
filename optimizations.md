---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33859
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#9-optimizations
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Optimizations

### Overview

See description below for full details.

### Original Finding Content

##### Description
Token rate range checks can be skipped if the token rate has the same value as the previous one https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/optimism/TokenRateOracle.sol#L146-L162.
During the removal of an observer, the removed one is overwritten by the last one: https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/lido/TokenRateNotifier.sol#L79. It can be optimized by doing so only if the removed one is not the last one.
`TOKEN_RATE_ORACLE.decimals()` is called every time when `ERC20RebasableBridged._getTokenRateAndDecimal()` is called:
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/token/ERC20RebasableBridged.sol#L291C30-L291C58.

##### Recommendation
We recommend adding a check that the token rate doesn't change and, in this case, skip range checks. Also, we recommend modifying the condition from `if (observers.length > 1)` to `if (observerIndexToRemove != observers.length - 1)`. Additionally, we recommend setting the oracle's decimals as an immutable in `ERC20RebasableBridged` or keeping it in the proxy's storage with the addition of a corresponding setter function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#9-optimizations
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

