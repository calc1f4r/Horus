---
# Core Classification
protocol: Renzo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33497
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-renzo
source_link: https://code4rena.com/reports/2024-04-renzo
github_link: https://github.com/code-423n4/2024-04-renzo-findings/issues/569

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

protocol_categories:
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 27
finders:
  - TECHFUND
  - ladboy233
  - t0x1c
  - guhu95
  - mt030d
---

## Vulnerability Title

[M-02] Withdrawals and Claims are meant to be pausable, but it is not possible in practice

### Overview


This bug report is about a contract called `WithdrawQueue` that has a problem with its pausing capabilities. The contract is supposed to allow an administrator to pause users' withdrawals and claims, but this is not working as expected. The contract has two functions, `pause` and `unpause`, which are supposed to be accessible only to the administrator. However, these functions do not have the necessary `whenNotPaused` modifier, which means they can still be accessed even when the contract is paused. This is especially problematic for the `withdraw` and `claim` functions, which are accessible to users and can still be used even when the contract is supposed to be paused. To fix this issue, the bug report recommends implementing the `whenNotPaused` modifier on these two functions. The report also includes a patch that shows how this can be done. The bug has been confirmed and mitigated by the project team. 

### Original Finding Content


<https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L13>

<https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L206>

<https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L279>

### Impact

Administrator is not able to pause users' withdrawals and claims as expected.

### Proof of Concept

The `WithdrawQueue` contract inherits `PausableUpgradable` to provide pausing capabilities to the administrator on users' withdrawals and claims.
The contract correctly exposes the `_pause()` and `_unpause()` internal functions through access restricted external functions.

However, none of the functions implement the `whenNotPaused` modifier. This is especially problematic for user-accessible functions: `withdraw` and `claim`.

```solidity
// @POC: WithdrawQueue inherits PausableUpgradeable
contract WithdrawQueue is
    Initializable,
    PausableUpgradeable,
    ReentrancyGuardUpgradeable,
    WithdrawQueueStorageV1
{
    // ...

    function initialize(
        IRoleManager _roleManager,
        IRestakeManager _restakeManager,
        IEzEthToken _ezETH,
        IRenzoOracle _renzoOracle,
        uint256 _coolDownPeriod,
        TokenWithdrawBuffer[] calldata _withdrawalBufferTarget
    ) external initializer {

        // ...

        __Pausable_init();

        // ...
    }

    function pause() external onlyWithdrawQueueAdmin {// @POC: pause is accessible to admin
        _pause();
    }

    function unpause() external onlyWithdrawQueueAdmin {// @POC: unpause is accessible to admin
        _unpause();
    }

    function withdraw(uint256 _amount, address _assetOut) external nonReentrant {// @POC: pause has no impact
        // ...
    }

    function claim(uint256 withdrawRequestIndex) external nonReentrant {// @POC: pause has no impact
        // ...
    }
}
```

### Recommended Mitigation Steps

Consider implementing `whenNotPaused` modifier on `claim` and `withdraw` functions. The following patch implements such a fix.

```diff
diff --git a/contracts/Withdraw/WithdrawQueue.sol b/contracts/Withdraw/WithdrawQueue.sol
index 786238c..91ec77b 100644
--- a/contracts/Withdraw/WithdrawQueue.sol
+++ b/contracts/Withdraw/WithdrawQueue.sol
@@ -203,7 +203,7 @@ contract WithdrawQueue is
      * @param   _amount  amount of ezETH to withdraw
      * @param   _assetOut  output token to receive on claim
      */
-    function withdraw(uint256 _amount, address _assetOut) external nonReentrant {
+    function withdraw(uint256 _amount, address _assetOut) whenNotPaused external nonReentrant {
         // check for 0 values
         if (_amount == 0 || _assetOut == address(0)) revert InvalidZeroInput();
 
@@ -276,7 +276,7 @@ contract WithdrawQueue is
      * @dev     revert on claim before cooldown period
      * @param   withdrawRequestIndex  Index of the Withdraw Request user wants to claim
      */
-    function claim(uint256 withdrawRequestIndex) external nonReentrant {
+    function claim(uint256 withdrawRequestIndex) whenNotPaused external nonReentrant {
         // check if provided withdrawRequest Index is valid
         if (withdrawRequestIndex >= withdrawRequests[msg.sender].length)
             revert InvalidWithdrawIndex();
```

*Note: The patch can be applied with `git apply`.*

### Assessed type

Context

**[jatinj615 (Renzo) confirmed](https://github.com/code-423n4/2024-04-renzo-findings/issues/569#event-12915964089)**

**[Renzo mitigated](https://github.com/code-423n4/2024-06-renzo-mitigation?tab=readme-ov-file#scope)**

**Status:** Mitigation confirmed. Full details in reports from [0xCiphky](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/13), [grearlake](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/52), [Fassi\_Security](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/45), [LessDupes](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/30), and [Bauchibred](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/25).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Renzo |
| Report Date | N/A |
| Finders | TECHFUND, ladboy233, t0x1c, guhu95, mt030d, tapir, Sathish9098, 0xBeastBoy, eeshenggoh, NentoR, Aymen0909, 0x73696d616f, ak1, zigtur, ilchovski, TheFabled, FastChecker, oakcobalt, cu5t0mpeo, 1, 2, xg, bigtone, 0xCiphky, LessDupes |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-renzo
- **GitHub**: https://github.com/code-423n4/2024-04-renzo-findings/issues/569
- **Contest**: https://code4rena.com/reports/2024-04-renzo

### Keywords for Search

`vulnerability`

