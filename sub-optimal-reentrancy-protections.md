---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19459
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Sub-Optimal Reentrancy Protections

### Overview

See description below for full details.

### Original Finding Content

## Description

The functions `createMotion()` and `enactMotion()` are sub-optimal with regards to resilience against reentrancy attacks. They have no check to prevent reentrancy (e.g., a `noReentrancy` modifier based on a storage flag) and do not properly apply the Checks-Effects-Interactions pattern. The external contracts accessed are relatively trustworthy (`EVMScriptExecutor`, and the factory) and no impactful exploits were identified. A clearly malicious factory is not part of a reasonable threat model, as these are approved by the DAO. However, it is more feasible to consider a scenario in which the DAO is tricked into accepting an obfuscated or vulnerable factory.

## Recommendations

- Restructure `createMotion()` and `enactMotion()` to better follow the checks-effects-interactions pattern.
  
- In `enactMotion()`, execute `_deleteMotion()` and emit `MotionEnacted()` before making any external contract calls.
  
- In `createMotion()`, increment `lastMotionId` and save as much of the `Motion` struct to storage as possible before executing `_createEVMScript()` (it should be possible to store all but `evmScriptHash` prior).

- Alternatively, these functions could be protected via a `noReentrancy` modifier, but this is likely not worth the additional storage costs.

## Resolution

This has been fixed in PR #8.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf

### Keywords for Search

`vulnerability`

