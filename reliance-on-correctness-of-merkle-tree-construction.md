---
# Core Classification
protocol: API3Market
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59662
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/api-3-market/30c52dab-387e-4643-9059-df5de1a4c6a7/index.html
source_link: https://certificate.quantstamp.com/full/api-3-market/30c52dab-387e-4643-9059-df5de1a4c6a7/index.html
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
finders_count: 3
finders:
  - Michael Boyle
  - Adrian Koegl
  - Jonathan Mevs
---

## Vulnerability Title

Reliance on Correctness of Merkle Tree Construction

### Overview


This bug report discusses potential issues with the off-chain construction of Merkle trees in the client's smart contracts. The client has acknowledged the issue and provided an explanation stating that the added complexity is not worth it. However, the report recommends finding a solution, such as passing a zk proof, to ensure the correctness of the Merkle trees on-chain. The report also outlines three constraints that are not currently enforced on-chain, which could lead to security issues and inconsistencies. These include not allowing a specific dAPI name to be used more than once, not allowing a dAPI name to be re-pointed to a different data feed during an active subscription, and ensuring all entries of the same dAPI name point to the same sponsor wallet. 

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Considering that these checks can be offloaded to the respective hash signers, we do not find the added complexity to be worthwhile. As a note, we do not agree with the statement “A dAPI name in the management Merkle tree should not be re-pointed to a different data feed during an active subscription. This might violate the purchasing conditions of the subscriber.” A dAPI is understood to be a managed service, and API3 maintaining the configuration of the dAPI over the lifetime of the subscription to uphold the expectations of the user as described by the dAPI name (e.g., “ETH/USD”) and update parameters is an important aspect of the service. For example, in the case that an API provider discontinues service, the dAPI name would be re-pointed to a Beacon set that replaces said API provider, and the contracts are designed to be able to handle this.

**Description:** The smart contracts in scope rely on the correct off-chain construction of Merkle trees. The following constraints are not enforced on-chain upon Merkle root submission and, if ever accidentally or intentionally violated, could lead to security issues and/or inconsistencies:

1.   The Management Merkle Tree cannot contain a specific dAPI name more than once. Otherwise, anyone can change the pointer of the dAPI name to the data feed ID.
2.   A dAPI name in the management Merkle tree should not be re-pointed to a different data feed during an active subscription. This might violate the purchasing conditions of the subscriber.
3.   All entries of the same dAPI name in the management Merkle tree must point to the same sponsor wallet.

**Recommendation:** The correctness of merkle trees is hard to verify on-chain. A potential solution would be to pass a zk proof, such that a smart contract can verify that some constraints hold for the submitted merkle root.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | API3Market |
| Report Date | N/A |
| Finders | Michael Boyle, Adrian Koegl, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/api-3-market/30c52dab-387e-4643-9059-df5de1a4c6a7/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/api-3-market/30c52dab-387e-4643-9059-df5de1a4c6a7/index.html

### Keywords for Search

`vulnerability`

