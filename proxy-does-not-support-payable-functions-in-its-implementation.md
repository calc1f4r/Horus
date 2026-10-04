---
# Core Classification
protocol: MakerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40895
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/d3ba51dd-e2ef-41fe-a33f-7da5573256e6
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_nov2023.pdf
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
finders_count: 2
finders:
  - m4rio
  - Christoph Michel
---

## Vulnerability Title

Proxy does not support payable functions in its implementation

### Overview


The report discusses a bug in the UpgradeableProxy contract where the fallback function is not defined as payable. This means that if the implementation contract has any functions that require ETH to be sent, they will not be accessible. The recommendation is to add the payable keyword to the fallback function. However, after internal discussion, it was decided that this functionality will not be added. The risk level of this bug is classified as low.

### Original Finding Content

## UpgradeableProxy Audit

## Context
`UpgradeableProxy.sol#L37`

## Description
The `UpgradeableProxy.fallback` function that forwards the calls to the implementation contract is not defined as `payable`. If the implementation contract defines any functions that require ETH to be sent, they will be inaccessible as the `UpgradeableProxy.fallback` will revert.

## Recommendation
Consider adding the `payable` keyword to the `UpgradeableProxy`'s fallback function.

```solidity
- fallback() external {
+ fallback() external payable {
```

## Responses
**Maker:** Acknowledged. After internal discussion, it was decided that we won’t use `payable` functionality, so this won’t be added.  
**Cantina:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | m4rio, Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_nov2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/d3ba51dd-e2ef-41fe-a33f-7da5573256e6

### Keywords for Search

`vulnerability`

