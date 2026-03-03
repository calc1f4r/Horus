---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: rewards
vulnerability_type: reward_calculation_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - reward_amount_incorrect
  - reward_per_share_error
  - accumulated_reward_error
  - delayed_balance_reward
  - decimal_mismatch_reward
  - btc_delegation_reward
  - weight_based_reward_error
  - historical_reward_loss

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - rewards
  - reward_calculation
  - staking_rewards
  - reward_per_share
  - reward_rate
  - accumulated_rewards
  - reward_distribution
  - decimal_mismatch
  
language: go
version: all
---

## References
- [future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md](../../../../reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md)
- [linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md](../../../../reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md)
- [missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md](../../../../reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md)
- [modification-of-time-unit.md](../../../../reports/cosmos_cometbft_findings/modification-of-time-unit.md)
- [node-operators-can-claim-rpl-stake-without-running-a-node.md](../../../../reports/cosmos_cometbft_findings/node-operators-can-claim-rpl-stake-without-running-a-node.md)
- [unmetered-balance-iteration-in-reward-termination-can-be-exploited-to-permission.md](../../../../reports/cosmos_cometbft_findings/unmetered-balance-iteration-in-reward-termination-can-be-exploited-to-permission.md)
- [updating-of-wsx-staking-proxy-or-validator-may-lead-to-the-loss-of-funds.md](../../../../reports/cosmos_cometbft_findings/updating-of-wsx-staking-proxy-or-validator-may-lead-to-the-loss-of-funds.md)
- [zeeve-admin-could-drain-validatorrewarder-by-abusing-off-chain-bls-validation-du.md](../../../../reports/cosmos_cometbft_findings/zeeve-admin-could-drain-validatorrewarder-by-abusing-off-chain-bls-validation-du.md)
- [locked-in-licenses-can-be-transferred.md](../../../../reports/cosmos_cometbft_findings/locked-in-licenses-can-be-transferred.md)
- [lack-of-input-validation.md](../../../../reports/cosmos_cometbft_findings/lack-of-input-validation.md)
- [lack-of-liquidity-inside-stakingmanager.md](../../../../reports/cosmos_cometbft_findings/lack-of-liquidity-inside-stakingmanager.md)
- [m-03-dos-of-staking-due-to-unguarded-receiver-lock-period.md](../../../../reports/cosmos_cometbft_findings/m-03-dos-of-staking-due-to-unguarded-receiver-lock-period.md)
- [m-05-admin-can-break-all-functionality-through-weth-address.md](../../../../reports/cosmos_cometbft_findings/m-05-admin-can-break-all-functionality-through-weth-address.md)
- [m-09-there-is-no-mechanism-that-prevents-from-minting-less-than-eslbr-maximum-su.md](../../../../reports/cosmos_cometbft_findings/m-09-there-is-no-mechanism-that-prevents-from-minting-less-than-eslbr-maximum-su.md)
- [m-17-nodeop-can-get-rewards-even-if-there-was-an-error-in-registering-the-node-a.md](../../../../reports/cosmos_cometbft_findings/m-17-nodeop-can-get-rewards-even-if-there-was-an-error-in-registering-the-node-a.md)
- [m-27-faulty-escrow-config-will-lock-up-reward-tokens-in-staking-contract.md](../../../../reports/cosmos_cometbft_findings/m-27-faulty-escrow-config-will-lock-up-reward-tokens-in-staking-contract.md)
- [m-6-validatormaxstake-can-be-bypassed-by-using-setvalidatoraddress.md](../../../../reports/cosmos_cometbft_findings/m-6-validatormaxstake-can-be-bypassed-by-using-setvalidatoraddress.md)

## Vulnerability Title

**Staking Reward Calculation Vulnerabilities**

### Overview

This entry documents 5 distinct vulnerability patterns extracted from 24 audit reports (9 HIGH, 15 MEDIUM severity) across 21 protocols by 14 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Reward Per Share Error

