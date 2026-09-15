---
# Core Classification
protocol: Gauntlet
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7098
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - yield
  - insurance
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Emanuele Ricci
  - Eric Wang
  - Gerard Persoon
---

## Vulnerability Title

Consult with Balancer team about best approach to add and remove funds

### Overview


This bug report is about the Aera Vault, which uses AssetManager’s functionality of function managePoolBalance() to add and remove funds. There is a potential for unexpected behavior, and this also disables the capacity to store funds elsewhere to generate yield. It is recommended to doublecheck with the Balancer team which is the best approach to implement. If either ways are nonoptimal, they should be asked to implement the functionality to support this. 

If the Balancer team recommends the joinPool() /exitPool() path, it can be implemented by limiting access to joinPool() via allowlist, limiting access to exitPool() via a custom pool with an onExit() callback function, adjusting the spotprice after joinPool() /exitPool() via updateWeights(), using the AUM fees, and only keeping the BPT (pool tokens) in the vault. 

Gauntlet and Spearbit have acknowledged the issue and will get in touch with the Balancer team about the best way to use these low-level functions.

### Original Finding Content

## Security Report

**Severity:** Medium Risk  
**Context:** AeraVaultV1.sol  

**Description:**  
The Aera Vault uses AssetManager’s functionality of the function `managePoolBalance()` to add and remove funds. The standard way to add and remove funds in Balancer is via `joinPool()` / `exitPool()`. Using the `managePoolBalance()` function might lead to future unexpected behavior. Additionally, this disables the capacity to implement the original intention of AssetManager's functionality, e.g., storing funds elsewhere to generate yield.

**Recommendation:**  
Double-check with the Balancer team on the best approach to implement. If either way is nonoptimal, ask them to implement the functionality to support this. If the `joinPool()` / `exitPool()` path is recommended by the Balancer team, it can probably be implemented in the following way:

- Limit access to `joinPool()` via allowlist (as is already done).
- Limit access to `exitPool()` via a custom pool with an `onExit()` callback function (which could also integrate `allowance()`).
- Adjust the spot price after `joinPool()` / `exitPool()` via `updateWeights()`.
- Perhaps use the AUM (`managementAumFeePercentage`) fees.
- Only keep the BPT (pool tokens) in the vault.

**Gauntlet:**  
Both ways are probably not the "intended" use case; the current version seems a bit more elegant code-wise. We will get in touch with the Balancer team about the best way to use these low-level functions.

**Spearbit:**  
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Gauntlet |
| Report Date | N/A |
| Finders | Emanuele Ricci, Eric Wang, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

