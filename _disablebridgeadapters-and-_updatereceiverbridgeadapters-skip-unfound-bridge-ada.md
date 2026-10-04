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
solodit_id: 34416
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#9-_disablebridgeadapters-and-_updatereceiverbridgeadapters-skip-unfound-bridge-adapters
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

`_disableBridgeAdapters()` and `_updateReceiverBridgeAdapters()` skip unfound bridge adapters

### Overview

See description below for full details.

### Original Finding Content

##### Description
Unfound bridge adapters are just skipped if they were not found during removal in `CrossChainForwarder._disableBridgeAdapters()` and `CrossChainReceiver._updateReceiverBridgeAdapters()`. It makes it more difficult to identify a mistake in the modification of the allowed bridge adapters set.
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/CrossChainForwarder.sol#L391
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/CrossChainReceiver.sol#L288


##### Recommendation
We recommend reverting in case of an unfound bridge adapter.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#9-_disablebridgeadapters-and-_updatereceiverbridgeadapters-skip-unfound-bridge-adapters
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

