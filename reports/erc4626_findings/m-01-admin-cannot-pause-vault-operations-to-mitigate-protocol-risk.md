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
solodit_id: 57891
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarmonixFinance-Hyperliquid-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-01] Admin Cannot Pause Vault Operations to Mitigate Protocol Risk

### Overview


This bug report discusses an issue with the `VaultSetting` struct in the `Vault` contract. The `isPaused` boolean field is not being properly initialized or updated, making it impossible for administrators to pause core vault operations during abnormal or high-risk scenarios. This could potentially expose user funds to loss or exploitation in the event of an exploit or required upgrade. The recommendation is to introduce a dedicated administrative function to explicitly update the `isPaused` state. The team has responded that the issue has been fixed.

### Original Finding Content

## Severity

Medium Risk

## Description

The `VaultSetting` struct within the `Vault` contract includes an `isPaused` boolean field intended to allow administrators to pause core vault operations such as deposits and withdrawals during abnormal or high-risk scenarios. The `setupVaultSetting()` function is responsible for initializing and updating vault parameters, including minimumSupply, capacity, and various fee configurations. However, this function hardcodes the `isPaused` field to false, and there exists an administrative function to set `isPaused` to true.

This design omission results in a critical gap in operational controls. Although the contract appears to support a paused state, in practice, there is no mechanism for administrators to activate it. As a result, the pause functionality is entirely unusable.

## Location of Affected Code

File: [vaults/hyperliquid/fundContract.sol](https://github.com/harmonixfi/core-contracts/blob/f02157aba919dcdd4a1133669361224108c5caef/contracts/vaults/hyperliquid/fundContract.sol)

```solidity
function setupVaultSetting(
    uint256 _minimumSupply,
    uint256 _capacity,
    uint256 _performanceFeeRate,
    uint256 _managementFeeRate,
    uint8 _tradingFeeRate,
    address _feeReceiver,
    uint256 _networkCost
) external nonReentrant {
      _auth(Role.ADMIN);
      bytes32 vaultKey = VaultStore.getVaultKey(address(this));
      VaultStore.VaultSetting memory vaultSetting = VaultStore.VaultSetting(
          _minimumSupply,
          _capacity,
          _performanceFeeRate,
          _managementFeeRate,
          _tradingFeeRate,
          _feeReceiver,
          false,
          _networkCost
      );
      VaultStore.setVaultSetting(fundStorage, vaultKey, vaultSetting);
      // code
}
```

## Impact

The inability to pause vault operations undermines the protocol's resilience to emergency situations. In the event of an exploit or a required upgrade, administrators would be unable to halt deposits and withdrawals, potentially exposing user funds to loss or exploitation.

## Recommendation

Introduce a dedicated administrative function, such as `pauseVault()` and `unpauseVault()`, that allows authorized roles (e.g., `Role.ADMIN`) to explicitly update the `isPaused` state for the vault.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

