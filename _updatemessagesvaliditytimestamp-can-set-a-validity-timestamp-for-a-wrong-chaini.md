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
solodit_id: 34417
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#10-_updatemessagesvaliditytimestamp-can-set-a-validity-timestamp-for-a-wrong-chainid
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

`_updateMessagesValidityTimestamp()` can set a validity timestamp for a wrong `chainId`

### Overview

See description below for full details.

### Original Finding Content

##### Description
There are no checks in `CrossChainReceiver._updateMessagesValidityTimestamp()` that a chain id is supported by the receiver. So, a validity timestamp can be set for any chain id. It makes more difficult to identify a mistake during the call of `CrossChainReceiver.updateMessagesValidityTimestamp()`.
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/CrossChainReceiver.sol#L246

##### Recommendation
We recommend adding a check to `CrossChainReceiver._updateMessagesValidityTimestamp()` that the `chainId` is in `_supportedChains`.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#10-_updatemessagesvaliditytimestamp-can-set-a-validity-timestamp-for-a-wrong-chainid
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

