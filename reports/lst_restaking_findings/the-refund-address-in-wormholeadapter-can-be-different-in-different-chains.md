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
solodit_id: 34415
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#8-the-refund-address-in-wormholeadapter-can-be-different-in-different-chains
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

The refund address in `WormholeAdapter` can be different in different chains

### Overview

See description below for full details.

### Original Finding Content

##### Description
`REFUND_ADDRESS` in `WormholeAdapter` is immutable. However, the address of the controller can be different in different chains. Using one `WormholeAdapter` for multiple chains can lead to the loss of gas refund.
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/adapters/wormhole/WormholeAdapter.sol#L24
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/adapters/wormhole/WormholeAdapter.sol#L69-L77

##### Recommendation
We recommend using different refund addresses for different chains.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#8-the-refund-address-in-wormholeadapter-can-be-different-in-different-chains
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

