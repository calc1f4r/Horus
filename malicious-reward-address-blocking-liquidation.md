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
solodit_id: 53696
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Malicious Reward Address Blocking Liquidation

### Overview


The report describes a bug in a function called `OperatorRewardsCollector._claim()`, which is responsible for transferring ETH to an operator reward address during the liquidation process. The bug allows an operator to set a malicious reward address that causes the transaction to fail, preventing the liquidation from being completed. The recommended solution is to convert the ETH balance to WETH to prevent this issue. The bug has been resolved in a commit called `21ba418` and a new function called `claimLiquidation()` has been added to address the issue.

### Original Finding Content

## Description

In `OperatorRewardsCollector._claim()`, the function responsible for finalizing liquidations and transferring ETH to the operator reward address is vulnerable to Denial-of-Service (DoS) attacks. An operator can set a malicious reward address that causes the transaction to revert, effectively preventing the liquidation process.

The process can be outlined as such:

1. **Initial Setup:** Alice delegates a specified amount of SD as collateral.
2. **Validator Preparation:** Bob adds a new validator using SD from `SDUtilityPool`.
3. **Fees Accrual:** Accrue fees for several blocks so that Bob’s health factor becomes unhealthy.
4. **Bob’s Liquidation:** Alice liquidates Bob’s position by calling `liquidationCall()`.
5. **Operator Reward Address Change:** Bob maliciously changes his reward address to a contract designed to revert transactions when receiving ETH.
6. **Finalize Liquidation:** Alice calls `claimFor()` on Bob to complete the liquidation. The amount specified when calling `claimFor()` will be non-zero (since zero represents Bob’s full balance).
7. **Transaction Failure:** Since the amount is non-zero, in the function `_claim()`, there will be an attempt to transfer the amount to the malicious reward address, which will revert, preventing the completion of the liquidation process.

## Recommendations

Convert the ETH balance to WETH, similar to how the liquidator is paid, to prevent a malicious reward address from blocking the liquidation process.

## Resolution

A new function `claimLiquidation()` was added for the liquidator to claim their portion separately. This issue has been addressed in commit `21ba418`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

