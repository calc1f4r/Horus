---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7297
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
  - don't_update_state

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

stateHash isn't updated by buyoutLien function

### Overview


This bug report is about a high risk issue in the LienToken.sol file, between lines 102 and 187. The issue is that the collateral state hash is not updated in the buyoutLien function. This means that after all checks are passed, the payment will be transferred from the buyer to the seller, but the seller will still own the lien in the system's state. 

The recommendation is to save the return value of the _replaceStackAtPositionWithNewLien function call and use it to call the keccak256(abi.encode(newUpdatedStack)). This will update the collateral state hash. This issue has been confirmed and fixed with the following commit.

### Original Finding Content

## Security Issue Report

## Severity
**High Risk**

## Context
LienToken.sol#L102-187

## Description
We never update the collateral state hash anywhere in the `buyoutLien` function. As a result, once all checks are passed, payment will be transferred from the buyer to the seller, but the seller will retain ownership of the lien in the system's state.

## Recommendation
We should save the return value of the `_replaceStackAtPositionWithNewLien` function call and use it to call:
```solidity
s.collateralStateHash[collateralId] = keccak256(abi.encode(newUpdatedStack));
```

## Spearbit
Confirmed, the following commit fixes this issue.

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

`Don't update state`

