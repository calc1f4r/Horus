---
# Core Classification
protocol: Berachain Honey
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52853
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Honey-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Honey-Spearbit-Security-Review-October-2024.pdf
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
  - Rvierdiiev
  - 0xLadboy
  - Noah Marconi
---

## Vulnerability Title

V2: HoneyFactoryReader required collateral calculation is incorrect

### Overview


The bug report discusses an issue with the HoneyFactoryReader contract's previewRequiredCollateral() function. This function is used to calculate the amount of collateral that users need to provide in order to mint a specific amount of Honey tokens. The problem is that the calculation involves converting the amount from 18 decimals to the asset's decimal precision and then back to 18 decimals, which results in incorrect amounts. This can cause problems for developers who are integrating the contract into their projects. The bug has been fixed in a recent update and the unnecessary conversions have been removed. 

### Original Finding Content

Severity: Medium Risk
Context: HoneyFactoryReader.sol#L75-L78
Description: HoneyFactoryReader.previewRequiredCollateral() function provides amounts that users should
pay to mint exactHoneyAmount . It calculates amounts for each asset in the basket that user should provide.
uint256 shares = exactHoneyAmount * weights[j] / mintRate;
uint256 amount = vault.previewMint(shares);
// Convert to asset decimals and then to 18 decimals.
amount = Utils.changeDecimals(amount, 18, assetDecimal);
res[j] = Utils.changeDecimals(amount, assetDecimal, 18);
In this calculation amount is returned in vault's asset decimals. So for example, if we have a USDC vault, then the
amount is returned in 106 precision.
Then later, we see that amount is converted from 18 decimals to assetDecimal and then back to 18 decimals.
This looks strange and will result in incorrect amounts, which will cause problems for integrators.
• Example for usdc vault:
assetDecimal = 6
uint256 amount = vault.previewMint(shares) = 100 * 10**6
amount = Utils.changeDecimals(amount, 18, assetDecimal); = 0
res[j] = Utils.changeDecimals(amount, assetDecimal, 18) = 0
Recommendation: Store amount returned by mint preview as required collateral.
Berachain: Fixed in PR 481.
Spearbit: Not needed conversions that caused the issue were removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Berachain Honey |
| Report Date | N/A |
| Finders | Rvierdiiev, 0xLadboy, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Honey-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Honey-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

