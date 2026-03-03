---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: accounting
vulnerability_type: balance_tracking_errors

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - balance_not_updated
  - balance_desynchronization
  - double_counting
  - tvl_calculation_error
  - accounting_state_corruption
  - missing_deduction
  - cross_module_accounting
  - pending_amount_tracking

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - accounting
  - balance_tracking
  - state_desynchronization
  - accounting_error
  - double_counting
  - TVL_calculation
  - state_corruption
  - missing_update
  
language: go
version: all
---

## References
- [h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md](../../../../reports/cosmos_cometbft_findings/h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md)
- [h-8-yield-swivel-element-apwine-and-sense-lend-are-subject-to-reentracy-resultin.md](../../../../reports/cosmos_cometbft_findings/h-8-yield-swivel-element-apwine-and-sense-lend-are-subject-to-reentracy-resultin.md)
- [rocketminipooldelegateold-node-operator-may-reenter-finalise-to-manipulate-accou.md](../../../../reports/cosmos_cometbft_findings/rocketminipooldelegateold-node-operator-may-reenter-finalise-to-manipulate-accou.md)
- [h-9-public-vaults-can-become-insolvent-because-of-missing-yintercept-update.md](../../../../reports/cosmos_cometbft_findings/h-9-public-vaults-can-become-insolvent-because-of-missing-yintercept-update.md)
- [dos-in-cometbft-block-sync-githubcomcometbftcometbftblocksync.md](../../../../reports/cosmos_cometbft_findings/dos-in-cometbft-block-sync-githubcomcometbftcometbftblocksync.md)
- [m-5-changing-the-epoch-duration-will-completely-break-the-vault-and-the-slashers.md](../../../../reports/cosmos_cometbft_findings/m-5-changing-the-epoch-duration-will-completely-break-the-vault-and-the-slashers.md)
- [missing-validation-that-ensures-unspent-btc-is-fully-sent-back-as-change-in-lomb.md](../../../../reports/cosmos_cometbft_findings/missing-validation-that-ensures-unspent-btc-is-fully-sent-back-as-change-in-lomb.md)
- [incorrect-inclusion-of-removed-nodes-in-_requireminsecondaryassetclasses-during-.md](../../../../reports/cosmos_cometbft_findings/incorrect-inclusion-of-removed-nodes-in-_requireminsecondaryassetclasses-during-.md)
- [m-01-bonding-weth-discounts-can-drain-weth-reserves-of-rdpxv2core-contract-to-ze.md](../../../../reports/cosmos_cometbft_findings/m-01-bonding-weth-discounts-can-drain-weth-reserves-of-rdpxv2core-contract-to-ze.md)
- [m-4-lack-of-slippage-control-for-issue-function.md](../../../../reports/cosmos_cometbft_findings/m-4-lack-of-slippage-control-for-issue-function.md)

## Vulnerability Title

**Balance and State Tracking Vulnerabilities**

### Overview

This entry documents 5 distinct vulnerability patterns extracted from 10 audit reports (4 HIGH, 6 MEDIUM severity) across 10 protocols by 6 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Balance Desynchronization

**Frequency**: 3/10 reports | **Severity**: MEDIUM | **Validation**: Strong (3 auditors)
**Protocols affected**: Shido, Symbiotic Relay, Althea Gravity Bridge

This bug report is about a potential issue in the Shido blockchain that could be caused by a malicious peer. The problem is that this peer could send a block with a very high LastCommit round, which could lead to excessive memory usage and crashes. This could disrupt the normal functioning of the bl

**Example 1.1** [HIGH] — Althea Gravity Bridge
Source: `h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md`
```solidity
// ❌ VULNERABLE: Balance Desynchronization
let mut all_valset_events = web3
    .check_for_events(
        end_search.clone(),
        Some(current_block.clone()),
        vec![gravity_contract_address],
        vec![VALSET_UPDATED_EVENT_SIG],
    )
    .await?;
```

#### Pattern 2: Double Counting

**Frequency**: 2/10 reports | **Severity**: HIGH | **Validation**: Moderate (2 auditors)
**Protocols affected**: Rocket Pool Atlas (v1.2), Illuminate

This bug report is about the reentrancy vulnerability in Yield, Swivel, Element, APWine and Sense lend() functions of the Lender. These functions use balance difference for the net result calculation, i.e. how much Illuminate PTs to mint for the caller, and call user-provided contract to perform the

**Example 2.1** [HIGH] — Illuminate
Source: `h-8-yield-swivel-element-apwine-and-sense-lend-are-subject-to-reentracy-resultin.md`
```solidity
// ❌ VULNERABLE: Double Counting
/// @notice swaps underlying premium via a Yield Space Pool
    /// @dev this method is only used by the Yield, Illuminate and Swivel protocols
    /// @param u address of an underlying asset
    /// @param y Yield Space Pool for the principal token
    /// @param a amount of underlying tokens to lend
    /// @param r the receiving address for PTs
    /// @param p the principal token in the Yield Space Pool
    /// @param m the minimum amount to purchase
    /// @return uint256 the amount of tokens sent to the Yield Space Pool
    function yield(
        address u,
        address y,
        uint256 a,
        address r,
        address p,
        uint256 m
    ) internal returns (uint256) {
        // Get the starting balance (to verify receipt of tokens)
        uint256 starting = IERC20
```

