---
# Core Classification
protocol: Stader Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53699
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
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

Price Inﬂation Of cTokenShare When Supply Is Zero

### Overview


This bug report describes a potential issue with the delegation process in a token called SD. If the token supply is zero and an attacker performs a share inflation attack, it can result in a loss of tokens for the user. The report suggests implementing a solution called decimal offset virtual shares and assets to prevent this type of attack. The team has resolved the issue by adding an initial delegate of 1 SD during initialization.

### Original Finding Content

## Description

If the current supply is zero, an attacker can perform a share inflation attack during delegation. This can be illustrated through the following steps:

1. Alice wants to delegate 1 SD token (which has 18 decimals) to the utility pool calling `delegate()`.
2. The pool is empty. The exchange rate is the default 1 SD per cTokenShare.
3. Bob sees Alice’s transaction in the mempool and decides to sandwich it.
4. Bob delegates 1 wei of SD and receives 1 wei of cTokenShare in exchange. The exchange rate is now 1 SD per cTokenShare.
5. Bob transfers 1 SD (1e18 wei) to the vault using an ERC-20 transfer. No new cTokenShares are created. Hence, the exchange rate is now `1e18 + 1 SD` per cTokenShare, or `1e18 + 1 wei` of SD per wei of cTokenShare.
6. Alice’s deposit is executed. Her 1e18 wei of SD tokens are worth less than 1 wei of cTokenShare. Therefore, the contract takes the assets, but does not add shares. Alice has effectively "donated" her tokens.

## Recommendations

Consider implementing a decimal offset virtual shares and assets to the pool.  
See the following for more details: [Addressing Inflation Attacks With Virtual Shares And Assets](link-to-details)

## Resolution

The Stader Team has elected to resolve this issue using an initial delegate of 1 SD during the initialization. This issue has been addressed in commit `21ba418`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Stader Labs |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf

### Keywords for Search

`vulnerability`

