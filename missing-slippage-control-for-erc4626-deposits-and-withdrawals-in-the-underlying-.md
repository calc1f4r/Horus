---
# Core Classification
protocol: NashPoint
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46049
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/16ca9765-fc97-471e-aece-ef52f5bbc877
source_link: https://cdn.cantina.xyz/reports/cantina_nashpoint_january_2025.pdf
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
  - Jonatas Martins
  - Kurt Barry
  - Gerard Persoon
---

## Vulnerability Title

Missing slippage control for ERC4626 deposits and withdrawals in the underlying vaults 

### Overview


The bug report is about a potential vulnerability in the ERC4626Router smart contract. The functions liquidate(), fulfillRedeemRequest() and invest() have validation for depositing and withdrawing from the underlying vault, but this does not protect against slippage. This means that a malicious attack could manipulate the share values in the vault, resulting in fewer assets being returned than expected. This issue also exists in the node functions, but it is difficult to implement a solution within the ERC4646 standard. The same issue exists in the ERC7540Router, but it is also difficult to implement a solution due to the asynchronous nature and the ERC7540 standard. The recommendation is to add a slippage parameter to the affected functions to protect against share price manipulation. This would involve supplying the expected number of assets or shares and comparing it to the received amount. The bug has been fixed in a pull request (PR 244) and has been verified by Cantina Managed. 

### Original Finding Content

## ERC4626Router Vulnerability Report

## Context
- **File Locations**:
  - `ERC4626Router.sol#L78-L83`
  - `ERC4626Router.sol#L213-L214`

## Description
The functions `liquidate()`, `fulfillRedeemRequest()`, and `invest()` in `ERC4626Router` have validation for depositing and withdrawing from the underlying vault. However, this validation does not protect against slippage. A sandwich attack could manipulate share values in the vault, causing it to return fewer assets than expected while still passing the current validation.

### Additional Notes
- There is also no slippage protection on node functions, but there is no good way to implement this within the ERC4646 standard.
- There is no slippage protection on the `ERC7540Router`, but implementing this is challenging due to the asynchronous nature and the ERC7540 standard.

## Recommendation
Consider adding a slippage parameter to `liquidate()`, `invest()`, and `fulfillRedeemRequest()` to protect against share price manipulation. The expected `assets()`/`shares()` can be supplied, and this can be compared to the received amount.

## NashPoint
Fixed in PR 244.

## Cantina Managed
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | NashPoint |
| Report Date | N/A |
| Finders | Jonatas Martins, Kurt Barry, Gerard Persoon |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_nashpoint_january_2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/16ca9765-fc97-471e-aece-ef52f5bbc877

### Keywords for Search

`vulnerability`

