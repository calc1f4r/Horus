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
solodit_id: 41078
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

[05] `deposit(uint256 assets, address to)`, `deposit(uint256 assets, address to, uint256 minSharesOut)`, `mint(uint256 shares, address to)`, and `startRedeem(uint256 shares, address beneficiary)` functions do not allow staker's approved spender to call these functions on behalf of staker

### Overview

See description below for full details.

### Original Finding Content


### Description
The `Vault` contract's `deposit(uint256 assets, address to)`, `deposit(uint256 assets, address to, uint256 minSharesOut)`, `mint(uint256 shares, address to)`, and `startRedeem(uint256 shares, address beneficiary)` functions all require `msg.sender` to be the actual staker, and the staker's approved spender cannot call these functions on behalf of the staker.

According to https://eips.ethereum.org/EIPS/eip-4626:
- `deposit` `MUST support EIP-20 ``approve`` / ``transferFrom`` on ``asset`` as a deposit flow`;
- `mint` `MUST support EIP-20 ``approve`` / ``transferFrom`` on ``asset`` as a mint flow`;
- `redeem` `MUST support a redeem flow where the shares are burned from ``owner`` directly where ``msg.sender`` has EIP-20 approval over the shares of ``owner``.

Since the `Vault` contract's `deposit(uint256 assets, address to)`, `deposit(uint256 assets, address to, uint256 minSharesOut)`, `mint(uint256 shares, address to)`, and `startRedeem(uint256 shares, address beneficiary)` functions do not support the staker's approved spender to call these functions on behalf of the staker, these functions are not EIP-4626 compliant.

https://github.com/code-423n4/2024-07-karak/blob/53eb78ebda718d752023db4faff4ab1567327db4/src/Vault.sol#L78-L87
```solidity
    function deposit(uint256 assets, address to)
        public
        override(ERC4626, IVault)
        whenFunctionNotPaused(Constants.PAUSE_VAULT_DEPOSIT)
        nonReentrant
        returns (uint256 shares)
    {
        if (assets == 0) revert ZeroAmount();
        return super.deposit(assets, to);
    }
```

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

https://github.com/code-423n4/2024-07-karak/blob/53eb78ebda718d752023db4faff4ab1567327db4/src/Vault.sol#L125-L149
```solidity
    function startRedeem(uint256 shares, address beneficiary)
        external
        whenFunctionNotPaused(Constants.PAUSE_VAULT_START_REDEEM)
        nonReentrant
        returns (bytes32 withdrawalKey)
    {
        if (shares == 0) revert ZeroShares();
        if (beneficiary == address(0)) revert ZeroAddress();

        (VaultLib.State storage state, VaultLib.Config storage config) = _storage();
        address staker = msg.sender;

        uint256 assets = convertToAssets(shares);

        withdrawalKey = WithdrawLib.calculateWithdrawKey(staker, state.stakerToWithdrawNonce[staker]++);

        state.withdrawalMap[withdrawalKey].staker = staker;
        state.withdrawalMap[withdrawalKey].start = uint96(block.timestamp);
        state.withdrawalMap[withdrawalKey].shares = shares;
        state.withdrawalMap[withdrawalKey].beneficiary = beneficiary;

        this.transferFrom(msg.sender, address(this), shares);

        emit StartedRedeem(staker, config.operator, shares, withdrawalKey, assets);
    }
```

### Recommended Mitigation
The `Vault` contract's `deposit(uint256 assets, address to)`, `deposit(uint256 assets, address to, uint256 minSharesOut)`, `mint(uint256 shares, address to)`, and `startRedeem(uint256 shares, address beneficiary)` functions can be updated to allow the staker's approved spender to call these functions on behalf of the staker.



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

