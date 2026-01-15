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
solodit_id: 60386
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

Missing Re-entrant Modifier [To be checked by the team]

### Overview


The client has reported a bug where certain functions in the code are missing a necessary security measure called a "non-reentrant modifier". This means that the functions can be called multiple times at once, potentially causing unexpected behavior or security vulnerabilities. The client has suggested adding these modifiers and making a small change to one of the functions to fix the issue. The bug has been marked as fixed by the client. 

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `df23927a8888bc70d3f6431ff4efc34f135e48da`, `95dea2abdd7cf637d5a3335c21bdeac8ec75b832`. The client provided the following explanation:

> Commit `df239` added `nonReentrantGuard` for `acceptBidSellNftToMarketPull` and `acceptBidSellNftToMarketPush`. Commit `95dea` added `nonReentrantGuard` for `onERC721Received` data branches. We acknowledge that the onERC721Received guard has a redundant check on `isEntered` -- it's a gas compromise we made to minimize change needed for OZ's `nonReentrantGaurd`.

**Description:** The following functions are missing non-reentrant modifiers:

*   `acceptBidSellNftToMarketPull()`
*   `acceptBidSellNftToMarketPush()`
*   `onERC721Received()`

It is unclear why the project team committed to using a re-entrancy guard on those functions.

**Recommendation:** Add the necessary modifiers, and in the case of `onERC721Received` change the state to entered when necessary and back to the original state once all state is updated and external calls are executed.

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

