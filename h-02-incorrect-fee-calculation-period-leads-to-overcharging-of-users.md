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
solodit_id: 57887
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

[H-02] Incorrect Fee Calculation Period Leads to Overcharging of Users

### Overview


The report describes a bug in the `FundContract` that causes users to be overcharged for management and performance fees. This happens because the contract initializes certain timestamps at the time of setup, rather than when funds are actually deposited. As a result, fees are calculated over a longer period of time, leading to financial loss for users. The recommendation is to only consider periods when funds were actually deposited, which has been implemented by the team.

### Original Finding Content

## Severity

High Risk

## Description

The `FundContract` initializes `lastHarvestManagementFeeTime` and `lastHarvestPerformanceFeeTime` to `block.timestamp` during `setupVaultSetting()`. This creates an issue when deposits occur significantly later, as the fee calculation in `harvestManagementFee()` and `harvestPerformanceFee()` uses the full time delta since contract initialization rather than the actual period during which funds were managed.

The problem manifests in `_calculateManagementFeeAmount()`, where the period variable is calculated as `timestamp - lastHarvestManagementFeeTime`. Since `lastHarvestManagementFeeTime` was set at contract initialization (potentially long before any deposits), this results in fees being calculated over an artificially extended period, leading to overcharging.

## Location of Affected Code

File: [vaults/hyperliquid/fundContract.sol](https://github.com/harmonixfi/core-contracts/blob/f02157aba919dcdd4a1133669361224108c5caef/contracts/vaults/hyperliquid/fundContract.sol)

```solidity
function _calculateManagementFeeAmount(
    uint256 timestamp,
    uint256 nav
) private view returns (uint256) {
    uint256 managementFeeRate = VaultStore.getManagementFeeRate(
        fundStorage,
        VaultStore.getVaultKey(address(this))
    );

    uint256 lastHarvestManagementFeeTime = VaultStore
        .getLastHarvestManagementFeeTime(
            fundStorage,
            VaultStore.getVaultKey(address(this))
        );
    uint256 perSecondRate = (managementFeeRate * 1e12) / (365 * 86400) + 1; // +1 mean round up second rate
    uint256 period = timestamp - lastHarvestManagementFeeTime;
    return (nav * perSecondRate * period) / 1e14;
}
```

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


    VaultStore.VaultState memory vaultState = VaultStore.VaultState(
        10 ** decimals(),
        0,
        0,
        // @audit Fee would be charged more
        block.timestamp,
        block.timestamp,
        0
    );

    VaultStore.setVaultState(fundStorage, vaultKey, vaultState);
}
```

## Impact

Users will be charged management and performance fees for periods when their funds were not deposited in the contract. This constitutes financial loss for users, as they pay fees disproportionate to the actual service period. The overcharging could significantly reduce user returns, especially if there's a long gap between contract deployment and first deposits.

## Recommendation

The fee calculation should only consider periods when funds were actually deposited. This can be achieved by initializing harvest timestamps on the first deposit rather than the contract setup.

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