**Example 2.2** [HIGH] — Rocket Pool Atlas (v1.2)
Source: `rocketminipooldelegateold-node-operator-may-reenter-finalise-to-manipulate-accou.md`
```solidity
// ❌ VULNERABLE: Double Counting
finalise() --> 
  status == MinipoolStatus.Withdrawable  //<-- true
  withdrawalBlock > 0  //<-- true
  _finalise() -->
     !finalised  //<-- true
        _refund()
            nodeRefundBalance = 0  //<-- reset refund balance
              ---> extCall: nodeWithdrawalAddress
                     ---> reenter: finalise()
                        status == MinipoolStatus.Withdrawable  //<-- true
                        withdrawalBlock > 0  //<-- true
                        _finalise() -->
                             !finalised  //<-- true
                             nodeRefundBalance > 0  //<-- false; no refund()
                             address(this).balance to RETH
                             RocketTokenRETHInterface(rocketTokenRETH).depositExcessCollateral()
                     
```

#### Pattern 3: Missing Deduction

**Frequency**: 2/10 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Astaria, Lombard Finance

Issue H-9 is a bug report found by zzykxx and 0xRajeev that deals with the deduction of `yIntercept` during payments being missing in `beforePayment()`. `yIntercept` is declared as "sum of all LienToken amounts" and its value is used to calculate the total assets of a public vault. When this deducti

**Example 3.1** [HIGH] — Astaria
Source: `h-9-public-vaults-can-become-insolvent-because-of-missing-yintercept-update.md`
```solidity
// ❌ VULNERABLE: Missing Deduction
/**
   * @notice Hook to update the slope and yIntercept of the PublicVault on payment.
   * The rate for the LienToken is subtracted from the total slope of the PublicVault, and recalculated in afterPayment().
   * @param lienId The ID of the lien.
   * @param amount The amount paid off to deduct from the yIntercept of the PublicVault.
   */
```

#### Pattern 4: Pending Amount Tracking

**Frequency**: 2/10 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Dopex, Napier

This bug report focuses on a potential issue in the RdpxV2Core contract, which is part of the Dopex project. Depending on the reserves of rDPX, bonding discounts are given both on the rDPX and WETH collateral requirements for minting dpxETH. The issue with this is that the RdpxV2Core contract only f

**Example 4.1** [MEDIUM] — Dopex
Source: `m-01-bonding-weth-discounts-can-drain-weth-reserves-of-rdpxv2core-contract-to-ze.md`
```solidity
// ❌ VULNERABLE: Pending Amount Tracking
reserveAsset[reservesIndex["WETH"]].tokenBalance -= _amount / 2;
```

**Example 4.2** [MEDIUM] — Dopex
Source: `m-01-bonding-weth-discounts-can-drain-weth-reserves-of-rdpxv2core-contract-to-ze.md`
```solidity
// ❌ VULNERABLE: Pending Amount Tracking
function bond(
  uint256 _amount,
  uint256 rdpxBondId,
  address _to
) public returns (uint256 receiptTokenAmount) {
  _whenNotPaused();
  // Validate amount
  _validate(_amount > 0, 4);

  // Compute the bond cost
  (uint256 rdpxRequired, uint256 wethRequired) = calculateBondCost(
    _amount,
    rdpxBondId
  );
  ...
  // purchase options
  uint256 premium;
  if (putOptionsRequired) {
    premium = _purchaseOptions(rdpxRequired);
  }

  _transfer(rdpxRequired, wethRequired - premium, _amount, rdpxBondId);
  
  // Stake the ETH in the ReceiptToken contract
  receiptTokenAmount = _stake(_to, _amount);
  ...
}
```

#### Pattern 5: Accounting State Corruption

**Frequency**: 1/10 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Suzaku Core

The `_requireMinSecondaryAssetClasses` function is causing a problem in the `forceUpdateNodes` process. If a node is removed in the first iteration, the second iteration still includes the removed node in its calculations. This can lead to inaccurate evaluations and cause issues with node removal de

**Example 5.1** [MEDIUM] — Suzaku Core
Source: `incorrect-inclusion-of-removed-nodes-in-_requireminsecondaryassetclasses-during-.md`
```solidity
// ❌ VULNERABLE: Accounting State Corruption
if ((newStake < assetClasses[PRIMARY_ASSET_CLASS].minValidatorStake)
                    || !_requireMinSecondaryAssetClasses(0, operator)) {
      newStake = 0;
      _initializeEndValidationAndFlag(operator, valID, nodeId);
}
```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 4 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 10
- HIGH severity: 4 (40%)
- MEDIUM severity: 6 (60%)
- Unique protocols affected: 10
- Independent audit firms: 6
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

> `balance-tracking`, `state-desynchronization`, `accounting-error`, `double-counting`, `TVL-calculation`, `state-corruption`, `missing-update`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
