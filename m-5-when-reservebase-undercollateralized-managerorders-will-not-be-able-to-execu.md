---
# Core Classification
protocol: Perennial V2 Update #3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38392
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/518
source_link: none
github_link: https://github.com/sherlock-audit/2024-08-perennial-v2-update-3-judging/issues/35

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
finders_count: 2
finders:
  - panprog
  - bin2chen
---

## Vulnerability Title

M-5: when ReserveBase undercollateralized , Manager.orders will not be able to execute

### Overview


This bug report discusses an issue found in the `Manager.sol` code. The issue occurs when the `reserve.redeemPrice` is less than 1:1, resulting in an insufficient balance and causing orders to not be executed successfully. This is due to the code not taking into account the possibility of `reserve.redeemPrice` being less than 1:1. The report also includes information on the root cause, internal and external pre-conditions, attack path, impact, and potential mitigation for the issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-08-perennial-v2-update-3-judging/issues/35 

## Found by 
bin2chen, panprog
### Summary

`Manager.sol` does not take into account that `reserve.redeemPrice` may be less than 1:1
The current code, `reserve.redeem(amount)` followed by a direct transfer of the same USDC, will fail because it results in an insufficient balance and the order will not be triggered successfully

### Root Cause

in [Manager.sol:219](https://github.com/sherlock-audit/2024-08-perennial-v2-update-3/blob/main/perennial-v2/packages/perennial-order/contracts/Manager.sol#L219)

If balance `order.interfaceFee.unwrap=true`, need to convert `DSU` to `USDC`
Use `reserve.redeem(amount);`
But this method, in the case of `undercollateralized`, is possible to convert less than `amount`, but the current code implementation logic directly uses `amount`.
```solidity
    /// @inheritdoc IReserve
    function redeemPrice() public view returns (UFixed18) {
        // if overcollateralized, cap at 1:1 redemption / if undercollateralized, redeem pro-rata
        return assets().unsafeDiv(dsu.totalSupply()).min(UFixed18Lib.ONE);
    }

    function _unwrapAndWithdaw(address receiver, UFixed18 amount) private {
        reserve.redeem(amount);
        USDC.push(receiver, UFixed6Lib.from(amount));
    }
```

### Internal pre-conditions

_No response_

### External pre-conditions

1. XXXReserve.sol  undercollateralized

### Attack Path

1. alice place `TriggerOrder[1] = {price < 123 , interfaceFee.unwrap=true}`
2. XXXReserve.sol  undercollateralized , redeemPrice < 1:1
3. when price < 123  , Meet the order conditions
4. keeper call `executeOrder(TriggerOrder[1])`  , but execute fail because revert Insufficient balance

### Impact

_No response_

### PoC

_No response_

### Mitigation

```diff
    function _unwrapAndWithdaw(address receiver, UFixed18 amount) private {
-       reserve.redeem(amount);
-       USDC.push(receiver, UFixed6Lib.from(amount));
+       USDC.push(receiver, UFixed6Lib.from(reserve.redeem(amount)));
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Perennial V2 Update #3 |
| Report Date | N/A |
| Finders | panprog, bin2chen |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-08-perennial-v2-update-3-judging/issues/35
- **Contest**: https://app.sherlock.xyz/audits/contests/518

### Keywords for Search

`vulnerability`