**Frequency**: 18/24 reports | **Severity**: MEDIUM | **Validation**: Strong (13 auditors)
**Protocols affected**: MilkyWay, Covalent, Popcorn, Across Token and Token Distributor Audit, Hubble Farms

The `AvalancheL1Middleware::calcAndCacheStakes` function in the Suzaku network has a bug where it does not check if the epoch provided is in the future. This allows attackers to manipulate reward calculations by locking in current stake values for future epochs. This can lead to inflated reward shar

**Example 1.1** [HIGH] — Suzaku Core
Source: `future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md`
```solidity
// ❌ VULNERABLE: Reward Per Share Error
function calcAndCacheStakes(uint48 epoch, uint96 assetClassId) public returns (uint256 totalStake) {
    uint48 epochStartTs = getEpochStartTs(epoch); // No validation of epoch timing
    // ... rest of function caches values for any epoch, including future ones
}
```

**Example 1.2** [HIGH] — Suzaku Core
Source: `future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md`
```solidity
// ❌ VULNERABLE: Reward Per Share Error
function getOperatorStake(
    address operator,
    uint48 epoch,
    uint96 assetClassId
) public view returns (uint256 stake) {
    if (totalStakeCached[epoch][assetClassId]) {
        uint256 cachedStake = operatorStakeCache[epoch][assetClassId][operator];
        return cachedStake;
    }
    ...
}
```

#### Pattern 2: Weight Based Reward Error

**Frequency**: 2/24 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: FCHAIN Validator and Staking Contracts Audit, 0x v3 Staking

The report discusses a bug in the FCHAIN smart contract system. It states that to become a validator, one must possess an FNode license and lock it into the StakeManager contract. Both validators and delegators can lock their licenses using a function called `_lockLicenses`. However, this function d

**Example 2.1** [MEDIUM] — 0x v3 Staking
Source: `mixinparamssetparams-bypasses-safety-checks-made-by-standard-stakingproxy-upgrad.md`
```solidity
// ❌ VULNERABLE: Weight Based Reward Error
/// @dev Detach the current staking contract.
	/// Note that this is callable only by an authorized address.
	function detachStakingContract()
	    external
	    onlyAuthorized
	{
	    stakingContract = NIL\_ADDRESS;
	    emit StakingContractDetachedFromProxy();
	}
```

**Example 2.2** [MEDIUM] — 0x v3 Staking
Source: `mixinparamssetparams-bypasses-safety-checks-made-by-standard-stakingproxy-upgrad.md`
```solidity
// ❌ VULNERABLE: Weight Based Reward Error
/// @dev Attach a staking contract; future calls will be delegated to the staking contract.
	/// Note that this is callable only by an authorized address.
	/// @param \_stakingContract Address of staking contract.
	function attachStakingContract(address \_stakingContract)
	    external
	    onlyAuthorized
	{
	    \_attachStakingContract(\_stakingContract);
	}
```

#### Pattern 3: Reward Amount Incorrect

**Frequency**: 2/24 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: GoGoPool, Suzaku Core

A bug has been identified in the code of the GoGoPool project, which could cause rewards to be distributed wrongly between node runners and malicious node runners can bypass the required time for running nodes during the reward cycle to be eligible for rewards. This bug is located in the MinipoolMan

**Example 3.1** [MEDIUM] — GoGoPool
Source: `m-10-functions-cancelminipool-doesnt-reset-the-value-of-the-rewardsstarttime-for.md`
```solidity
// ❌ VULNERABLE: Reward Amount Incorrect
function cancelMinipool(address nodeID) external nonReentrant {
		Staking staking = Staking(getContractAddress("Staking"));
		ProtocolDAO dao = ProtocolDAO(getContractAddress("ProtocolDAO"));
		int256 index = requireValidMinipool(nodeID);
		onlyOwner(index);
		// make sure they meet the wait period requirement
		if (block.timestamp - staking.getRewardsStartTime(msg.sender) < dao.getMinipoolCancelMoratoriumSeconds()) {
			revert CancellationTooEarly();
		}
		_cancelMinipoolAndReturnFunds(nodeID, index);
	}

	function _cancelMinipoolAndReturnFunds(address nodeID, int256 index) private {
		requireValidStateTransition(index, MinipoolStatus.Canceled);
		setUint(keccak256(abi.encodePacked("minipool.item", index, ".status")), uint256(MinipoolStatus.Canceled));

		address owner = getAddress(keccak
```

