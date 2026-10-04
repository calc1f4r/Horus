---
# Core Classification
protocol: Hashflow Hashverse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60984
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/hashflow-hashverse/1af3e150-d612-4b24-bc74-185624a863f8/index.html
source_link: https://certificate.quantstamp.com/full/hashflow-hashverse/1af3e150-d612-4b24-bc74-185624a863f8/index.html
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Cameron Biniamow
  - Ibrahim Abouzied
  - Rabib Islam
  - Jeffrey Kam
---

## Vulnerability Title

Items Can Be Bridged to Inactive Chain

### Overview


The client has marked a bug as "Fixed" and added a check to address the issue. The bug affected two files, `RenovaItemBase.sol` and `WormholeBaseUpgradeable.sol`. The bug allowed users to bridge their items between chains, but if they chose a destination chain that did not have a `RenovaItemSatellite` contract, the item would be lost. The bug report recommends implementing a check to ensure that a valid destination chain is selected.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. The check was added. Addressed in: `74496b665998e7cb3b9cb7101756e78cc1569d1a`.

**File(s) affected:**`RenovaItemBase.sol`, `WormholeBaseUpgradeable.sol`

**Description:** Users can bridge their items between chains by calling `wormholeBridgeOut()` in `RenovaItem` and `RenovaItemSatellite`. The user chooses the destination Wormhole chain ID with `dstWormholeChainId`. If the user passes the chain ID for a chain that does not have a `RenovaItemSatellite` contract deployed, the item is essentially lost as the item is burnt on the source chain during the bridging. There are no relevant checks to ensure that the destination chain is configured for bridging Renova items.

**Recommendation:** Implement the check `_wormholeRemotes[dstWormholeChainId] != bytes(0)` to ensure a valid destination chain is selected.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Hashflow Hashverse |
| Report Date | N/A |
| Finders | Cameron Biniamow, Ibrahim Abouzied, Rabib Islam, Jeffrey Kam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/hashflow-hashverse/1af3e150-d612-4b24-bc74-185624a863f8/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/hashflow-hashverse/1af3e150-d612-4b24-bc74-185624a863f8/index.html

### Keywords for Search

`vulnerability`

