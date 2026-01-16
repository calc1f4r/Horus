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
solodit_id: 58296
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

Adding new oracles does not require a delay period

### Overview


The bug report discusses a medium risk issue in the file OracleRegistry.sol. The problem is that when a new oracle is added through the `addOracle()` function, it becomes effective immediately without any delay period. This could potentially lead to a compromised protocol if a malicious oracle is added. The report recommends introducing a delay period for vault owners to review the oracle before it becomes effective. This could be achieved by removing a certain check in the `scheduleOracleUpdate()` function. The report also mentions that this change may make it difficult to create new strategies quickly, but the issue has been fixed in PR 302. The report has been verified by Spearbit.

### Original Finding Content

## Risk Assessment

## Severity 
**Medium Risk**

## Context 
**File:** OracleRegistry.sol  
**Lines:** L73-L89  

## Description  
Adding an oracle through the `addOracle()` function makes the oracle effective immediately. There should be a delay period for vault owners to review the oracle in case the protocol gets compromised and a malicious oracle is added. This would only affect the case where the vault has already been configured to allow operations based on the base/quote price before the oracle is added. The case is rare but not impossible for some vault owners to do so.

## Recommendation  
Consider introducing a delay when a new oracle is added so the vault owners have enough time to review it. A possible change could be to remove the `require(currentOracle.isNotEmpty(), ...)` check in the `scheduleOracleUpdate()` function so that it also works for adding new oracles.

## Aera 
Unfortunately, this could make it tricky to create new strategies quickly, so while we can't remove `addOracle`, we will check that the oracle exists when adding a new token in `Provisioner setTokenDetails`. Fixed in PR 302.

## Spearbit 
Verified.

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

