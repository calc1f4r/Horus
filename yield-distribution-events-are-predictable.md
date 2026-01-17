---
# Core Classification
protocol: Sperax - USDs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59840
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html
source_link: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Shih-Hung Wang
  - Pavel Shabarkin
  - Ibrahim Abouzied
---

## Vulnerability Title

Yield Distribution Events Are Predictable

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> The official documentation has not been updated with the new mechanism yet. Previously, we manually performed rebases every 7-12 days to maintain randomness. However, with the upgraded version, anyone can initiate a rebase as long as certain conditions are met. These conditions include a calculated APR for the rebase greater than aprBottom and a time gap between consecutive rebases greater than the configured gap in the RebaseManager. Rebasing involves multiple steps (harvest, buyback) and is semi-automated within the mint and redeem process, accessible to anyone. This makes it difficult to predict and take advantage of. The rebase amount will be relatively small but more frequent, reducing the incentive for front-running. We will closely monitor and adjust parameters over time.

**File(s) affected:**`vault/VaultCore.sol`, `rebase/RebaseManager.sol`

**Description:** According to the official documentation:

> Yield is distributed approximately every 7 days. The exact distribution time is determined in a quasi-random way. We have decided on this randomised distribution time to prevent users from timing their USDs minting and redeeming with yield distribution events. Huge spike in minting or redeeming around the time of yield distribution can put strain on the peg and this randomisation works as a defence mechanism for maintaining peg

However, according to the code implementation, the yield distribution events, i.e., rebasing events, can be triggered by anyone by calling the`VaultCore.rebase()`function. As long as the cooldown period has passed and sufficient funds are in the vault or can be collected from`Dripper`, the`rebase()`call will take effect. Therefore, the rebasing events are considered easily predictable and can be executed by users.

**Recommendation:** Consider clarifying the intention of such a randomization defense mechanism and ensure it matches the code implementation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Sperax - USDs |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Pavel Shabarkin, Ibrahim Abouzied |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html

### Keywords for Search

`vulnerability`

