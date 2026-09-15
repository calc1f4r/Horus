---
# Core Classification
protocol: Camp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62776
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/camp/ae830654-5f2b-4d21-aba2-1de572092da6/index.html
source_link: https://certificate.quantstamp.com/full/camp/ae830654-5f2b-4d21-aba2-1de572092da6/index.html
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
finders_count: 3
finders:
  - Paul Clemson
  - Gereon Mendler
  - Andy Lin
---

## Vulnerability Title

User Deposit May Not Cover Bridging Fees

### Overview


This bug report states that a client has marked a bug as "Fixed" and has made additional improvements to the contract accounting. The specific file affected is `CampTimelockEscrowNativeOFT.sol`. The issue is that the `send()` operation incurs additional fees that are not taken into account during the initial deposit using the `bridgeOut()` function. This can lead to the contract running out of funds while still having unprocessed deposits. The recommendation is to ensure that the original deposit transfer includes the incurred fees and required native tokens by checking against `msg.value`.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `95fad25a5770015dba8595595249a9fe8257b35e`.

Additional fixes were made to improve overall contract accounting. Final related commit: `3f19c068cfdc88d63caac061aacaa41585d1a516`

**File(s) affected:**`CampTimelockEscrowNativeOFT.sol`

**Description:** The `send()` operation incurs additional fees exceeding the `_originalAmount` recorded during the initial deposit using the `bridgeOut()` function. This total value is calculated in the `_bridgeNativeTokens()` functions, and then paid from the contract balance. However, there is no validation that this fee is paid during the initial deposit. In its current form, the contract may run out of funds while still having unprocessed queued deposits.

**Recommendation:** Ensure that the original deposit transfer of native tokens includes the incurred fees and the required native tokens (see [](https://certificate.quantstamp.com/full/camp/ae830654-5f2b-4d21-aba2-1de572092da6/index.html#findings-qs1)[CAMP-1](https://certificate.quantstamp.com/full/camp/ae830654-5f2b-4d21-aba2-1de572092da6/index.html#findings-qs1)) by checking against `msg.value`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Camp |
| Report Date | N/A |
| Finders | Paul Clemson, Gereon Mendler, Andy Lin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/camp/ae830654-5f2b-4d21-aba2-1de572092da6/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/camp/ae830654-5f2b-4d21-aba2-1de572092da6/index.html

### Keywords for Search

`vulnerability`

