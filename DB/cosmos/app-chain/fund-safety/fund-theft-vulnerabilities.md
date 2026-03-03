---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: fund-safety
vulnerability_type: fund_theft_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - direct_theft_via_auth
  - theft_via_manipulation
  - theft_via_reentrancy
  - theft_via_share_price
  - theft_via_delegatecall
  - theft_via_replay
  - theft_via_frontrunning
  - surplus_balance_theft

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - fund_safety
  - fund_theft
  - drain
  - steal
  - unauthorized_withdrawal
  - reentrancy
  - delegatecall
  - replay_attack
  - frontrunning
  
language: go
version: all
---

## References
- [cvgt-staking-pool-state-manipulation.md](../../../../reports/cosmos_cometbft_findings/cvgt-staking-pool-state-manipulation.md)
- [h-3-tier-winner-can-steal-excess-funds-from-tiered-percentage-bounty-if-any-depo.md](../../../../reports/cosmos_cometbft_findings/h-3-tier-winner-can-steal-excess-funds-from-tiered-percentage-bounty-if-any-depo.md)
- [risk-of-tokenutoken-exchange-rate-manipulation.md](../../../../reports/cosmos_cometbft_findings/risk-of-tokenutoken-exchange-rate-manipulation.md)
- [the-pool-owner-can-manipulate-users-to-steal-all-of-their-stake-amounts-by-using.md](../../../../reports/cosmos_cometbft_findings/the-pool-owner-can-manipulate-users-to-steal-all-of-their-stake-amounts-by-using.md)
- [delegatecall-to-staking-precompile-allows-theft-of-all-staked-mon.md](../../../../reports/cosmos_cometbft_findings/delegatecall-to-staking-precompile-allows-theft-of-all-staked-mon.md)
- [h-04-hijacking-of-node-operators-minipool-causes-loss-of-staked-funds.md](../../../../reports/cosmos_cometbft_findings/h-04-hijacking-of-node-operators-minipool-causes-loss-of-staked-funds.md)
- [h-7-there-are-no-illuminate-pt-transfers-from-the-owner-in-erc5095s-withdraw-and.md](../../../../reports/cosmos_cometbft_findings/h-7-there-are-no-illuminate-pt-transfers-from-the-owner-in-erc5095s-withdraw-and.md)
- [lack-of-prioritization-of-oracle-messages.md](../../../../reports/cosmos_cometbft_findings/lack-of-prioritization-of-oracle-messages.md)
- [m-1-lack-of-on-chain-deviation-check-for-lst-can-lead-to-loss-of-assets.md](../../../../reports/cosmos_cometbft_findings/m-1-lack-of-on-chain-deviation-check-for-lst-can-lead-to-loss-of-assets.md)
- [m-5-malicious-or-compromised-admin-of-certain-lsts-could-manipulate-the-price.md](../../../../reports/cosmos_cometbft_findings/m-5-malicious-or-compromised-admin-of-certain-lsts-could-manipulate-the-price.md)
- [possible-signature-re-usage.md](../../../../reports/cosmos_cometbft_findings/possible-signature-re-usage.md)

## Vulnerability Title

**Direct Fund Theft and Drain Vulnerabilities**

### Overview

This entry documents 3 distinct vulnerability patterns extracted from 11 audit reports (7 HIGH, 4 MEDIUM severity) across 10 protocols by 7 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Theft Via Manipulation

**Frequency**: 8/11 reports | **Severity**: MEDIUM | **Validation**: Strong (5 auditors)
**Protocols affected**: Umee, Convergent, Tokemak, OpenQ, Moonscape

The report highlights a potential vulnerability in the CVGT staking state that can be exploited by manipulating the CVGT mint and CVGTStakingPoolState accounts. This allows attackers to set any CVGT on a poolstate and stability_pool_state, as well as spoof the CVGTStakingPoolState, potentially enabl

