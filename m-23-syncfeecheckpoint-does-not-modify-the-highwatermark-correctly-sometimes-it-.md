---
# Core Classification
protocol: Popcorn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22020
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-popcorn
source_link: https://code4rena.com/reports/2023-01-popcorn
github_link: https://github.com/code-423n4/2023-01-popcorn-findings/issues/365

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
  - yield
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - cccz
  - KIntern\_NA
  - chaduke
  - rbserver
---

## Vulnerability Title

[M-23] `syncFeeCheckpoint()` does not modify the highWaterMark correctly, sometimes it might even decrease its value, resulting in charging more performance fees than it should

### Overview


This bug report is about an issue in the `Vault.syncFeeCheckpoint()` function of the RedVeil (Popcorn) smart contract. This function does not modify the `highWaterMark` correctly, sometimes even decreasing its value, resulting in charging more performance fees than it should. 

The `syncFeeCheckpoint()` modifier is supposed to update the `highWaterMark` with a higher share values. Instead of updating with a higher share values, it might actually decrease the value of `highWaterMark`. As a result, more performance fees might be charged since the `highWaterMark` was brought down again and again. 

To illustrate this, suppose the current `highWaterMark = 2 * e18` and `convertToAssets(1e18) = 1.5 * e18`. After `deposit()` is called, since the `deposit()` function has the `synFeeCheckpoint` modifier, the `highWaterMark` will be incorrectly reset to `1.5 * e18`. Suppose after some activities, `convertToAssets(1e18) = 1.99 * e18`. When `TakeFees()` is called, then the performance fee will be charged, since it wrongly decides `convertToAssets(1e18) > highWaterMark` with the wrong `highWaterMark = 1.5 * e18`. The correct `highWaterMark` should be `2 * e18`.

The recommended mitigation step is to revise the `syncFeeCheckpoint()` as follows:

     modifier syncFeeCheckpoint() {
            _;
         
             uint256 shareValue = convertToAssets(1e18);

            if (shareValue > highWaterMark) highWaterMark = shareValue;
        }

This bug has been confirmed by RedVeil (Popcorn).

### Original Finding Content


`syncFeeCheckpoint()`  does not modify the `highWaterMark` correctly, sometimes it might even decrease its value, resulting in charging more performance fees than it should.

### Proof of Concept

The `Vault.syncFeeCheckpoint()` function does not modify the `highWaterMark` correctly, sometimes it might even decrease its value, resulting in charging more performance fees than it should.  Instead of updating with a higher share values, it might actually decrease the value of `highWaterMark`. As a result, more performance fees might be charged since the `highWaterMark` was brought down again and again.

[https://github.com/code-423n4/2023-01-popcorn/blob/d95fc31449c260901811196d617366d6352258cd/src/vault/Vault.sol#
L496-L499](https://github.com/code-423n4/2023-01-popcorn/blob/d95fc31449c260901811196d617366d6352258cd/src/vault/Vault.sol#L496-L499)

     modifier syncFeeCheckpoint() {
            _;
            highWaterMark = convertToAssets(1e18);
        }

1.  Suppose the current `highWaterMark = 2 * e18` and `convertToAssets(1e18) = 1.5 * e18`.

2.  After `deposit()` is called, since the `deposit()` function has the `synFeeCheckpoint` modifier, the `highWaterMark` will be incorrectly reset to `1.5 * e18`.

3.  Suppose after some activities, `convertToAssets(1e18) = 1.99 * e18`.

4.  `TakeFees()` is called, then the performance fee will be charged, since it wrongly decides `convertToAssets(1e18) > highWaterMark` with the wrong `highWaterMark = 1.5 * e18`. The correct `highWaterMark` should be `2 * e18`:

```javascript
 modifier takeFees() {
        uint256 managementFee = accruedManagementFee();
        uint256 totalFee = managementFee + accruedPerformanceFee();
        uint256 currentAssets = totalAssets();
        uint256 shareValue = convertToAssets(1e18);

        if (shareValue > highWaterMark) highWaterMark = shareValue;

        if (managementFee > 0) feesUpdatedAt = block.timestamp;

        if (totalFee > 0 && currentAssets > 0)
            _mint(feeRecipient, convertToShares(totalFee));

        _;
    }
function accruedPerformanceFee() public view returns (uint256) {
        uint256 highWaterMark_ = highWaterMark;
        uint256 shareValue = convertToAssets(1e18);
        uint256 performanceFee = fees.performance;

        return
            performanceFee > 0 && shareValue > highWaterMark
                ? performanceFee.mulDiv(
                    (shareValue - highWaterMark) * totalSupply(),
                    1e36,
                    Math.Rounding.Down
                )
                : 0;
    }
```

5.  As a result, the performance fee is charged when it is not supposed to do so. Investors might not be happy with this.

### Tools Used

Remix

### Recommended Mitigation Steps

Revise the `syncFeeCheckpoint()` as follows:

     modifier syncFeeCheckpoint() {
            _;
         
             uint256 shareValue = convertToAssets(1e18);

            if (shareValue > highWaterMark) highWaterMark = shareValue;
        }

**[RedVeil (Popcorn) confirmed](https://github.com/code-423n4/2023-01-popcorn-findings/issues/365)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Popcorn |
| Report Date | N/A |
| Finders | cccz, KIntern\_NA, chaduke, rbserver |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-popcorn
- **GitHub**: https://github.com/code-423n4/2023-01-popcorn-findings/issues/365
- **Contest**: https://code4rena.com/reports/2023-01-popcorn

### Keywords for Search

`vulnerability`

