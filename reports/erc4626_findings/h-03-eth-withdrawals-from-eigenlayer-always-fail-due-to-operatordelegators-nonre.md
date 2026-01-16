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
solodit_id: 33490
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-renzo
source_link: https://code4rena.com/reports/2024-04-renzo
github_link: https://github.com/code-423n4/2024-04-renzo-findings/issues/368

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

protocol_categories:
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - blutorque
  - kennedy1030
  - KupiaSec
  - 0x73696d616f
  - ilchovski
---

## Vulnerability Title

[H-03] ETH withdrawals from EigenLayer always fail due to `OperatorDelegator`'s nonReentrant `receive()`

### Overview


Bug report for code-423n4/2024-04-renzo repository

The bug is located in the OperatorDelegator.sol file in the contracts/Delegation folder. The vulnerable functions are completeQueuedWithdrawal() and receive(). These functions are marked as nonReentrant, meaning they cannot be called again while they are still executing. However, in this case, the receive() function is normally called by the EigenPod contract during the execution of the completeQueuedWithdrawal() function. This creates a reentrancy issue that prevents ETH withdrawals from being completed. To fix this, the nonReentrant modifier should be removed from the receive() function or only applied when the caller is not the EigenPod contract. This bug has been confirmed and mitigated by the Renzo team.

### Original Finding Content


<https://github.com/code-423n4/2024-04-renzo/blob/519e518f2d8dec9acf6482b84a181e403070d22d/contracts/Delegation/OperatorDelegator.sol#L269>

<https://github.com/code-423n4/2024-04-renzo/blob/519e518f2d8dec9acf6482b84a181e403070d22d/contracts/Delegation/OperatorDelegator.sol#L501>

### Vulnerability details

The [`OperatorDelegator.completeQueuedWithdrawal()`](https://github.com/code-423n4/2024-04-renzo/blob/519e518f2d8dec9acf6482b84a181e403070d22d/contracts/Delegation/OperatorDelegator.sol#L265) function is used by admins to finalize previously initiated withdraws of shares from EigenLayer.

We note that both this and the OperatorDelegator's `receive()` functions are `nonReentrant`:

```Solidity
File: OperatorDelegator.sol
265:     function completeQueuedWithdrawal(
266:         IDelegationManager.Withdrawal calldata withdrawal,
267:         IERC20[] calldata tokens,
268:         uint256 middlewareTimesIndex
269:     ) external nonReentrant onlyNativeEthRestakeAdmin {
270:         uint256 gasBefore = gasleft();
271:         if (tokens.length != withdrawal.strategies.length) revert MismatchedArrayLengths();
272: 
273:         // complete the queued withdrawal from EigenLayer with receiveAsToken set to true
274:         delegationManager.completeQueuedWithdrawal(withdrawal, tokens, middlewareTimesIndex, true);
---
501:     receive() external payable nonReentrant {
502:         // check if sender contract is EigenPod. forward full withdrawal eth received
503:         if (msg.sender == address(eigenPod)) {
504:             restakeManager.depositQueue().forwardFullWithdrawalETH{ value: msg.value }();
```

However, the `receive()` function is normally called by the `EigenPod` in the call stack originated by the L274 `completeQueuedWithdrawal()` when `receiveAsTokens == true` like in this case. This particular instance of reentrancy is not only acceptable but also required to allow ETH redemptions from EigenLayer. However, the `nonReentrant` modifier prevents it.

### Impact

All withdrawals that include any amount of ETH will be permanently stuck in EigenLayer and won't be redeemable. Only amounts coming from new deposits can be redeemed and the team will have no way to fill the withdrawal queues. To unblock them, the team will necessarily have to upgrade `OperatorDelegator`.

### Proof of Concept

To prove the concept, it's sufficient to upgrade `OperatorDelegator` on a mainnet fork and initiate a withdrawal that has ETH among the withdrawn strategies.

While it would be too bulky to provide a coded PoC, you can find in [this GH Gist](<https://gist.github.com/assets/145972240/0f2500e1-1f93-4daf-8a5f-509da79f2e96>) the Foundry traces of such failed call on a mainnet fork.

### Tools Used

Foundry

### Recommended Mitigation Steps

Consider removing `nonReentrant` from OperatorDelegator's `receive`, or applying the modifier only in case `msg.sender != eigenPod`.

### Assessed type

Reentrancy

**[jatinj615 (Renzo) confirmed via duplicate Issue \#571](https://github.com/code-423n4/2024-04-renzo-findings/issues/571#event-12785930232)**

**[Renzo mitigated](https://github.com/code-423n4/2024-06-renzo-mitigation?tab=readme-ov-file#scope)**

**Status:** Mitigation confirmed. Full details in reports from [0xCiphky](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/10), [grearlake](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/56), [Fassi\_Security](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/42), [Bauchibred](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/19), and [LessDupes](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/4).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Renzo |
| Report Date | N/A |
| Finders | blutorque, kennedy1030, KupiaSec, 0x73696d616f, ilchovski, zzykxx, LessDupes |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-renzo
- **GitHub**: https://github.com/code-423n4/2024-04-renzo-findings/issues/368
- **Contest**: https://code4rena.com/reports/2024-04-renzo

### Keywords for Search

`vulnerability`

