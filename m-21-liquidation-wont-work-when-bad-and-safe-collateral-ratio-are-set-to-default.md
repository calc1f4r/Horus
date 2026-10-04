---
# Core Classification
protocol: Lybra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21166
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-lybra
source_link: https://code4rena.com/reports/2023-06-lybra
github_link: https://github.com/code-423n4/2023-06-lybra-findings/issues/44

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
finders_count: 6
finders:
  - KupiaSec
  - T1MOH
  - devival
  - y51r
  - kenta
---

## Vulnerability Title

[M-21] Liquidation won't work when bad and safe collateral ratio are set to default values

### Overview


This bug report describes an issue with the `getBadCollateralRatio()` function in the LybraFinance protocol. The function will revert if `vaultBadCollateralRatio[pool]` and `vaultSafeCollateralRatio[pool]` are set to 0, blocking liquidation flow. This is because a value of 1e19 is decremented from `vaultSafeCollateralRatio[pool]`, however, `vaultSafeCollateralRatio[pool]` can be set to 0, which should mean 160%. Additionally, the `BadCollateralRatio` can't be set when `SafeCollateralRatio` is default, as `newRatio` must be less than 10%.

The bug was identified through manual review and assessed as an Invalid Validation. The severity was decreased to Medium by 0xean (judge) and confirmed by LybraFinance. The recommended mitigation step is to use functions `getSafeCollateralRatio()` and `getBadCollateralRatio()` in all the occurences instead of internal accessing variables, as variables can be zero.

### Original Finding Content


`getBadCollateralRatio()` will revert because of underflow, if `vaultBadCollateralRatio[pool]` and `vaultSafeCollateralRatio[pool]` are set to 0 (i.e. using default ratios 150% and 130% accordingly).
It blocks liquidation flow.

### Proof of Concept

1e19 is decremented from value `vaultSafeCollateralRatio[pool]`:

```solidity
    function getBadCollateralRatio(address pool) external view returns(uint256) {
        if(vaultBadCollateralRatio[pool] == 0) return vaultSafeCollateralRatio[pool] - 1e19;
        return vaultBadCollateralRatio[pool];
    }
```

However, `vaultSafeCollateralRatio[pool]` can be set to 0, which should mean 160%:

```solidity
    function getSafeCollateralRatio(
        address pool
    ) external view returns (uint256) {
        if (vaultSafeCollateralRatio[pool] == 0) return 160 * 1e18;
        return vaultSafeCollateralRatio[pool];
    }
```

As a result, incorrect accounting block liquidation when using default values.

Also, I think this is similar issue, but different impact; therefore, described in this issue. `BadCollateralRatio` can't be set when `SafeCollateralRatio` is default, as `newRatio` must be less than 10%:

<https://github.com/code-423n4/2023-06-lybra/blob/5d70170f2c68dbd3f7b8c0c8fd6b0b2218784ea6/contracts/lybra/configuration/LybraConfigurator.sol#L127>

```solidity
    function setBadCollateralRatio(address pool, uint256 newRatio) external onlyRole(DAO) {
        require(newRatio >= 130 * 1e18 && newRatio <= 150 * 1e18 && newRatio <= vaultSafeCollateralRatio[pool] + 1e19, "LNA");
        ...
    }
```

### Tools Used

Manual Review

### Recommended Mitigation Steps

Instead of internal accessing variables, use functions `getSafeCollateralRatio()` and `getBadCollateralRatio()` in all the occurences because variables can be zero.

### Assessed type

Invalid Validation

**[0xean (judge) decreased severity to Medium](https://github.com/code-423n4/2023-06-lybra-findings/issues/44#issuecomment-1656232136)**

**[LybraFinance confirmed](https://github.com/code-423n4/2023-06-lybra-findings/issues/44#issuecomment-1656709539)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lybra Finance |
| Report Date | N/A |
| Finders | KupiaSec, T1MOH, devival, y51r, kenta, RedTiger |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-lybra
- **GitHub**: https://github.com/code-423n4/2023-06-lybra-findings/issues/44
- **Contest**: https://code4rena.com/reports/2023-06-lybra

### Keywords for Search

`vulnerability`

