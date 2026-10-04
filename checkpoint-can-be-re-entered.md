---
# Core Classification
protocol: Hyperdrive February 2024
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35826
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-February-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-February-2024.pdf
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
  - Saw-Mon and Natalie
  - Christoph Michel
  - Deivitto
  - M4rio.eth
---

## Vulnerability Title

checkpoint can be re-entered

### Overview


This bug report is about a medium risk issue in the Hyperdrive smart contract. The checkpoint function does not have a reentrancy guard, which means it can change important contract state and interfere with other functions that don't expect this to happen. This can lead to incorrect calculations and potentially violate solvency requirements. The recommendation is to make all calls to a specific function atomic and to add a reentrancy guard to the checkpoint function. The issue has been fixed and verified in a pull request.

### Original Finding Content

## Security Vulnerability Report

## Severity
**Medium Risk**

## Context
- **Files**: 
  - `HyperdriveCheckpoint.sol#L32`
  - `HyperdriveShort.sol#L98`

## Description
Most public functions of Hyperdrive have reentrancy guards, but the `checkpoint` function does not. This oversight can lead to changes in important contract states, such as reserves, which may interfere with other functions that do not expect these states to change during a `_deposit` call.

For example, the following call sequence:
- `StEthHyperdrive.openShort`
  - `_openShort`
    - `_deposit`

This series of calls performs a refund that occurs in the middle of the `openShort` function, continuing execution with the `_applyShort` function afterward. An attacker could potentially re-enter `checkpoint` during `_deposit` to apply a checkpoint, thereby altering the market state. This could result in the calculation of a swap that violates solvency requirements since solvency is only checked after the `_deposit`.

Furthermore, once the market state is updated in `_applyCheckpoint`, there may be some excess idle that needs distribution. If so, the curve `C` will be scaled down to a new value. However, when `_applyOpenShort` is called, the inputs are derived from deltas calculated when trading on `C`, not the new value, which could potentially push our point `(z, , y)` further to the right. While it might not result in exceeding the solvency or minimum lines, it could exceed the acceptable amount.

## Recommendation
All calls to `_calculateOpenShort` and `_applyOpenShort` should be atomic, ensuring that the curve `C` does not change in between these calls. Additionally, consider adding reentrancy guards to the `checkpoint` function.

## Additional Information
**DELV**: Fixed in PR 765.  
**Spearbit**: Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Hyperdrive February 2024 |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Christoph Michel, Deivitto, M4rio.eth |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-February-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-February-2024.pdf

### Keywords for Search

`vulnerability`

