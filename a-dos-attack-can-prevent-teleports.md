---
# Core Classification
protocol: $BOBA Teleportation and Token as a Fee
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60676
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/boba-teleportation-and-token-as-a-fee/72fc60f1-efe4-4f86-8a3f-6ada60d11005/index.html
source_link: https://certificate.quantstamp.com/full/boba-teleportation-and-token-as-a-fee/72fc60f1-efe4-4f86-8a3f-6ada60d11005/index.html
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
finders_count: 5
finders:
  - Pavel Shabarkin
  - Ibrahim Abouzied
  - Andy Lin
  - Adrian Koegl
  - Valerian Callens
---

## Vulnerability Title

A DOS Attack Can Prevent Teleports

### Overview


A client has reported a bug in the `Teleportation` contract, which allows attackers to exhaust the daily transfer limit without paying a fee. This can prevent other users from using the contract for 24 hours. The client suggests adding a fee to prevent this type of attack.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation: Since this is only one way to move Boba tokens around to another chain we are avoiding adding a fee for now. There exists the native way of using the LayerZero bridges to bridge tokens onto the other chain.

**File(s) affected:**`Teleportation.sol`

**Description:** Since the `Teleportation` contract does not charge a fee, attackers can exhaust the `maxTransferAmountPerDay` by calling `teleportBOBA()` or `teleportNativeBOBA()` functions to teleport the full value. The attack would be relatively cheap, only costing L2 gas. Once the daily limit is reached, other users can no longer bridge.

Any user owning at least `maxTransferAmountPerDay` BOBA may be incentivized to block the teleportations in the right situation, such as a governance decision impacting them is up for a vote. To do so, they could teleport enough BOBA through the different chains to reach the `maxTransferAmountPerDay` threshold on each supported chain, thereby blocking teleportations for the next 24 hours.

**Recommendation:** Consider charging a teleportation fee to mitigate DOS attacks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | $BOBA Teleportation and Token as a Fee |
| Report Date | N/A |
| Finders | Pavel Shabarkin, Ibrahim Abouzied, Andy Lin, Adrian Koegl, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/boba-teleportation-and-token-as-a-fee/72fc60f1-efe4-4f86-8a3f-6ada60d11005/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/boba-teleportation-and-token-as-a-fee/72fc60f1-efe4-4f86-8a3f-6ada60d11005/index.html

### Keywords for Search

`vulnerability`

