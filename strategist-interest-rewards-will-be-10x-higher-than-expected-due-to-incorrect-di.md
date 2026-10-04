---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7302
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - wrong_math

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

Strategist Interest Rewards will be 10x higher than expected due to incorrect divisor

### Overview


This bug report is about an issue in the PublicVault.sol code. It states that the VAULT_FEE set as an immutable argument in the construction of new vaults is intended to be set in basis points, but when the strategist interest rewards are calculated in _handleStrategistInterestReward() the VAULT_FEE is only divided by 1000. This means that the fee calculated by the function will be 10x higher than expected, and the strategist will be dramatically overpaid. 

The recommendation made is to change the code from: 

uint256 fee = x.mulDivDown(VAULT_FEE(), 1000); 

to: 

uint256 fee = x.mulDivDown(VAULT_FEE(), 10000); 

and also to add the following line:

s.strategistUnclaimedShares += convertToShares(fee).safeCastTo88();

The bug has been resolved based on the PR 203, and verified by Spearbit.

### Original Finding Content

## High Risk Report

**Severity:** High Risk  
**Context:** PublicVault.sol#L564  
**Description:**  
`VAULT_FEE` is set as an immutable argument in the construction of new vaults and is intended to be set in basis points. However, when the strategist interest rewards are calculated in `_handleStrategistInterestReward()`, the `VAULT_FEE` is only divided by 1000. The result is that the fee calculated by the function will be 10x higher than expected, and the strategist will be dramatically overpaid.

**Recommendation:**  
```solidity
unchecked {
- uint256 fee = x.mulDivDown(VAULT_FEE(), 1000);
+ uint256 fee = x.mulDivDown(VAULT_FEE(), 10000);
s.strategistUnclaimedShares += convertToShares(fee).safeCastTo88();
}
```

**Astaria:** Resolved based on the following PR 203.  
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Wrong Math`

