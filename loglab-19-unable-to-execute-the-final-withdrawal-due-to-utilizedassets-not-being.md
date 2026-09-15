---
# Core Classification
protocol: Basisos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62403
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-11-25-BasisOS.md
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
  - Hexens
---

## Vulnerability Title

[LOGLAB-19] Unable to execute the final withdrawal due to utilizedAssets() not being zero

### Overview


This bug report discusses an issue with the `LogarithmVault._isWithdrawRequestExecuted()` function in the `LogarithmVault.sol` file. This function determines whether a user's withdrawal request can be executed and returns a boolean variable called `isExecuted`. However, an attacker can manipulate the state by transferring small amounts of tokens to the strategy and hedge manager contracts, causing the `utilizedAssets()` value to remain non-zero. This prevents the final withdrawal request from being executed. The report suggests clearing idle assets before checking the `utilizedAssets()` value as a possible solution. This bug has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** src/vault/LogarithmVault.sol#L758-L761 

**Description:** The function `LogarithmVault._isWithdrawRequestExecuted()` determines whether a specific withdrawal request can be executed. It returns a boolean variable, `isExecuted`, to indicate if the user’s request has been fulfilled. A user is allowed to execute the withdrawal only when this variable evaluates to `true`.

For the last withdrawal request, the value of `isExecuted` is determined by checking whether the `utilizedAssets()` value of the strategy contract is zero. If it is, the user is permitted to withdraw their tokens. However, an attacker can manipulate the state by front-running the execution and causing `utilizedAssets()` to remain non-zero, thereby preventing the user from completing their withdrawal.

To understand this, we examine the implementation of the function `BasisStrategy.utilizedAssets()`:
```
function utilizedAssets() public view returns (uint256) {
    BasisStrategyStorage storage $ = _getBasisStrategyStorage();
    return 
        $.spotManager.getAssetValue() + 
        $.hedgeManager.positionNetBalance() + 
        assetsToWithdraw(); 
}

function assetsToWithdraw() public view returns (uint256) {
    return IERC20(asset()).balanceOf(address(this));
}
```
The `assetsToWithdraw()` function calculates its value based on the strategy contract's token balance. An attacker can exploit this by transferring 1 wei of the asset token directly to the strategy contract, making the `utilizedAssets()` return a value greater than zero. As a result, `isExecuted` will evaluate to `false`, blocking the final withdrawal request.

Another way to exploit this involves manipulating `the positionNetBalance()` value. An attacker can transfer some collateral token directly to the `OffChainPositionManager` contract, possibly causing `positionNetBalance()` to return a non-zero value. Here's the relevant implementation:
```
function positionNetBalance() public view virtual override returns (uint256) {
    OffChainPositionManagerStorage storage $ = _getOffChainPositionManagerStorage();
    PositionState memory state = $.positionStates[$.currentRound];
        
    uint256 initialNetBalance = state.netBalance 
                              + $.pendingCollateralIncrease 
                              + idleCollateralAmount(); 
    ... 
}

function idleCollateralAmount() public view returns (uint256) {
    return IERC20(collateralToken()).balanceOf(address(this));
}
```
In both cases, by transferring minimal tokens to the respective contracts, the attacker can artificially inflate the `utilizedAssets()` value, thereby preventing the execution of the last withdrawal request.
```
if (isLast) {
    // last withdraw is claimable when utilized assets is 0
    isExecuted = IStrategy(strategy()).utilizedAssets() == 0;
} else {
```

**Remediation:**  Consider clearing the idle assets within the strategy and hedge manager contract before checking if the `utilizedAssets()` is equal to zero. 

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Basisos |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-11-25-BasisOS.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

