---
# Core Classification
protocol: Aera Contracts v3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58295
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review-April-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review-April-2025.pdf
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
finders_count: 3
finders:
  - Slowfi
  - Eric Wang
  - High Byte
---

## Vulnerability Title

CCTP hook blocks subsequent token bridging after the first one

### Overview


This bug report discusses an issue with the CCTP hook in the CCTPHooks.sol file. The hook is currently only a before-hook and not an after-hook, which means that the `depositForBurn()` function will only be called once before the operation. This causes a problem when trying to bridge USDC to multiple recipients in a submission, as the second call to `depositForBurn()` will fail. The recommendation is to either remove the `if (HooksLibrary.hasBeforeHookBeenCalled())` statement or configure the CCTP hook as both a before- and after-hook to reset the slot to 0 after the operation. The bug has been fixed in PR 303 and verified by Spearbit.

### Original Finding Content

## Risk Assessment Report

## Severity
**Medium Risk**

## Context
`CCTPHooks.sol#L17-L27`

## Description
Based on the tests, the CCTP hook is a before-hook but not an after-hook, which means that the `depositForBurn()` function will only be called once before the operation. Therefore, the `HAS_BEFORE_BEEN_CALLED_SLOT` remains 1 after the operation (i.e., not reset to 0).

Consider a case where the guardian wants to bridge USDC to multiple recipients in a submission. The second call
to `depositForBurn()` will fail since the hook considers that it is in a post-op state and returns empty bytes, which causes the Merkle proof verification to fail.

## Recommendation
Consider either removing the `if (HooksLibrary.hasBeforeHookBeenCalled())` statement if the CCTP hook is a before-hook but not an after-hook. Otherwise, configure the CCTP hook as both a before- and after-hook so the slot can be reset to 0 after the operation. Generally speaking, if a hook uses the `hasBeforeHookBeenCalled()` function, it should be both a before- and after-hook.

## Aera
Fixed in PR 303.

## Spearbit
Verified. The CCTP hook is now only a before-hook, but not an after-hook.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Aera Contracts v3 |
| Report Date | N/A |
| Finders | Slowfi, Eric Wang, High Byte |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review-April-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review-April-2025.pdf

### Keywords for Search

`vulnerability`

