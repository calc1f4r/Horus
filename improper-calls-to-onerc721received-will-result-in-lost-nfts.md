---
# Core Classification
protocol: Particle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60384
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/particle/3cd57a7b-681f-4f38-b0cd-9fd6f2f37a89/index.html
source_link: https://certificate.quantstamp.com/full/particle/3cd57a7b-681f-4f38-b0cd-9fd6f2f37a89/index.html
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
  - Michael Boyle
  - Zeeshan Meghji
  - Faycal Lalidji
  - Gelei Deng
---

## Vulnerability Title

Improper Calls to `onERC721Received()` Will Result in Lost Nfts

### Overview


This bug report is about a problem with the `onERC721Received()` function in the `ParticleExchange.sol` file. This function allows users to take actions on a protocol without having to approve an NFT transfer. However, there is a bug where if the `data` parameter has an incorrect length, the NFT will be lost and cannot be retrieved. The client has marked this as "Fixed" and provided a code fix to address the issue. The recommendation is to revert the call to `onERC721Received()` if the `data.length` does not meet certain conditions.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `7ef86ce5f4a487cbeecbfab93c079186023f0ea2`. The client provided the following explanation:

> If data length is incorrect, throw `InvalidParameter` error, so the supplied NFT won't be lost.

**File(s) affected:**`ParticleExchange.sol`

**Description:** The `onERC721Received()` function allows users to take various actions on the protocol without the additional step of approving an NFT transfer. The action taken depends on the contents of the `data` parameter. However, for some values of invalid values of `data` no protocol action will be taken on the NFT, and it will simply be swallowed up by the contract and locked forever. This would happen for values of data such that: `data.length != 64 && data.length != 288 data.length < 384`.

**Recommendation:** If the `data.length` doesn't correspond to any of the conditions in the if statements, revert the call to `onERC721Received()`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Particle |
| Report Date | N/A |
| Finders | Michael Boyle, Zeeshan Meghji, Faycal Lalidji, Gelei Deng |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/particle/3cd57a7b-681f-4f38-b0cd-9fd6f2f37a89/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/particle/3cd57a7b-681f-4f38-b0cd-9fd6f2f37a89/index.html

### Keywords for Search

`vulnerability`

