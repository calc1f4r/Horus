---
# Core Classification
protocol: Karak
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41084
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-karak
source_link: https://code4rena.com/reports/2024-07-karak
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[11] `Vault.mint` and `Vault.finishRedeem` functions do not have slippage controls

### Overview

See description below for full details.

### Original Finding Content


### Description
Unlike the `Vault.deposit(uint256 assets, address to, uint256 minSharesOut)` function that includes the `minSharesOut` input for slippage control, the `Vault.mint` and `Vault.finishRedeem` functions do not have similar inputs for slippage controls. When the staker is an EOA, the `previewMint` and `Vault.mint` functions need to be called in separate transactions, and the `previewRedeem` and `Vault.finishRedeem` functions need to be called in separate transactions. When malicious frontrunnings that manipulate the vault's exchange rates occur, calling the `Vault.mint` function can cause the staker to send more underlying tokens than expected to the vault, and calling the `Vault.finishRedeem` function can cause the staker to receive less underlying tokens than expected from the vault.

Moreover, according to https://eips.ethereum.org/EIPS/eip-4626#security-considerations, `If implementors intend to support EOA account access directly, they should consider adding an additional function call for ``deposit``/``mint``/``withdraw``/``redeem`` with the means to accommodate slippage loss or unexpected deposit/withdrawal limits, since they have no other means to revert the transaction if the exact output amount is not achieved`. Hence, having no slippage controls in the `Vault.mint` and `Vault.finishRedeem` functions is also EIP-4626 non-compliant.

https://github.com/code-423n4/2024-07-karak/blob/53eb78ebda718d752023db4faff4ab1567327db4/src/Vault.sol#L94-L103
```solidity
    function deposit(uint256 assets, address to, uint256 minSharesOut)
        external
        nonReentrant
        whenFunctionNotPaused(Constants.PAUSE_VAULT_DEPOSIT_SLIPPAGE)
        returns (uint256 shares)
    {
        if (assets == 0) revert ZeroAmount();
        shares = super.deposit(assets, to);
        if (shares < minSharesOut) revert NotEnoughShares();
    }
```

https://github.com/code-423n4/2024-07-karak/blob/53eb78ebda718d752023db4faff4ab1567327db4/src/Vault.sol#L110-L119
```solidity
    function mint(uint256 shares, address to)
        public
        override(ERC4626, IVault)
        whenFunctionNotPaused(Constants.PAUSE_VAULT_MINT)
        nonReentrant
        returns (uint256 assets)
    {
        if (shares == 0) revert ZeroShares();
        assets = super.mint(shares, to);
    }
```

https://github.com/code-423n4/2024-07-karak/blob/53eb78ebda718d752023db4faff4ab1567327db4/src/Vault.sol#L157-L188
```solidity
    function finishRedeem(bytes32 withdrawalKey)
        external
        nonReentrant
        whenFunctionNotPaused(Constants.PAUSE_VAULT_FINISH_REDEEM)
    {
        (VaultLib.State storage state, VaultLib.Config storage config) = _storage();

        WithdrawLib.QueuedWithdrawal memory startedWithdrawal = state.validateQueuedWithdrawal(withdrawalKey);

        uint256 shares = startedWithdrawal.shares;
        if (shares > maxRedeem(address(this))) revert RedeemMoreThanMax();
        uint256 redeemableAssets = convertToAssets(shares);

        delete state.withdrawalMap[withdrawalKey];

        _withdraw({
            by: address(this),
            to: startedWithdrawal.beneficiary,
            owner: address(this),
            assets: redeemableAssets,
            shares: shares
        });
        ...
    }
```

### Recommended Mitigation
The `Vault.mint` and `Vault.finishRedeem` functions can be updated to include inputs for slippage controls.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Karak |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-karak
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-07-karak

### Keywords for Search

`vulnerability`

