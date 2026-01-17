---
# Core Classification
protocol: Mycelium
chain: everychain
category: dos
vulnerability_type: dos

# Attack Vector Details
attack_type: dos
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3401
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/7
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-mycelium-judging/tree/main/006-M

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - dos
  - denial-of-service
  - external_contract

protocol_categories:
  - dexes
  - cdp
  - cross_chain
  - synthetics
  - oracle

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - IllIllI
  - WATCHPUG
  - berndartmueller
  - ak1
  - ctf\_sec
---

## Vulnerability Title

M-1: When one of the plugins is broken or paused, `deposit()` or `withdraw()` of the whole Vault contract can malfunction

### Overview


This bug report is about an issue found in the Vault contract, where a malfunctioning plugin can cause the whole contract to malfunction. The malfunctioning plugin can be paused or broken, and this prevents users from depositing or withdrawing funds from the Vault. The issue was found by ctf\_sec, IllIllI, berndartmueller, ak1, and WATCHPUG.

The bug is caused by the fact that the deposit will always go to the first plugin, and withdrawal from the last plugin first. This means that when a plugin is malfunctioning, the Vault contract cannot be used as normal. Neither can the owner remove the plugin or rebalance it to other plugins to resume operation. This is because withdrawal from the plugin can not be done and removing a plugin or rebalancing both rely on this.

The code snippets in the report demonstrate this issue and the tools used to find it were manual review. Two recommendations are given to fix this issue. The first is to consider introducing a new method to pause one plugin from the Vault contract level. The second is to consider returning 0 for availableForDeposit() and availableForWithdrawal() when the pool is paused in AaveV2Plugin.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-mycelium-judging/tree/main/006-M 

## Found by 
ctf\_sec, IllIllI, berndartmueller, ak1, WATCHPUG

## Summary

One malfunctioning plugin can result in the whole Vault contract malfunctioning.

## Vulnerability Detail

A given plugin can temporally or even permanently becomes malfunctioning (cannot deposit/withdraw) for all sorts of reasons.

Eg, Aave V2 Lending Pool can be paused, which will prevent multiple core functions that the Aave v2 plugin depends on from working, including `lendingPool.deposit()` and `lendingPool.withdraw()`.

https://github.com/aave/protocol-v2/blob/master/contracts/protocol/lendingpool/LendingPool.sol#L54

```soldity
  modifier whenNotPaused() {
    _whenNotPaused();
    _;
  }
```

https://github.com/aave/protocol-v2/blob/master/contracts/protocol/lendingpool/LendingPool.sol#L142-L146

```solidity
  function withdraw(
    address asset,
    uint256 amount,
    address to
  ) external override whenNotPaused returns (uint256) {
```

That's because the deposit will always goes to the first plugin, and withdraw from the last plugin first.

## Impact

When Aave V2 Lending Pool is paused, users won't be able to deposit or withdraw from the vault.

Neither can the owner remove the plugin nor rebalanced it to other plugins to resume operation.

Because withdrawal from the plugin can not be done, and removing a plugin or rebalancing both rely on this.

## Code Snippet

https://github.com/sherlock-audit/2022-10-mycelium/blob/main/mylink-contracts/src/Vault.sol#L456-L473

https://github.com/sherlock-audit/2022-10-mycelium/blob/main/mylink-contracts/src/Vault.sol#L492-L519

## Tool used

Manual Review

## Recommendation

1. Consider introducing a new method to pause one plugin from the Vault contract level;

2. Aave V2's Lending Pool contract has a view function [`paused()`](https://github.com/aave/protocol-v2/blob/master/contracts/protocol/lendingpool/LendingPool.sol#L685), consider returning `0` for `availableForDeposit()` and ``availableForWithdrawal() when pool paused in AaveV2Plugin:

```solidity
function availableForDeposit() public view override returns (uint256) {
    if (lendingPool.paused()) return 0;
    return type(uint256).max - balance();
}
```

```solidity
function availableForWithdrawal() public view override returns (uint256) {
    if (lendingPool.paused()) return 0;
    return balance();
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Mycelium |
| Report Date | N/A |
| Finders | IllIllI, WATCHPUG, berndartmueller, ak1, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-mycelium-judging/tree/main/006-M
- **Contest**: https://app.sherlock.xyz/audits/contests/7

### Keywords for Search

`DOS, Denial-Of-Service, External Contract`

