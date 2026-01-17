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
solodit_id: 33863
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#13-transfers-of-zero-value
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

Transfers of zero value

### Overview

See description below for full details.

### Original Finding Content

##### Description
Due to rounding errors, non-zero stETH amount can be converted to 0 wstETH:
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/optimism/L1ERC20ExtendedTokensBridge.sol#L137
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/optimism/L2ERC20ExtendedTokensBridge.sol#L152
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/token/ERC20RebasableBridged.sol#L236

So, no tokens will be actually transfered, but a `Transfer` event with a non-zero amount will be emitted: https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/token/ERC20RebasableBridged.sol#L362,

and non-zero `allowance` will be spent: https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/token/ERC20RebasableBridged.sol#L161.

It can be done even if the caller or `from_` address has a zero balance. If some offchain service relies on `Transfer` events, it could lead to broken invariants. 

The original stETH on L1 follows the same logic: https://github.com/lidofinance/lido-dao/blob/5fcedc6e9a9f3ec154e69cff47c2b9e25503a78a/contracts/0.4.24/StETH.sol#L375.

##### Recommendation
We recommend restricting the transfer of 0 shares because it is an abnormal behavior of the system for a user to spend a non-zero approval to transfer 0 amount of tokens.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#13-transfers-of-zero-value
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

