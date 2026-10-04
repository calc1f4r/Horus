---
# Core Classification
protocol: Eigenlayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53495
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-10-16-EigenLayer.md
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

[EIG-17] Operator or delegation approver have the power to censor delegated stakers

### Overview


The bug report describes a potential issue in the DelegationManager smart contract. The problem is that the operator or delegation approver, who has been delegated to by stakers, has the ability to censor certain stakers by undelegating them. This can be exploited by an attacker, who can create multiple operators and use them to undelegate stakers, causing instability in the protocol and discouraging users from using it.

The report also mentions that the staker must wait for a week before being able to delegate their shares to another operator. This delay should only be applied if the staker wants to withdraw their tokens, not when they want to claim back their shares.

The suggested solution is for stakers to claim back their shares immediately without waiting for the delay. The report has been acknowledged and the issue is being addressed. 

### Original Finding Content

**Severity:** Medium

**Path:** DelegationManager.sol:undelegate#L213-L257

**Description:**  

The operator or delegation approver that stakers have delegated to, have the power to selectively censor those stakers.

As soon as anyone can register an operator on EigenLayer, an attacker can create operators massively and grief stakers by undelegating them, consequently damaging protocol stability and making users averse to use the protocol.

The operator or delegation approver can call the `undelegate()` function for a particular staker. This will move the staker to the undelegation limbo (call to `forceIntoUndelegationLimbo()`) , and forcefully removing staker’s shares from `StartegyManager` (call to `forceTotalWithdrawal()`).

```    function undelegate(
        address staker
    ) external onlyWhenNotPaused(PAUSED_UNDELEGATION) returns (bytes32 withdrawalRoot) {
        require(isDelegated(staker), "DelegationManager.undelegate: staker must be delegated to undelegate");
        address operator = delegatedTo[staker];
        require(!isOperator(staker), "DelegationManager.undelegate: operators cannot be undelegated");
        require(staker != address(0), "DelegationManager.undelegate: cannot undelegate zero address");
        require(
            msg.sender == staker ||
                msg.sender == operator ||                                       // @audit
                msg.sender == _operatorDetails[operator].delegationApprover,    // @audit
            "DelegationManager.undelegate: caller cannot undelegate staker"
        );
        
        // remove any shares from the delegation system that the staker currently has delegated, if necessary
        // force the staker into "undelegation limbo" in the EigenPodManager if necessary
       if (eigenPodManager.podOwnerHasActiveShares(staker)) {
            uint256 podShares = eigenPodManager.forceIntoUndelegationLimbo(staker, operator); // @audit
            ...
        }
        // force-queue a withdrawal of all of the staker's shares from the StrategyManager, if necessary
        if (strategyManager.stakerStrategyListLength(staker) != 0) {
            IStrategy[] memory strategies;
            uint256[] memory strategyShares;
            (strategies, strategyShares, withdrawalRoot) = strategyManager.forceTotalWithdrawal(staker); // @audit
            ...
    }
```

The staker is able to delegate his shares to another operator only after `withdrawalDelayBlocks` period. Which is 1 week according to the documentation https://github.com/Layr-Labs/eigenlayer-contracts/blob/master/docs/core/StrategyManager.md#strategymanager.

```
    function exitUndelegationLimbo(
        uint256 middlewareTimesIndex,
        bool withdrawFundsFromEigenLayer
    ) external onlyWhenNotPaused(PAUSED_WITHDRAW_RESTAKED_ETH) onlyNotFrozen(msg.sender) nonReentrant {
        ...

        // enforce minimum delay lag
        require(
            limboStartBlock + strategyManager.withdrawalDelayBlocks() <= block.number,  // @audit
            "EigenPodManager.exitUndelegationLimbo: withdrawalDelayBlocks period has not yet passed"
        );
```
```
   function _completeQueuedWithdrawal(
        QueuedWithdrawal calldata queuedWithdrawal,
        IERC20[] calldata tokens,
        uint256 middlewareTimesIndex,
        bool receiveAsTokens
    ) internal onlyNotFrozen(queuedWithdrawal.delegatedAddress) {
       ...
        // enforce minimum delay lag
        require(
            queuedWithdrawal.withdrawalStartBlock + withdrawalDelayBlocks <= block.number,   // @audit
            "StrategyManager.completeQueuedWithdrawal: withdrawalDelayBlocks period has not yet passed"
        );
```
```
* uint withdrawalDelayBlocks:
    As of M2, this is 50400 (roughly 1 week) // @audit
    Stakers must wait this amount of time before a withdrawal can be completed
```
During 1 week period staker’s funds, including beacon chain staked ETH, and LSTs (cbETH, rETH, stETH), aren’t usable on EigenLayer.

**Remediation:**  The staker should claim back his shares immediately without waiting for the `withdrawalDelayBlocks`. Delay `withdrawalDelayBlocks` should be applied only if the staker withdraws their tokens (ETH or LSTs) back.

**Status:**   Acknowledged

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Eigenlayer |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-10-16-EigenLayer.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

