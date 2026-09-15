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
solodit_id: 33867
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#17-withdrawn-steth-gets-stuck-on-the-bridge-if-the-recipient-is-an-steth-address-on-l1
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

Withdrawn stETH gets stuck on the bridge if the recipient is an stETH address on L1

### Overview

See description below for full details.

### Original Finding Content

##### Description
stETH on L1 doesn't permit transfers to the token's own address:
https://github.com/lidofinance/lido-dao/blob/5fcedc6e9a9f3ec154e69cff47c2b9e25503a78a/contracts/0.4.24/StETH.sol#L444.
However, there are no restrictions in `L2ERC20ExtendedTokensBridge.withdrawTo()` to use such address as a recipient:
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/optimism/L2ERC20ExtendedTokensBridge.sol#L97
So, if someone uses it as a withdrawal address, tokens will be successfully burnt on L2 but the finalization on L1 will always revert:
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/optimism/L1ERC20ExtendedTokensBridge.sol#L114.

Sending tokens to any incorrect address will likely lead to the loss of funds. At the same time having tokens stuck on the bridge is also an undesirable scenario.

##### Recommendation
We recommend adding a check in `L2ERC20ExtendedTokensBridge.withdrawTo()` that the recipient is not an stETH address on L1.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#17-withdrawn-steth-gets-stuck-on-the-bridge-if-the-recipient-is-an-steth-address-on-l1
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

