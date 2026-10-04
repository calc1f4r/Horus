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
solodit_id: 62775
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

Missing Check of `msg.value` in `bridgeOut()` Function Allows DoS or Stealing Funds

### Overview


This report discusses a bug found in the `CampTimelockEscrowNativeOFT.sol` file that affects the `bridgeOut()` function. The function is supposed to receive native tokens, but it does not verify the amount of tokens provided by the user against the actual supplied `msg.value`. This allows users to initiate a bridging operation with debt, potentially leading to the loss of tokens provided by other depositors. The bug can be exploited by whitelisted users, who can drain the contract immediately, and can also be used in combination with front-running to steal funds. The report recommends fixing the bug by checking against `msg.value` and ensuring that the original deposit transfer includes the required fees and tokens.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `95fad25a5770015dba8595595249a9fe8257b35e`.

**File(s) affected:**`CampTimelockEscrowNativeOFT.sol`

**Description:** The `bridgeOut()` function acts as the deposit entrypoint to the OFT bridge. It is supposed to receive native tokens, which are later bridged. The amount of tokens to be bridged is provided by the user with the `_originalAmount` parameter, however it is never verified against the actual supplied `msg.value`. This allows users to effectively initiate a bridging operation with debt, which then consumes tokens provided by other depositors.

This is particularly exploitable by whitelisted users, who can drain the contract immediately. Other users cannot affect already initiated deposits, and only misuse tokens from those initiated after the malicious one. This could be exploited in combination with frontrunning to steal funds while ensuring that sufficient funds are available for the validations in the `send()` function. Alternatively, creating a deposit with very high debt would effectively DoS the bridge as a whole, as this deposit cannot be skipped in the `batchRelease()` function.

**Exploit Scenario:**

1.   Alice makes a deposit of 10 tokens.
2.   Mallory can create a deposit with `_originalAmount` of 10, without transferring native tokens. If Mallory is whitelisted, this is executed immediately and will consume the 10 tokens supplied by Alice.
3.   Bob makes a deposit of 20 tokens. If mallory wasn't whitelisted, 10 of these tokens will be stolen by Mallory once the unlock period passes. If there are no other deposits, Bobs' bridging operation will fail due to insufficient contract balance. 
4.   Mallory creates a deposit with `_originalAmount` of 1e77. This can never be repayed, all future deposits are lost, no further bridging operation can occur.

**Recommendation:** Ensure that the original deposit transfer of native tokens includes the incurred fees (see [](https://certificate.quantstamp.com/full/camp/ae830654-5f2b-4d21-aba2-1de572092da6/index.html#findings-qs2)[CAMP-2](https://certificate.quantstamp.com/full/camp/ae830654-5f2b-4d21-aba2-1de572092da6/index.html#findings-qs2)) and the required native tokens by checking against `msg.value`.

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

