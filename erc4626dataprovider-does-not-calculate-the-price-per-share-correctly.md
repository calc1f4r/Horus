---
# Core Classification
protocol: Hyperdrive June 2023
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35856
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
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
  - Saw-Mon and Natalie
  - Christoph Michel
  - Deivitto
  - M4rio.eth
---

## Vulnerability Title

ERC4626DataProvider does not calculate the price per share correctly

### Overview


The report is about a bug in the code of ERC4626DataProvider and ERC4626Hyperdrive contracts. It is a medium risk bug that affects the calculation of the price per share. The ERC4626DataProvider contract is returning the inverse of the price per share instead of the correct value. The recommendation is to correct the _pricePerShare() function in the ERC4626DataProvider contract by using a different calculation method and removing the return statement. This issue has been addressed in Pull Request 460, but it is suggested that both contracts use the same code to avoid any discrepancies. 

### Original Finding Content

## Severity: Medium Risk

## Context
- `ERC4626DataProvider.sol#L50-L51`
- `ERC4626Hyperdrive.sol#L129-L130`

## Description
`ERC4626DataProvider` does not calculate the price per share correctly. It returns the inverse of the price per share. This hook is implemented correctly in `ERC4626Hyperdrive`.

## Recommendation
`_pricePerShare()` needs to be corrected to:

```solidity
uint256 shareEstimate = _pool.convertToShares(FixedPointMath.ONE_18);
sharePrice = FixedPointMath.ONE_18.divDown(shareEstimate);
// return statement is not necessary since we are using a named return parameter
```

`ERC4626Hyperdrive._pricePerShare()` performs the correct calculation:
1. Not using the `totalSupply()` and `totalAssets()` to calculate this value would avoid calling the `_pool` twice.
2. Using the other endpoint, we can also remove the final division:
   ```solidity
   sharePrice = _pool.convertToAsset(FixedPointMath.ONE_18); // <--- note we are using a different endpoint
   ```
   
Note that the above should still return the value in the 18 decimal fixed format.

## DELV
Addressed in PR 460.

## Spearbit
The recommendation was done only for `contracts/src/instances/ERC4626DataProvider.sol`. It'd be good if both contracts (`ERC4626Hyperdrive.sol`) used identical code.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Hyperdrive June 2023 |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Christoph Michel, Deivitto, M4rio.eth |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf

### Keywords for Search

`vulnerability`

