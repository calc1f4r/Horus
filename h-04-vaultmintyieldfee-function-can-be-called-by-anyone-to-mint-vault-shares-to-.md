---
# Core Classification
protocol: PoolTogether
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26364
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-pooltogether
source_link: https://code4rena.com/reports/2023-07-pooltogether
github_link: https://github.com/code-423n4/2023-07-pooltogether-findings/issues/396

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 2

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 38
finders:
  - keccak123
  - 0xStalin
  - josephdara
  - ni8mare
  - 0xMirce
---

## Vulnerability Title

[H-04] `Vault.mintYieldFee` function can be called by anyone to mint `Vault Shares` to any recipient address

### Overview


A bug was found in the `Vault.mintYieldFee` external function, which is used to mint `Vault shares` to the yield fee `_recipient`. This function allows the caller to set the `_recipient` (address of the yield fee recipient). It does not use the `_yieldFeeRecipient` state variable, which was set in the `Vault.constructor` as the `yield fee recipient`. This means, anyone can steal the available `yield fee` from the vault by `minting shares` to their own address or to any address of their choice.

It is recommended to use the `_yieldFeeRecipient` state variable value as the `yield fee recipient` inside the `Vault.mintYieldFee` external function and to remove the input parameter `address _recipient` from the `Vault.mintYieldFee` function; so that the caller will not be able to mint shares to any arbitrary address of their choice and steal the yield fee of the protocol. The bug has been confirmed and mitigated by PoolTogether.

### Original Finding Content


The `Vault.mintYieldFee` external function is used to mint `Vault shares` to the yield fee `_recipient`. The function is an external function and can be called by anyone since there is no access control. The function will revert only under following two conditions:

1. If the Vault is under-collateralized.
2. If the `_shares` are greater than the accrued `_yieldFeeTotalSupply`.

The issue with this function is, it allows the caller to set the `_recipient` (address of the yield fee recipient). It does not use the `_yieldFeeRecipient` state variable, which was set in the `Vault.constructor` as the `yield fee recipient`. 

Which means, anyone can steal the available `yield fee` from the vault (as long as the above two revert conditions are not satisfied) by `minting shares` to their own address or to any address of their choice.

### Proof of Concept

```solidity
  function mintYieldFee(uint256 _shares, address _recipient) external {
    _requireVaultCollateralized();
    if (_shares > _yieldFeeTotalSupply) revert YieldFeeGTAvailable(_shares, _yieldFeeTotalSupply);

    _yieldFeeTotalSupply -= _shares;
    _mint(_recipient, _shares);

    emit MintYieldFee(msg.sender, _recipient, _shares);
  }
```

<https://github.com/GenerationSoftware/pt-v5-vault/blob/b1deb5d494c25f885c34c83f014c8a855c5e2749/src/Vault.sol#L394-L402>

### Tools Used

VSCode

### Recommended Mitigation Steps

Hence, it is recommended to use the `_yieldFeeRecipient` state variable value as the `yield fee recipient` inside the `Vault.mintYieldFee` external function and to remove the input parameter `address _recipient` from the `Vault.mintYieldFee` function; so that the caller will not be able to mint shares to any arbitrary address of their choice and steal the yield fee of the protocol.

The updated function should be as follows:

```solidity
  function mintYieldFee(uint256 _shares) external {
    _requireVaultCollateralized();
    if (_shares > _yieldFeeTotalSupply) revert YieldFeeGTAvailable(_shares, _yieldFeeTotalSupply);

    _yieldFeeTotalSupply -= _shares;
    _mint(_yieldFeeRecipient, _shares);

    emit MintYieldFee(msg.sender, _recipient, _shares);
  } 
```

**[asselstine (PoolTogether) confirmed](https://github.com/code-423n4/2023-07-pooltogether-findings/issues/396#issuecomment-1644711562)**

**[PoolTogether mitigated](https://github.com/code-423n4/2023-08-pooltogether-mitigation#individual-prs):**
> Removed recipient param.<br>
> PR: https://github.com/GenerationSoftware/pt-v5-vault/pull/7

**Status**: Mitigation confirmed. Full details in reports from [rvierdiiev](https://github.com/code-423n4/2023-08-pooltogether-mitigation-findings/issues/30), [dirk\_y](https://github.com/code-423n4/2023-08-pooltogether-mitigation-findings/issues/5) and [0xStalin](https://github.com/code-423n4/2023-08-pooltogether-mitigation-findings/issues/26).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | PoolTogether |
| Report Date | N/A |
| Finders | keccak123, 0xStalin, josephdara, ni8mare, 0xMirce, dacian, markus\_ether, Nyx, ravikiranweb3, seeques, shaka, peanuts, alexweb3, minhtrng, Praise, LuchoLeonel1, 0xPsuedoPandit, wangxx2026, KupiaSec, mahdirostami, ktg, GREY-HAWK-REACH, btk, Co0nan, 0xbepresent, Udsen, Aymen0909, zzzitron, teawaterwire, serial-coder, Bobface, Jeiwan, bin2chen, dirk\_y, ptsanev, John, rvierdiiev, RedTiger |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-pooltogether
- **GitHub**: https://github.com/code-423n4/2023-07-pooltogether-findings/issues/396
- **Contest**: https://code4rena.com/reports/2023-07-pooltogether

### Keywords for Search

`vulnerability`

