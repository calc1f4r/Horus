---
# Core Classification
protocol: Superform
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40855
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9
source_link: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
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
finders_count: 4
finders:
  - ljmanini
  - solthodox
  - ladboy233 - Sparkware
  - ethan
---

## Vulnerability Title

Vaults write function return values could not reﬂect the real output 

### Overview


The bug is located in the ERC4626FormImplementation.sol file on line 240. When the superform calls the deposit or redeem methods of the underlying vault, it uses the return value to determine the amount of shares minted or assets withdrawn. However, some vaults may not accurately reflect this information, leading to incorrect accounting of shares and positions. The recommendation is to directly fetch the real output from the shares or assets balance using the balanceOf function for better security. Additionally, the contract could require the return value to match the real output for better accuracy. The bug may unfairly affect users' positions and should be fixed to ensure proper accounting.

### Original Finding Content

## ERC4626FormImplementation.sol

## Context
Line: [240](ERC4626FormImplementation.sol#L240)

## Description
When the superform calls either the `deposit` or `redeem` methods of the underlying vault, it uses the return value of those functions to fetch the amount of shares minted on deposit and the amount of assets withdrawn on redeem. Some vaults could not reflect the reality in their return values (maybe they decided to return an empty value, or they return the share values when redeeming, instead of the real assets, which might be less due to slippage of swaps in the withdraw process) and this would make the superform have incorrect accounting of its shares and superpositions, potentially accounting users' positions unfairly.

## Recommendation
Fetch the real output directly from the shares or assets balance, using `balanceOf` for extra security. The contract could even require the return value to equal the real output for more sanity.

```solidity
if (singleVaultData_.retain4626) {
    uint256 balanceBefore = v.balanceOf(address(singleVaultData_.receiverAddress));
    v.deposit(vars.assetDifference, singleVaultData_.receiverAddress);
    dstAmount = v.balanceOf(address(singleVaultData_.receiverAddress)) - balanceBefore;
} else {
    //...
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Superform |
| Report Date | N/A |
| Finders | ljmanini, solthodox, ladboy233 - Sparkware, ethan |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9

### Keywords for Search

`vulnerability`

