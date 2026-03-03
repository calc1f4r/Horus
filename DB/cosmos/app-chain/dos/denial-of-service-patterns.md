---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: dos
vulnerability_type: denial_of_service_patterns

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - function_reversion_dos
  - panic_crash_dos
  - frontrun_dos
  - dust_amount_dos
  - reentrancy_dos
  - external_call_dos
  - permission_dos
  - upgrade_dos

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - dos
  - denial_of_service
  - DoS
  - revert
  - panic
  - crash
  - griefing
  - frontrun_DoS
  - dust_amount
  
language: go
version: all
---

## References
- [dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md](../../../../reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md)
- [h-03-a-dos-on-snapshots-due-to-a-rounding-error-in-calculations.md](../../../../reports/cosmos_cometbft_findings/h-03-a-dos-on-snapshots-due-to-a-rounding-error-in-calculations.md)
- [h-06-bond-operations-will-always-revert-at-certain-time-when-putoptionsrequired-.md](../../../../reports/cosmos_cometbft_findings/h-06-bond-operations-will-always-revert-at-certain-time-when-putoptionsrequired-.md)
- [h-10-lientokenbuyoutlien-will-always-revert.md](../../../../reports/cosmos_cometbft_findings/h-10-lientokenbuyoutlien-will-always-revert.md)
- [h-2-the-notional-version-of-lend-can-be-used-to-lock-ipts.md](../../../../reports/cosmos_cometbft_findings/h-2-the-notional-version-of-lend-can-be-used-to-lock-ipts.md)
- [h-3-adversary-can-brick-autoroller-by-creating-another-autoroller-on-the-same-ad.md](../../../../reports/cosmos_cometbft_findings/h-3-adversary-can-brick-autoroller-by-creating-another-autoroller-on-the-same-ad.md)
- [h-4-adversary-can-permanently-break-percentage-tier-bounties-by-funding-certain-.md](../../../../reports/cosmos_cometbft_findings/h-4-adversary-can-permanently-break-percentage-tier-bounties-by-funding-certain-.md)
- [h-5-committoliens-always-reverts.md](../../../../reports/cosmos_cometbft_findings/h-5-committoliens-always-reverts.md)
- [malicious-target-can-make-_endvote-revert-forever-by-forceunstakingstaking-again.md](../../../../reports/cosmos_cometbft_findings/malicious-target-can-make-_endvote-revert-forever-by-forceunstakingstaking-again.md)
- [minting-limit-calculation-may-prevent-legitimate-claims.md](../../../../reports/cosmos_cometbft_findings/minting-limit-calculation-may-prevent-legitimate-claims.md)
- [h-03-executerequests-are-not-properly-removed-from-the-context-queue.md](../../../../reports/cosmos_cometbft_findings/h-03-executerequests-are-not-properly-removed-from-the-context-queue.md)
- [execution-of-stake-and-unstake-operations-blocked-due-to-uninitialized-_methods-.md](../../../../reports/cosmos_cometbft_findings/execution-of-stake-and-unstake-operations-blocked-due-to-uninitialized-_methods-.md)
- [m-01-changing-the-slashinghandler-for-nativevaults-will-dos-slashing.md](../../../../reports/cosmos_cometbft_findings/m-01-changing-the-slashinghandler-for-nativevaults-will-dos-slashing.md)
- [m-01-in-edge-cases-create_pool-can-either-be-reverted-or-allow-user-underpay-fee.md](../../../../reports/cosmos_cometbft_findings/m-01-in-edge-cases-create_pool-can-either-be-reverted-or-allow-user-underpay-fee.md)
- [m-01-the-increasestakeandlock-function-prevents-users-from-increasing-stake-amou.md](../../../../reports/cosmos_cometbft_findings/m-01-the-increasestakeandlock-function-prevents-users-from-increasing-stake-amou.md)
- [m-02-ve3drewardpoolsol-is-incompatible-with-balvebal.md](../../../../reports/cosmos_cometbft_findings/m-02-ve3drewardpoolsol-is-incompatible-with-balvebal.md)
- [m-15-redeemersetfee-function-will-always-revert.md](../../../../reports/cosmos_cometbft_findings/m-15-redeemersetfee-function-will-always-revert.md)
- [m-6-astariaroutercommittoliens-will-revert-if-the-protocol-fee-is-enabled.md](../../../../reports/cosmos_cometbft_findings/m-6-astariaroutercommittoliens-will-revert-if-the-protocol-fee-is-enabled.md)
- [m-8-malicious-peer-can-cause-a-syncing-node-to-panic-during-blocksync.md](../../../../reports/cosmos_cometbft_findings/m-8-malicious-peer-can-cause-a-syncing-node-to-panic-during-blocksync.md)

