---
# Core Classification
protocol: Harmonixfinance Hyperliquid
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57885
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarmonixFinance-Hyperliquid-Security-Review.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[C-03] NAV Value Overwrites Last Fee Harvest Time

### Overview



The `VaultStore` library has a bug that affects the protocol's revenue. This is because the library defines a critical storage key incorrectly, causing a function to always revert. The bug is located in the `lib/VaultStore.sol` file and can be fixed by changing the storage key to use the correct identifier. The team has responded that the bug has been fixed.

### Original Finding Content

## Severity

Critical Risk

## Description

The `VaultStore` library defines a critical storage key incorrectly:

```solidity
bytes32 public constant LAST_HARVEST_PERFORMANCE_FEE_TIME = keccak256(abi.encode("NAV"));
```

Instead of using a unique identifier for the last performance fee harvest time, it reuses the same key as NAV.

When `setVaultState()` is called (e.g., in `_updateVaultState()`), it stores the NAV value in `LAST_HARVEST_PERFORMANCE_FEE_TIME`. Consequently, `getLastHarvestPerformanceFeeTime()` returns the NAV value instead of the expected timestamp.

This causes `harvestPerformanceFee()` to always revert because:

```solidity
require(block.timestamp >= lastHarvest + minHarvestInterval, "HARVEST_TOO_SOON");
```

Since `lastHarvest` is set to a large NAV value, the condition will never pass.

## Location of Affected Code

File: [lib/VaultStore.sol](https://github.com/harmonixfi/core-contracts/blob/f02157aba919dcdd4a1133669361224108c5caef/contracts/lib/VaultStore.sol)

```solidity
// @audit this would return NAV value instead of LAST_HARVEST_PERFORMANCE_FEE_TIME value
bytes32 public constant LAST_HARVEST_PERFORMANCE_FEE_TIME = keccak256(abi.encode("NAV"));
```

```solidity
function setVaultState(
    FundStorage fundStorage,
    bytes32 key,
    VaultState memory vaultState
) internal {
    fundStorage.setUint256(
        keccak256(abi.encode(key, PRICE_PER_SHARE)),
        vaultState.pricePerShare
    );
    fundStorage.setUint256(
        keccak256(abi.encode(key, WITHDRAW_POOL_AMOUNT)),
        vaultState.withdrawPoolAmount
    );
    fundStorage.setUint256(
        keccak256(abi.encode(key, LAST_HARVEST_MANAGEMENT_FEE_TIME)),
        vaultState.lastHarvestManagementFeeTime
    );
    fundStorage.setUint256(
        keccak256(abi.encode(key, LAST_HARVEST_PERFORMANCE_FEE_TIME)),
        vaultState.lastHarvestPerformanceFeeTime
    );
    fundStorage.setUint256(keccak256(abi.encode(key, NAV)), vaultState.nav);
}
```

## Impact

Performance fees cannot be collected, leading to lost protocol revenue.

## Recommendation

Fix the storage key to use the correct identifier:

```solidity
bytes32 public constant LAST_HARVEST_PERFORMANCE_FEE_TIME = keccak256(abi.encode("LAST_HARVEST_PERFORMANCE_FEE_TIME"));
```

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Harmonixfinance Hyperliquid |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarmonixFinance-Hyperliquid-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

