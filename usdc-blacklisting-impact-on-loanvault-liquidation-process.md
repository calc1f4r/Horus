---
# Core Classification
protocol: Creditswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37112
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
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
  - Zokyo
---

## Vulnerability Title

USDC Blacklisting Impact on LoanVault Liquidation Process

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Informational

**Status**: Acknowledged 

**Description**:

The LoanVault contract in the system is designed to handle collateral and debt for loans, potentially including the use of USDC as either collateral or debt. USDC, being a regulated stablecoin, includes a blacklisting feature allowing the USDC contract to prevent certain addresses from executing transactions. This feature can significantly impact the liquidation process of loans within the LoanVault contract if USDC is used.
Scenario:
Liquidation Failure: When the liquidation process is initiated, the contract attempts to transfer USDC (either as part of returning collateral to the borrower or moving debt to the liquidator). However, due to the blacklisting, the USDC transfer reverts.
Resulting Impact: The entire liquidation transaction fails, leaving the loan in a state where it can neither be repaid nor liquidated. This scenario leads to a deadlock, potentially causing financial loss and operational issues within the platform.

**Recommendation**:

Several approaches can be considered:
Pre-Liquidation Checks: Implement checks within the LoanVault contract to verify whether the involved addresses are blacklisted in the USDC contract before initiating liquidation.
Fallback Mechanisms: Develop a mechanism where alternative actions are taken if a USDC transfer fails due to blacklisting. This could involve using another form of collateral or a secondary process for dealing with blacklisted addresses.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Creditswap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

