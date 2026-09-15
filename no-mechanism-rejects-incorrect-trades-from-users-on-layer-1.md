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
solodit_id: 60338
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
source_link: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
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
  - Danny Aksenov
  - Faycal Lalidji
  - Ruben Koch
  - Valerian Callens
  - Guillermo Escobero
---

## Vulnerability Title

No Mechanism Rejects Incorrect Trades From Users on Layer 1

### Overview


The report is about a bug in the Pheasant Network Bridge Child contract. This bug affects the system's ability to handle upward trades. The client has suggested addressing the issue by documenting it in the system's documentation to reduce gas costs. The bug occurs when the system receives a transfer from the relayer, and it is considered invalid if the networkId cannot be extracted or if the transferred amount is too low or too high. The recommendation is to add a mechanism on Layer 1, such as a smart contract, to reject any trades that would be considered invalid on Layer 2.

### Original Finding Content

**Update**
The client provided the following explanation:

> We understood this feedback. However we are currently implementing a mechanism and have decided to address the issue by documenting it in the docs to reduce gas costs. In the "Technical Details / Token Transfer" section of the documentation, we have clarified that when sending tokens to the relayer, it is important to send an amount within the relayer's supported range and restrict it to the networkCode(s) that the relayer supports. https://docs.pheasant.network/contracts/technical-details#token-transfer

**File(s) affected:**`PheasantNetworkBridgeChild.sol`

**Description:** The system expects as the first step for upward trades a transfer to the EOA of the Relayer. However, even if that trade cannot be rejected, it is considered invalid under several conditions:

*   if we cannot extract a valid `networkId` from the transferred amount;
*   if the transferred amount is too low or too big.

**Recommendation:** Consider adding a mechanism on Layer 1, like a smart contract, to reject any trade that would be considered invalid on Layer 2.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

