---
# Core Classification
protocol: Blueberry_2025-03-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61470
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-03-26.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-02] Donated tokens are never deposited into vaults

### Overview


This bug report discusses an issue with the `HyperEvmVault` contract. The problem is that when users donate tokens to the vault, the excess balance is included in the share's price calculation but cannot be distributed. This means that users are unable to redeem all of their shares and the management fee is also affected. This can be exploited by an attacker who deposits and donates tokens, causing the total supply of shares to increase but the total amount of assets to remain the same. When an innocent user tries to redeem their shares, it will always fail because the vault's equity does not include the donated tokens. The report recommends depositing any excess amounts in the L1 vault to fix this issue.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The `HyperEvmVault` contract has to use the asset balances of the `VaultEscrow`s in the share's price calculation to handle tokens being received from the system contract. In normal the balances should not exceed the `$.requestSum.assets` value. The problem is that in case of donation to the vaults, the excess balance increases the shares price but can not be distributed, i.e. it is locked on the vaults. This way, users can not redeem all shares. Also, the excess amount increases the management fee.
Assume an attacker deposited 100 tokens and donated another 100 tokens. Then the attacker has 100 shares and the total amount of assets locked by the vault equals 200 since the `$.requestSum.assets` is zero.
HyperEvmVault.sol
```solidity
    function _totalEscrowValue(V1Storage storage $) internal view returns (uint256 assets_) {
        uint256 escrowLength = $.escrows.length;
        for (uint256 i = 0; i < escrowLength; ++i) {
            VaultEscrow escrow = VaultEscrow($.escrows[i]);
>>          assets_ += escrow.tvl();
        }

        if ($.lastL1Block == l1Block()) {
            assets_ += $.currentBlockDeposits;
        }

        return assets_ - $.requestSum.assets;
    }
```
VaultEscrow.sol
```solidity
    function tvl() public view returns (uint256) {
        uint256 assetBalance = ERC20Upgradeable(_asset).balanceOf(address(this));
        (uint64 vaultEquity_,) = _vaultEquity();
        return uint256(vaultEquity_) + assetBalance;
    }
```
Then an innocent user mints 100 shares. Now the total supply is 200 and the total amount of assets is 400.
Then the attacker requests redeeming of 100 shares. Now the total amount of assets is 200 because the `$.requestSum.assets` is 200.  
Then the user tries to request redeeming 100 shares but it will always revert because the vaults equity does not include the donated tokens:
```solidity
    function withdraw(uint64 assets_) external override onlyVaultWrapper {
>>      (uint64 vaultEquity_, uint64 lockedUntilTimestamp_) = _vaultEquity();
        require(block.timestamp > lockedUntilTimestamp_, Errors.L1_VAULT_LOCKED());

        // Update the withdraw state for the current L1 block
        L1WithdrawState storage l1WithdrawState_ = _getV1Storage().l1WithdrawState;
        _updateL1WithdrawState(l1WithdrawState_);
>>      l1WithdrawState_.lastWithdraws += assets_;

        // Ensure we havent exceeded requests for the current L1 block
>>      require(vaultEquity_ >= l1WithdrawState_.lastWithdraws, Errors.INSUFFICIENT_VAULT_EQUITY());

        // Withdraw from L1 vault
        _withdrawFromL1Vault(assets_);
    }    
<..>
    function _vaultEquity() internal view returns (uint64, uint64) {
        (bool success, bytes memory result) =
            VAULT_EQUITY_PRECOMPILE_ADDRESS.staticcall(abi.encode(address(this), _vault));
        require(success, "VaultEquity precompile call failed");

        UserVaultEquity memory userVaultEquity = abi.decode(result, (UserVaultEquity));
        uint256 equityInSpot = _scaleToSpotDecimals(userVaultEquity.equity);

        return (uint64(equityInSpot), userVaultEquity.lockedUntilTimestamp);
    }
``` 

## Recommendations

Consider depositing any excess amounts in the L1 vault.





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Blueberry_2025-03-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-03-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