**Example 3.2** [MEDIUM] — Suzaku Core
Source: `rewards-distribution-dos-due-to-uncached-secondary-asset-classes.md`
```solidity
// ❌ VULNERABLE: Reward Amount Incorrect
function _calculateOperatorShare(uint48 epoch, address operator) internal {
  // code..

  uint96[] memory assetClasses = l1Middleware.getAssetClassIds();
  for (uint256 i = 0; i < assetClasses.length; i++) {
       uint256 totalStake = l1Middleware.totalStakeCache(epoch, assetClasses[i]); //@audit directly accesses totalStakeCache
  }
}
```

#### Pattern 4: Decimal Mismatch Reward

**Frequency**: 1/24 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Kwenta Staking Rewards Upgrade

This bug report discusses an issue found by several individuals where the lower precision of USDC and frequent reward updates in the Kwenta staking contracts could potentially result in stakers receiving 0 of the allotted 10K USDC weekly rewards. This is due to a mistake in using the same reward cal

**Example 4.1** [MEDIUM] — Kwenta Staking Rewards Upgrade
Source: `m-1-attacker-will-prevent-distribution-of-usdc-to-stakers-through-frequent-rewar.md`
```solidity
// ❌ VULNERABLE: Decimal Mismatch Reward
((lastTimeRewardApplicable() - lastUpdateTime) * rewardRateUSDC * 1e18) / allTokensStaked
```

**Example 4.2** [MEDIUM] — Kwenta Staking Rewards Upgrade
Source: `m-1-attacker-will-prevent-distribution-of-usdc-to-stakers-through-frequent-rewar.md`
```solidity
// ❌ VULNERABLE: Decimal Mismatch Reward
(6 * rewardRateUSDC * 1e18) / allTokensStaked
```

#### Pattern 5: Historical Reward Loss

**Frequency**: 1/24 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Lido

This bug report is about a problem with the Lido platform, where a portion of staking rewards are distributed as a fee to the staking node operators. When rewards are distributed, an integer division is done which results in a small remainder that stays with the NodeOperatorRegistry. This remainder 

**Example 5.1** [MEDIUM] — Lido
Source: `node-operator-rewards-unevenly-leaked.md`
```solidity
// ❌ VULNERABLE: Historical Reward Loss
uint256 perValReward = _totalReward.div(effectiveStakeTotal);
```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 9 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 24
- HIGH severity: 9 (37%)
- MEDIUM severity: 15 (62%)
- Unique protocols affected: 21
- Independent audit firms: 14
- Patterns with 3+ auditor validation (Strong): 1

### Detection Patterns

#### Code Patterns to Look For
```
- Missing balance update before/after token transfers
- Unchecked return values from staking/delegation operations
- State reads without freshness validation
- Arithmetic operations without overflow/precision checks
- Missing access control on state-modifying functions
- Linear iterations over unbounded collections
- Race condition windows in multi-step operations
```

#### Audit Checklist
- [ ] Verify all staking state transitions update balances atomically
- [ ] Check that slashing affects all relevant state (pending, queued, active)
- [ ] Ensure withdrawal requests cannot bypass cooldown periods
- [ ] Validate that reward calculations handle all edge cases (zero stake, partial periods)
- [ ] Confirm access control on all administrative and state-modifying functions
- [ ] Test for frontrunning vectors in all two-step operations
- [ ] Verify iteration bounds on all loops processing user-controlled data
- [ ] Check cross-module state consistency after complex operations

### Keywords for Search

> `reward-calculation`, `staking-rewards`, `reward-per-share`, `reward-rate`, `accumulated-rewards`, `reward-distribution`, `decimal-mismatch`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
