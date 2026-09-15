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
solodit_id: 58293
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

Fees accrued by the old fee calculator may be lost when setting a new one

### Overview


This bug report discusses an issue with the FeeVault smart contract. When the owner of the vault sets a new fee calculator, any unclaimed fees on the old calculator will be lost. To prevent this, the report suggests calling the `claimFees()` function on the old calculator before setting a new one. However, there is a possibility that this function may constantly fail, so the report offers two potential solutions. The first solution involves allowing anyone to call `claimFees()`, but the fees will be transferred to the correct recipients instead of the caller. The second solution suggests using a low-level call to `claimFees()` and only transferring the fees if the call is successful. The report also mentions that the bug has been acknowledged, but it will not be fixed due to the complexity and the current trust model in place. 

### Original Finding Content

## Severity: Medium Risk

**Context:** FeeVault.sol#L81

**Description:** 
When the vault owner sets a new fee calculator, there may be finalized but unclaimed fees on the old one. If so, those fees will be lost. Before changing the fee calculator, `claimFees()` should be called on the old one to retrieve the latest fee amounts, and the vault should transfer the fees to the recipients.

**Recommendation:** 
Considering that it would be an issue if the `claimFees()` function on the old fee calculator constantly reverts, there can be two possible mitigations:
1. Allow anyone to call `claimFees()`, but the fees will be transferred to the correct recipients instead of `msg.sender`. On the UI side, make the vault owner call `claimFees()` before `setFeeCalculator()`, but skip `claimFees()` if it will revert.
2. Call `feeCalculator.claimFees()` with a low-level call. Proceed with transferring the fees to the recipients only if the call has succeeded.

**Aera:** Acknowledged. Won't fix due to the complexity and because the trust model already necessitates that fee recipients claim regularly.

**Spearbit:** Acknowledged.

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