**Example 1.1** [HIGH] — Convergent
Source: `cvgt-staking-pool-state-manipulation.md`
```solidity
// ❌ VULNERABLE: Theft Via Manipulation
pub struct Initialize<'info> {
    #[account()]
    pub cvgt: Box<Account<'info, Mint>>,
}
```

**Example 1.2** [HIGH] — Convergent
Source: `cvgt-staking-pool-state-manipulation.md`
```solidity
// ❌ VULNERABLE: Theft Via Manipulation
pub fn config_pool_state_handler(ctx: Context<ConfigPoolState>) -> Result<()> {
    let pool_state = &mut ctx.accounts.pool_state;
    let cvgt_staking_state_key = ctx.accounts.cvgt_staking_state.key();
    pool_state.cvgt_staking_state = cvgt_staking_state_key;
    Ok(())
}
```

#### Pattern 2: Direct Theft Via Auth

**Frequency**: 2/11 reports | **Severity**: HIGH | **Validation**: Moderate (2 auditors)
**Protocols affected**: GoGoPool, Illuminate

A bug has been found in the GoGoPool smart contract, which allows anyone to hijack a minipool of any node operator that finished the validation period or had an error. This could lead to the node operator losing their staked funds, as well as the hacker gaining rewards without hosting a node.

The p

**Example 2.1** [HIGH] — GoGoPool
Source: `h-04-hijacking-of-node-operators-minipool-causes-loss-of-staked-funds.md`
```solidity
// ❌ VULNERABLE: Direct Theft Via Auth
function createMinipool(
		address nodeID,
		uint256 duration,
		uint256 delegationFee,
		uint256 avaxAssignmentRequest
	) external payable whenNotPaused {
---------
		// Create or update a minipool record for nodeID
		// If nodeID exists, only allow overwriting if node is finished or canceled
		// 		(completed its validation period and all rewards paid and processing is complete)
		int256 minipoolIndex = getIndexOf(nodeID);
		if (minipoolIndex != -1) {
			requireValidStateTransition(minipoolIndex, MinipoolStatus.Prelaunch);
			resetMinipoolData(minipoolIndex);
----------
		setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".status")), uint256(MinipoolStatus.Prelaunch));
----------
		setAddress(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".owner")), msg.send
```

**Example 2.2** [HIGH] — Illuminate
Source: `h-7-there-are-no-illuminate-pt-transfers-from-the-owner-in-erc5095s-withdraw-and.md`
```solidity
// ❌ VULNERABLE: Direct Theft Via Auth
/// @notice At or after maturity, burns exactly `shares` of Principal Tokens from `owner` and sends `assets` of underlying tokens to `receiver`. Before maturity, sends `assets` by selling `shares` of PT on a YieldSpace AMM.
    /// @param s The number of shares to be burned in exchange for the underlying asset
    /// @param r The receiver of the underlying tokens being withdrawn
    /// @param o Address of the owner of the shares being burned
    /// @return uint256 The amount of underlying tokens distributed by the redemption
    function redeem(
        uint256 s,
        address r,
        address o
    ) external override returns (uint256) {
        // Pre-maturity
        if (block.timestamp < maturity) {
            uint128 assets = Cast.u128(previewRedeem(s));
            // If own
```

#### Pattern 3: Theft Via Delegatecall

**Frequency**: 1/11 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Monad

This bug report discusses a critical risk issue found in a commit of a protocol. The staking precompile does not properly enforce the EVMC message kind, which can lead to malicious contracts stealing staked MON. The issue has been fixed in a later commit, but the report recommends enforcing `CALL` f


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 7 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 11
- HIGH severity: 7 (63%)
- MEDIUM severity: 4 (36%)
- Unique protocols affected: 10
- Independent audit firms: 7
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

> `fund-theft`, `drain`, `steal`, `unauthorized-withdrawal`, `reentrancy`, `delegatecall`, `replay-attack`, `frontrunning`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
