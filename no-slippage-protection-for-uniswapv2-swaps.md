---
# Core Classification
protocol: Fastlane Atlas
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36788
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
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
  - Riley Holterhus
  - Blockdev
  - Gerard Persoon
---

## Vulnerability Title

No slippage protection for UniswapV2 swaps

### Overview


This bug report discusses a high-risk issue in the V2DAppControl.sol code, specifically lines 96-109. The problem is that the amount0In and amount1In values are affected by the current token balance of the UniswapV2 pool and the amount-out values. This allows for a potential attack where someone can manipulate the pool's balance and profit from the transaction. The recommendation is to add slippage protection to the swap or at least acknowledge the lack of it. The issue has been solved in a pull request and verified by Spearbit. 

### Original Finding Content

## Security Report

## Severity: High Risk

### Context
V2DAppControl.sol#L96-L109

### Description
The `amount0In` and `amount1In` values are dependent on the UniswapV2 pool's current token balance and on amount-out values. Someone can sandwich an Atlas transaction to imbalance the pool, leading to a high amount-in value which is then transferred from the user to the pool. 

The attacker makes a profit through this sandwich, and thus it's likely that all the token balance of the user is transferred to the pool.

### Recommendation
Add slippage protection to the swap, or at least make a comment about the lack of slippage protection.

### Fastlane
Solved in PR 360 by making a comment.

### Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Fastlane Atlas |
| Report Date | N/A |
| Finders | Riley Holterhus, Blockdev, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf

### Keywords for Search

`vulnerability`

