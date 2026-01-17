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
solodit_id: 34414
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#7-the-missing-check-for-requiredconfirmation-when-updating-the-allowedbridgeadapters-set
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

The missing check for `requiredConfirmation` when updating the `allowedBridgeAdapters` set

### Overview

See description below for full details.

### Original Finding Content

##### Description
There is an issue in the function defined at line https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/CrossChainReceiver.sol#L288. This function is used to update the `allowedBridgeAdapters` set. It is possible that some adapters could be removed, resulting in an insufficient number of remaining adapters to confirm a received envelope.

##### Recommendation
We recommend adding a check that after removing adapters from the `allowedBridgeAdapters` set, there are still enough adapters for the particular chain to pass the `requiredConfirmation` check.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#7-the-missing-check-for-requiredconfirmation-when-updating-the-allowedbridgeadapters-set
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

