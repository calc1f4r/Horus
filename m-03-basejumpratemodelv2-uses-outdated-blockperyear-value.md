---
# Core Classification
protocol: Fungify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31816
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
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
  - Zach Obront
---

## Vulnerability Title

[M-03] BaseJumpRateModelV2 uses outdated blockPerYear value

### Overview


The report discusses a bug in the `BaseJumpRateModelV2.sol` file, which is used for setting interest rates in non-ERC721 markets. The constant `blocksPerYear` is currently set to 2102400, which was accurate before a recent merge, but is now outdated. This results in a 25% increase in the calculated interest rate. The recommendation is to update the `blocksPerYear` constant to reflect the current block spacing of 12 seconds per block. The bug has been fixed by setting the correct value in the constructor.

### Original Finding Content

In `BaseJumpRateModelV2.sol`, which is intended to be used as the rate model for all non-ERC721 markets, we use the following constant for `blocksPerYear`:
```solidity
uint public constant blocksPerYear = 2102400;
```
This value is used when setting interest rates, which are inputted on an annual basis and adjusted to the per block rate using the following function:
```solidity
function updateJumpRateModelInternal(uint baseRatePerYear, uint multiplierPerYear, uint jumpMultiplierPerYear, uint kink_) internal {
    baseRatePerBlock = baseRatePerYear / blocksPerYear;
    multiplierPerBlock = (multiplierPerYear * BASE) / (blocksPerYear * kink_);
    jumpMultiplierPerBlock = jumpMultiplierPerYear / blocksPerYear;
    kink = kink_;

    emit NewInterestParams(baseRatePerBlock, multiplierPerBlock, jumpMultiplierPerBlock, kink);
}
```
This value is forked from Compound, but is outdated. It was set before the merge, and estimated an average block time of `1 / (2102400/365/24/60/60) = 15 seconds`.

Since the merge, blocks are only 12 seconds. Using the formulas above, we can see that this results in a 25% increase in the calculated interest rate over what was intended.

```
baseRatePerYear = 1e18
baseRatePerBlock = 1e18 / 2102400 = 476190476190476
actualRatePerYear = 476190476190476 * 2628000 = 1.25e18
```

**Recommendation**

Update the `blocksPerYear` constant to `(60/12)*60*24*365 = 2628000`, which reflects the current block spacing of 12 seconds per block.

**Review**

Fixed by setting the `blockPerYear` value in the constructor in [7e0ee60622ddcbf384657da480ef9c851f2adc11](https://github.com/fungify-dao/taki-contracts/pull/9/commits/7e0ee60622ddcbf384657da480ef9c851f2adc11).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Fungify |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

