---
# Core Classification
protocol: Cork Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41487
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/506
source_link: none
github_link: https://github.com/sherlock-audit/2024-08-cork-protocol-judging/issues/182

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
finders_count: 18
finders:
  - Pro\_King
  - ydlee
  - Trooper
  - 404Notfound
  - Abhan1041
---

## Vulnerability Title

M-2: Admin will not be able to only pause deposits in the `Vault` due to incorrect check leading to DoSed withdrawals

### Overview


The report discusses a bug found in the Cork Protocol, where the admin is unable to pause deposits in the Vault. This is due to an incorrect check in the code, which causes withdrawals to be DoSed. The root cause of the issue is a mistake in the code, where the modifier checks for withdrawal pauses instead of deposit pauses. The impact of this bug is that the admin is unable to pause deposits, which can lead to loss of funds. The team has fixed this issue in their code. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-08-cork-protocol-judging/issues/182 

## Found by 
0x73696d616f, 404Notfound, 4gontuk, Abhan1041, KupiaSec, Pro\_King, Smacaud, Trooper, durov, hunter\_w3b, korok, mladenov, octeezy, ravikiran.web3, tinnohofficial, tmotfl, ydlee, yovchev\_yoan
### Summary

The modifier [LVDepositNotPaused](https://github.com/sherlock-audit/2024-08-cork-protocol/blob/main/Depeg-swap/contracts/core/ModuleState.sol#L108) in [Vault::depositLv()](https://github.com/sherlock-audit/2024-08-cork-protocol/blob/main/Depeg-swap/contracts/core/Vault.sol#L33) checks [states[id].vault.config.isWithdrawalPaused](https://github.com/sherlock-audit/2024-08-cork-protocol/blob/main/Depeg-swap/contracts/core/ModuleState.sol#L109) instead of [states[id].vault.config.isDepositPaused](https://github.com/sherlock-audit/2024-08-cork-protocol/blob/main/Depeg-swap/contracts/libraries/State.sol#L107), which means deposits will only be paused if withdrawals are paused, DoSing withdrawals.

### Root Cause

In `ModuleState:109`, it checks `states[id].vault.config.isWithdrawalPaused` when it should check `states[id].vault.config.isDepositPaused`.

### Internal pre-conditions

1. Admin pauses deposits.

### External pre-conditions

None.

### Attack Path

1. Admin sets deposits paused, but deposits are not actually paused due to the incorrect modifier.
2. Admin either leaves deposits unpaused or pauses both deposits and withdrawals, DoSing withdrawals.

### Impact

Admin is not able to pause deposits alone which would lead to loss of funds as this is an emergency mechanism. If the admin wants to pause deposits, withdrawals would also have to be paused, DoSing withdrawals.

### PoC

`ModuleState::LVDepositNotPaused()` is incorrect:
```solidity
modifier LVDepositNotPaused(Id id) {
    if (states[id].vault.config.isWithdrawalPaused) { //@audit isDepositPaused
        revert LVDepositPaused();
    }
    _;
}
```

### Mitigation

`ModuleState::LVDepositNotPaused()` should be:
```solidity
modifier LVDepositNotPaused(Id id) {
    if (states[id].vault.config.isDepositPaused) {
        revert LVDepositPaused();
    }
    _;
}
```



## Discussion

**ziankork**

will fix

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/Cork-Technology/Depeg-swap/pull/78

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Cork Protocol |
| Report Date | N/A |
| Finders | Pro\_King, ydlee, Trooper, 404Notfound, Abhan1041, tinnohofficial, mladenov, Smacaud, korok, ravikiran.web3, KupiaSec, 4gontuk, durov, tmotfl, 0x73696d616f, octeezy, yovchev\_yoan, hunter\_w3b |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-08-cork-protocol-judging/issues/182
- **Contest**: https://app.sherlock.xyz/audits/contests/506

### Keywords for Search

`vulnerability`

