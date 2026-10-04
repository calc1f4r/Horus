---
# Core Classification
protocol: Liquorice
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49452
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#12-inability-to-liquidate-at-high-utilization
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
  - MixBytes
---

## Vulnerability Title

Inability to liquidate at high utilization

### Overview


The liquidation function in the LendingPool contract is not working properly and can result in bad debt accumulation. This means that if a borrower has borrowed a large amount of one asset and another borrower has borrowed a large amount of a different asset, there may not be enough funds in the pool to liquidate both borrowers if the value of one of the assets decreases rapidly. This can lead to a high level of bad debt that is not profitable for liquidators to handle. To fix this, it is recommended to add an option to receive the liquidated user's `CollateralToken` instead of transferring the underlying asset.

### Original Finding Content

##### Description
The liquidation function reverts if there aren’t enough funds in the pool to perform the transfer:
```solidity
function _liquidation
    ...
    (uint256 withdrawnLockedAmount, uint256 lockedAmountToTransfer,) =
    _withdrawAsset(
        _withdrawal[i].asset, 
        _withdrawal[i].amount, 
        _borrower, 
        true, 
        protocolLiquidationFee);

  (uint256 withdrawnAmount, uint256 amountToTransfer,) =
    _withdrawAsset(
        _withdrawal[i].asset, 
        _withdrawal[i].amount, 
        _borrower, 
        false, 
        protocolLiquidationFee);

    ERC20(_withdrawal[i].asset).safeTransfer(
        _liquidator, 
        lockedAmountToTransfer + amountToTransfer);
```
https://github.com/Liquorice-HQ/contracts/blob/a5b4c6a56df589b8ea4f6c7b8cb028b1723ad479/src/contracts/LendingPool.sol#L667

This can lead to bad debt accumulation. For example, consider a scenario with assets WETH and WBTC. One whale borrows almost all the WETH against WBTC, while another borrows nearly all the WBTC against WETH. Now, both pools lack enough funds for a complete liquidation of both whales. If one of the assets rapidly loses value, no one will be able to liquidate the unhealthy whale, and at some point the level of bad debt will reach an unprofitable threshold for liquidators.

##### Recommendation

We recommend adding an option to receive the liquidated user's `CollateralToken` instead of transferring the underlying asset.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Liquorice |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#12-inability-to-liquidate-at-high-utilization
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

