---
# Core Classification
protocol: HypurrFi_2025-02-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55470
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/HypurrFi-security-review_2025-02-12.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Pool reserves should be initialized and supplied in same transaction

### Overview


This bug report is about a vulnerability in the HyperEVM testnet. The pool is currently being initialized with reserve tokens in one script, but the tokens are being supplied in a different script. This leaves the system open to an inflation attack by the first depositor if they manipulate the pool before adding liquidity. The recommended solution is to update the deployment process so that both initialization and supplying of reserves happen in the same transaction to prevent potential exploitation.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

Currently, for the **HyperEVM testnet**, the pool is initialized with the reserve tokens in the `ConfigurrHyFiReserves` script, and the tokens are supplied in a different script, `SupplyHyFi`. This approach leaves the system vulnerable to a **inflation attack** by the first depositor on an empty reserve.
Ideally, both actions (initializing and supplying reserves) should happen in the same transaction to ensure that the system is correctly configured and cannot be exploited by an attacker who may manipulate the pool before the liquidity is added.

Instances:

- **USDC** and **sUSDe** tokens are supplied to the pool, but their respective reserves are not initialized by any of the deployment scripts as the `ConfigurrHyFiReserves` script only initializes the **KHYPE** token reserves.
- The **KHYPE reserve** is initialized by the `ConfigurrHyFiReserves` script but not supplied with liquidity.

## Recommendations

Update the deployment process so that the pool reserves are both initialized and supplied with a minimum liquidity (seed amount) in the same transaction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | HypurrFi_2025-02-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/HypurrFi-security-review_2025-02-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

