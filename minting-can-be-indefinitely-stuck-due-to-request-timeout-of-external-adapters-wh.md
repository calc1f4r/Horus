---
# Core Classification
protocol: Mode Earnm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29272
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
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
finders_count: 2
finders:
  - Dacian
  - 0kage
---

## Vulnerability Title

Minting can be indefinitely stuck due to request timeout of external adapters when using Chainlink Any API

### Overview


Mode has identified a bug in its system that interacts with external adapters to verify user codes and wallet addresses. If the initial GET request times out, pending requests remain and users are unable to submit another minting request, resulting in them losing their codes and not receiving their mystery box rewards. Mode has acknowledged the issue and is considering implementing a function that code recipients can invoke in the event of a request timeout. This function would call `ChainlinkClient:cancelChainlinkRequest` and include a callback to the `MysteryBox` contract to initiate a new request with the same data as the original. This would allow users to resubmit their requests and receive their rewards.

### Original Finding Content

**Description:** Mode has integrated Chainlink Any API to interact with external adapters, verifying user codes and wallet addresses to determine the number of boxes to mint. The system uses a `direct-request` job type, triggering actions based on the `ChainlinkRequested` event emission. However, there's a notable issue: if the initial GET request times out, such requests may remain pending indefinitely. Current design does not have a provision to cancel pending requests and create new ones.

**Impact:** If the external adapter doesn't respond promptly, users are unable to submit another minting request because their code is deleted after the initial request. This could result in users losing their codes and not receiving their mystery box rewards.

**Recommended Mitigation:** Consider implementing a function that code recipients can invoke in the event of a request timeout. This function should internally call `ChainlinkClient:cancelChainlinkRequest` and include a callback to the `MysteryBox` contract to initiate a new request using the same data as the original. Essentially, this means reusing the code/user address and the previously generated random number for the new request.

**Mode:**
Acknowledged.


\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Mode Earnm |
| Report Date | N/A |
| Finders | Dacian, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

