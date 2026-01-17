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
solodit_id: 34412
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#5-unrestricted-forwardmessage-and-setuppayments
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

Unrestricted `forwardMessage` and `setupPayments`

### Overview

See description below for full details.

### Original Finding Content

##### Description
The `forwardMessage` and `setupPayments` functions in all adapters can be called by anyone:
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/adapters/ccip/CCIPAdapter.sol#L67-L72
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/adapters/ccip/CCIPAdapter.sol#L122-L124
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/adapters/hyperLane/HyperLaneAdapter.sol#L46-L51
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/adapters/layerZero/LayerZeroAdapter.sol#L75-L80
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/adapters/wormhole/WormholeAdapter.sol#L54-L59
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/adapters/polygon/PolygonAdapterBase.sol#L42-L47

##### Recommendation
We recommend adding a check that these functions can be called only from the controller via `delegatecall`.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#5-unrestricted-forwardmessage-and-setuppayments
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

