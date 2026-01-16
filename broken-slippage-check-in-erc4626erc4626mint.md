---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40860
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad
source_link: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
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

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Christoph Michel
  - T1MOH
---

## Vulnerability Title

Broken slippage check in erc4626.erc4626mint 

### Overview


Bug Summary: The ERC4626Bundler.sol#L36 function is not correctly applying the slippage parameter to the shares parameter, potentially resulting in users paying a higher share price than intended.

Explanation: When a user specifies shares and a maxAssets slippage parameter for the erc4626Mint function, the slippage parameter is not directly applied to the shares parameter. Instead, it is applied to the smaller value between the specified shares and the maximum mintable shares determined by the vault. This can lead to users paying a worse share price than intended.

Example: If a user wants to mint 1000 shares at a share price of 1.0 and specifies shares = 1000 and maxAssets = 1000, but the vault only allows for 1 share to be minted, the share price suddenly becomes 1000.0. This means the user would pay 1000 assets for a single share, even though they intended to pay 1 asset per share.

Recommendation: To fix this issue, the code should be adjusted to either revert the transaction if the specified shares are less than the maximum mintable shares, or to adjust the maxAssets parameter proportionally to the maximum mintable shares divided by the initial desired shares. This will ensure that the intended share price is enforced.

### Original Finding Content

## ERC4626Bundler.sol Analysis

## Context
- **File**: ERC4626Bundler.sol
- **Line**: 36

## Description
A user specifies shares and a `maxAssets` slippage parameter for the `erc4626Mint` function. However, the slippage parameter is not directly applied to the `shares` parameter; it is applied to the smaller shares value of:

```solidity
shares = Math.min(shares, IERC4626(vault).maxMint(receiver));
```

This leads to the user potentially accepting a worse share price for the mint than they specified in the function.

## Example
A user wants to mint 1000 shares at a share price of 1.0 and specifies:
- `shares = 1000`
- `maxAssets = 1000`

Imagine `maxMint` returning only 1 share and the share price suddenly being 1000.0. The user now pays 1000 assets for a single share and the slippage check still passes.

## Recommendation
- Revert if the `shares` are less than `maxMint`, or 
- Adjust the `maxAssets` proportional to `maxMint / initialDesiredShares` to enforce the same share price.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Christoph Michel, T1MOH |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad

### Keywords for Search

`vulnerability`

