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
solodit_id: 42000
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/8f86c4a6-a42c-4541-a4b4-154fb8a3d919
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_spark_psm_oct2024.pdf
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
finders_count: 2
finders:
  - m4rio
  - Jonatas Martins
---

## Vulnerability Title

Increased risks of unwanted share price manipulation by manipulating the pocket USDC balance

### Overview

See description below for full details.

### Original Finding Content

## PSM3.sol Contract Overview

## Context

Location: `PSM3.sol#L286`

## Description

The `PSM3.sol` contract includes a pocket contract designed to store the USDC balance. By default, this pocket is set to the PSM address (`address(this)`), but it can be modified by invoking the `setPocket` function. This function transfers the current USDC balance to a new address, as shown below:

```solidity
if (pocket_ == address(this)) {
    usdc.safeTransfer(newPocket, amountToTransfer);
} else {
    usdc.safeTransferFrom(pocket_, newPocket, amountToTransfer);
}
```

The new Pocket address is governed by the governance contract, meaning governance has the authority to move the USDC balance. This action could impact the `totalAssets`, subsequently affecting the share price.

## Recommendation

To avoid unintended consequences, consider restricting interactions with the Pocket balance solely by the PSM.

## Comments

### Maker
Acknowledged. Agreed, this is something that we want to make very clear and known. Governance has control of the pocket and therefore has control over the USDC balance and corresponding `totalAssets`. This is a new trust assumption that was introduced with the pocket feature.

### Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | m4rio, Jonatas Martins |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_spark_psm_oct2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/8f86c4a6-a42c-4541-a4b4-154fb8a3d919

### Keywords for Search

`vulnerability`

