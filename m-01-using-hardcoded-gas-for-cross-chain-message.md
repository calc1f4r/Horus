---
# Core Classification
protocol: StationX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41397
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
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

[M-01] Using hardcoded gas for cross-chain message

### Overview


The report mentions a bug in the Contracts LayerZeroImpl and LayerZeroDeployer. These contracts use a fixed amount of gas when sending messages between different chains, but this can cause problems. Different chains may require different amounts of gas, and the length of lists in the message can also affect the gas fee. This can result in the loss of cross-chain DAO deployments. The recommendation is to have a mechanism to estimate the required gas amount, taking into account factors such as baseGas, intrinsicGas, and executionGas.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

Contracts LayerZeroImpl and LayerZeroDeployer uses hardcoded gas amounts when they send cross-chain messages through LayerZero bridges. The issue is that different destination chains may require different amount of gas and also the message itself can cause different amount of gas. When users create DAO they specify multiple lists and the length of those lists can have impact in the cross-chain message gas fee. As result the cross-chain DAO deployment would be lost for some chains and some DAOs.

## Recommendations

Have some mechanisms to estimate the require gas amount that considers `baseGas`, `intrinsicGas` and `executionGas`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StationX |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

