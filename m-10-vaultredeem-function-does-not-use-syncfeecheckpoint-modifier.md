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
solodit_id: 22007
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-popcorn
source_link: https://code4rena.com/reports/2023-01-popcorn
github_link: https://github.com/code-423n4/2023-01-popcorn-findings/issues/557

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
finders_count: 7
finders:
  - ustas
  - rbserver
  - cccz
  - bin2chen
  - hansfriese
---

## Vulnerability Title

[M-10] `Vault.redeem` function does not use `syncFeeCheckpoint` modifier

### Overview


This bug report is about a vulnerability in the `Vault.redeem` function of the RedVeil (Popcorn) project. It does not use the `syncFeeCheckpoint` modifier, which is unlike the `Vault.withdraw` function. As a result, `highWaterMark` is not synced after calling the `Vault.redeem` function. This issue can cause the performance fee to be calculated inaccurately, which can lead to the `feeRecipient` receiving more or no performance fee than it should.

The proof of concept for this vulnerability is as follows. First, a user calls the `Vault.redeem` function, which does not sync `highWaterMark`. Then, the vault owner calls the `Vault.takeManagementAndPerformanceFees` function, which eventually calls the `accruedPerformanceFee` function. When calling the `Vault.accruedPerformanceFee` function, because `convertToAssets(1e18)` is less than the stale `highWaterMark`, no performance fee is accrued. As a result, the `feeRecipient` receives no performance fee when it should.

The tool used for this bug report is VS Code. The recommended mitigation steps to fix this vulnerability is to update the `Vault.redeem` function to use the `syncFeeCheckpoint` modifier. This bug has been confirmed by RedVeil (Popcorn).

### Original Finding Content


<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L253-L278> 

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L211-L240> 

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L496-L499> 

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L473-L477>

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L480-L494> 

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L447-L460>

### Impact

The following `Vault.redeem` function does not use the `syncFeeCheckpoint` modifier, which is unlike the `Vault.withdraw` function below. Because of this, after calling the `Vault.redeem` function, `highWaterMark` is not sync'ed. In this case, calling functions like `Vault.takeManagementAndPerformanceFees` after the `Vault.redeem` function is called and before the `syncFeeCheckpoint` modifier is triggered will eventually use a stale `highWaterMark` to call the `Vault.accruedPerformanceFee` function. This will cause the performance fee to be calculated inaccurately in which the `feeRecipient` can receive more performance fee than it should receive or receive no performance fee when it should.

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L253-L278>

```solidity
    function redeem(
        uint256 shares,
        address receiver,
        address owner
    ) public nonReentrant returns (uint256 assets) {
        ...
    }
```

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L211-L240>

```solidity
    function withdraw(
        uint256 assets,
        address receiver,
        address owner
    ) public nonReentrant syncFeeCheckpoint returns (uint256 shares) {
        ...
    }
```

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L496-L499>

```solidity
    modifier syncFeeCheckpoint() {
        _;
        highWaterMark = convertToAssets(1e18);
    }
```

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L473-L477>

```solidity
    function takeManagementAndPerformanceFees()
        external
        nonReentrant
        takeFees
    {}
```

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L480-L494>

```solidity
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
```

<https://github.com/code-423n4/2023-01-popcorn/blob/main/src/vault/Vault.sol#L447-L460>

```solidity
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

### Proof of Concept

The following steps can occur for the described scenario.

1.  A user calls the `Vault.redeem` function, which does not sync `highWaterMark`.
2.  The vault owner calls the `Vault.takeManagementAndPerformanceFees` function, which eventually calls the `accruedPerformanceFee` function.
3.  When calling the `Vault.accruedPerformanceFee` function, because `convertToAssets(1e18)` is less than the stale `highWaterMark`, no performance fee is accrued. If calling the `Vault.redeem` function can sync `highWaterMark`, some performance fee would be accrued through using such updated `highWaterMark` but that is not the case here.
4.  `feeRecipient` receives no performance fee when it should.

### Tools Used

VS Code

### Recommended Mitigation Steps

The `Vault.redeem` function can be updated to use the `syncFeeCheckpoint` modifier.

**[RedVeil (Popcorn) confirmed](https://github.com/code-423n4/2023-01-popcorn-findings/issues/557)** 

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
| Finders | ustas, rbserver, cccz, bin2chen, hansfriese, chaduke, eccentricexit |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-popcorn
- **GitHub**: https://github.com/code-423n4/2023-01-popcorn-findings/issues/557
- **Contest**: https://code4rena.com/reports/2023-01-popcorn

### Keywords for Search

`vulnerability`

