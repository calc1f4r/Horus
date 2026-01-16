---
# Core Classification
protocol: Pheasant Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60334
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
source_link: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Danny Aksenov
  - Faycal Lalidji
  - Ruben Koch
  - Valerian Callens
  - Guillermo Escobero
---

## Vulnerability Title

Relayer Can Set Arbitrary Supported Tokens for Upward Trades on L2

### Overview


This bug report is about a problem in the code for a specific file called `PheasantNetworkBridgeChild.sol`. The issue occurs when a certain function, `acceptUpwardTrade()`, is used by a relayer. The function includes an extra parameter called `_tokenTypeIndex` that needs to be checked to make sure it matches the network id. This will prevent any malicious activity and ensure that the trade is valid. The bug has been fixed in the code and the fix can be found in the specific code version mentioned in the report.

### Original Finding Content

**Update**
Addressed in: `f0ce3b728e76ae15ac71c5809a28f2a283a54596`.

**File(s) affected:**`PheasantNetworkBridgeChild.sol`

**Description:** When a relayer executes `PheasantNetworkBridgeChild.acceptUpwardTrade()`, it supplies the `_tokenTypeIndex` as an additional parameter next to the evidence struct. Note that this trade will not be subject to slashing as a result of such a malicious relay, as all rules have been followed, and the target network is still the correct one.

**Recommendation:** Validate if the `_tokenTypeIndex` and the network id are matching the values provided through the evidence structure.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Pheasant Network |
| Report Date | N/A |
| Finders | Danny Aksenov, Faycal Lalidji, Ruben Koch, Valerian Callens, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html

### Keywords for Search

`vulnerability`

