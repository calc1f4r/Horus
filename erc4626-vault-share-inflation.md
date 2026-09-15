---
# Core Classification
protocol: Treehouse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38555
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/treehouse/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/treehouse/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

ERC4626 Vault Share Inflation

### Overview


The bug report describes a potential issue where a malicious user could steal assets from another user by taking advantage of a profit accounting update in the system. This is due to a vulnerability in the Treehouse protocol, specifically in the TreehouseRouter.deposit() function. The likelihood of this issue occurring is low, but the report recommends implementing protection measures such as using an offchain solution like Flashbots and fine-tuning constants used in the protocol. The issue has been addressed in a recent commit.

### Original Finding Content

## Description

A malicious user may frontrun an accounting update when the protocol is empty to steal assets from another user. The share inflation attack, common to ERC4626 implementations, is possible when the system posts a profit after having had a user deposit. The malicious user notices the profit accounting and frontruns the accounting transaction with a `redeem()` request of `original deposit - 1size`. 

Next, when another user deposits, if their deposit is half or less than the profit posted, they will lose their deposit as they are allocated no shares. Given the need for the system to post a profit after one user depositing with no other current users of the system, the likelihood of this issue occurring has been rated as low.

## Recommendations

Protection against users frontrunning accounting updates, such as using an offchain solution like Flashbots to avoid transactions being seen in the mempool, would prevent this issue from occurring.

The Treehouse team should also fine-tune the constants used in ERC4626, such as `_decimalOffset()`, to make this attack less profitable and even more unlikely to occur. A small sacrificial deposit could be placed with the creation of the protocol to enforce the ratio of assets to shares, as seen in discussion here.

## Resolution

`TreehouseRouter.deposit()` will revert when no shares are minted. This issue has been addressed in commit `d34c3b3`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Treehouse |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/treehouse/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/treehouse/review.pdf

### Keywords for Search

`vulnerability`