## Vulnerability Title

**General Denial of Service Attack Patterns**

### Overview

This entry documents 4 distinct vulnerability patterns extracted from 19 audit reports (11 HIGH, 8 MEDIUM severity) across 16 protocols by 5 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Function Reversion Dos

**Frequency**: 16/19 reports | **Severity**: HIGH | **Validation**: Strong (5 auditors)
**Protocols affected**: Sense, Dopex, Qoda DAO, Astaria, OpenQ

The `VeQoda` contract has a bug where it is not properly initialized with valid entries for its `_methodInfo` mapping. This causes calls to the `stake` and `unstake` functions to fail, as they try to call the `safeTransferFrom` function in the default value for uninitialized variables, `address(0)`.

**Example 1.1** [MEDIUM] — Qoda DAO
Source: `execution-of-stake-and-unstake-operations-blocked-due-to-uninitialized-_methods-.md`
```solidity
// ❌ VULNERABLE: Function Reversion Dos
function stake(address account, bytes32 method, uint256 amount) external {
        if (amount <= 0) {
            revert CustomErrors.ZeroStakeAmount();
        }

        // Calculate unclaimed reward before balance update
        _updateReward(account);

        // if user exists, first update their cached veToken balance
        if (_users.contains(account)) {
            _updateVeTokenCache(account);
        }

        // Do token transfer from user to contract
        address token = _methodInfo[method].token;
        IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
```

**Example 1.2** [MEDIUM] — Qoda DAO
Source: `execution-of-stake-and-unstake-operations-blocked-due-to-uninitialized-_methods-.md`
```solidity
// ❌ VULNERABLE: Function Reversion Dos
function unstake(bytes32 method, uint256 amount) external {
        if (amount <= 0) {
            revert CustomErrors.ZeroUnstakeAmount();
        }

        // User cannot over-unstake
        if (_userInfo[msg.sender][method].amount < amount) {
            revert CustomErrors.InsufficientBalance();
        }
```

#### Pattern 2: Dust Amount Dos

**Frequency**: 1/19 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Suzaku Core

The bug report describes a vulnerability in the `forceUpdateNodes()` function that can be exploited by an attacker. By using a small `limitStake` value, the attacker can force all validator nodes into a pending update state, effectively blocking legitimate rebalancing for the entire epoch. This can 

#### Pattern 3: External Call Dos

**Frequency**: 1/19 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Initia

The `minievm` cosmos precompile allows a Solidity contract to dispatch a Cosmos SDK message, which is executed after the EVM call is successfully executed. This can be done by calling the cosmos precompile with specific function selectors and passing the encoded message. However, there is a bug wher

**Example 3.1** [HIGH] — Initia
Source: `h-03-executerequests-are-not-properly-removed-from-the-context-queue.md`
```solidity
// ❌ VULNERABLE: External Call Dos
287: messages := ctx.Value(types.CONTEXT_KEY_EXECUTE_REQUESTS).(*[]types.ExecuteRequest)
288: *messages = append(*messages, types.ExecuteRequest{
289: 	Caller: caller,
290: 	Msg:    sdkMsg,
291:
292: 	AllowFailure: executeCosmosArguments.Options.AllowFailure,
293: 	CallbackId:   executeCosmosArguments.Options.CallbackId,
294: })
```

**Example 3.2** [HIGH] — Initia
Source: `h-03-executerequests-are-not-properly-removed-from-the-context-queue.md`
```solidity
// ❌ VULNERABLE: External Call Dos
347: // handle cosmos execute requests
348: requests := sdkCtx.Value(types.CONTEXT_KEY_EXECUTE_REQUESTS).(*[]types.ExecuteRequest)
349: if dispatchLogs, err := k.dispatchMessages(sdkCtx, *requests); err != nil {
350: 	return nil, nil, err
351: } else {
352: 	logs = append(logs, dispatchLogs...)
353: }
```

#### Pattern 4: Panic Crash Dos

**Frequency**: 1/19 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Allora

This bug report discusses a vulnerability found in the system's use of a vulnerable version of CometBFT. This vulnerability, known as GO-2024-2951, allows an attacker to cause a panic during blocksync, which can lead to a denial of service (DoS) attack on the network. The vulnerability is present in


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 11 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 19
- HIGH severity: 11 (57%)
- MEDIUM severity: 8 (42%)
- Unique protocols affected: 16
- Independent audit firms: 5
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

> `denial-of-service`, `DoS`, `revert`, `panic`, `crash`, `griefing`, `frontrun-DoS`, `dust-amount`, `permanent-revert`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
