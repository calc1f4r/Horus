---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: accounting
vulnerability_type: exchange_rate_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - exchange_rate_manipulation
  - exchange_rate_stale
  - exchange_rate_calculation_error
  - share_price_inflation
  - conversion_rounding
  - rate_update_missing
  - donation_attack
  - rate_during_slash

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - accounting
  - exchange_rate
  - share_price
  - rate_manipulation
  - stale_rate
  - donation_attack
  - share_inflation
  - conversion_rounding
  - rate_update
  
language: go
version: all
---

## References
- [discrepancy-between-health-calculation-and-slashable-collateral-computation.md](../../../../reports/cosmos_cometbft_findings/discrepancy-between-health-calculation-and-slashable-collateral-computation.md)
- [h-01-possible-arbitrage-from-chainlink-price-discrepancy.md](../../../../reports/cosmos_cometbft_findings/h-01-possible-arbitrage-from-chainlink-price-discrepancy.md)
- [h-07-exchange-rate-implementation-not-used-in-token-operations.md](../../../../reports/cosmos_cometbft_findings/h-07-exchange-rate-implementation-not-used-in-token-operations.md)
- [h-08-exchange-rate-calculation-is-incorrect.md](../../../../reports/cosmos_cometbft_findings/h-08-exchange-rate-calculation-is-incorrect.md)
- [eigen2-14-stake-deviations-due-to-addingremoving-strategy-may-allow-for-ejector-.md](../../../../reports/cosmos_cometbft_findings/eigen2-14-stake-deviations-due-to-addingremoving-strategy-may-allow-for-ejector-.md)
- [m-17-strategy-in-stakervaultsol-can-steal-more-rewards-even-though-its-designed-.md](../../../../reports/cosmos_cometbft_findings/m-17-strategy-in-stakervaultsol-can-steal-more-rewards-even-though-its-designed-.md)
- [missing-slashing-check.md](../../../../reports/cosmos_cometbft_findings/missing-slashing-check.md)
- [m-23-rounding-errors-can-cause-erc20rebasedistributor-transfers-and-mints-to-fai.md](../../../../reports/cosmos_cometbft_findings/m-23-rounding-errors-can-cause-erc20rebasedistributor-transfers-and-mints-to-fai.md)
- [m-5-daigohm-exchange-rate-may-be-stale.md](../../../../reports/cosmos_cometbft_findings/m-5-daigohm-exchange-rate-may-be-stale.md)
- [users-may-be-able-to-borrow-sweth-at-an-outdated-price.md](../../../../reports/cosmos_cometbft_findings/users-may-be-able-to-borrow-sweth-at-an-outdated-price.md)

## Vulnerability Title

**Exchange Rate and Share Price Vulnerabilities**

### Overview

This entry documents 5 distinct vulnerability patterns extracted from 10 audit reports (4 HIGH, 6 MEDIUM severity) across 9 protocols by 7 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Rate Update Missing

**Frequency**: 3/10 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Kelp DAO, Eigenlayer, Backd

This bug report discusses a problem in the StakeRegistry contract where the `updateOperatorsStake()` function is not updating all operators' stakes immediately after a strategy is added or removed from a quorum. This can lead to unfair competition and manipulation by the ejector role. The suggested 

**Example 1.1** [MEDIUM] — Eigenlayer
Source: `eigen2-14-stake-deviations-due-to-addingremoving-strategy-may-allow-for-ejector-.md`
```solidity
// ❌ VULNERABLE: Rate Update Missing
(uint96[] memory stakeWeights, bool[] memory hasMinimumStakes) =
    _weightOfOperatorsForQuorum(quorumNumber, operators);

int256 totalStakeDelta = 0;
// If the operator no longer meets the minimum stake, set their stake to zero and mark them for removal
/// also handle setting the operator's stake to 0 and remove them from the quorum
for (uint256 i = 0; i < operators.length; i++) {
    if (!hasMinimumStakes[i]) {
        stakeWeights[i] = 0;
        shouldBeDeregistered[i] = true;
    }

    // Update the operator's stake and retrieve the delta
    // If we're deregistering them, their weight is set to 0
    int256 stakeDelta = _recordOperatorStakeUpdate({
        operatorId: operatorIds[i],
        quorumNumber: quorumNumber,
        newStake: stakeWeights[i]
    });

    totalStakeDelt
```

**Example 1.2** [HIGH] — Kelp DAO
Source: `h-01-possible-arbitrage-from-chainlink-price-discrepancy.md`
```solidity
// ❌ VULNERABLE: Rate Update Missing
*   `test_DepositAsset()`:
        *
```

#### Pattern 2: Exchange Rate Calculation Error

**Frequency**: 3/10 reports | **Severity**: HIGH | **Validation**: Moderate (2 auditors)
**Protocols affected**: Kinetiq_2025-02-26, Kakeru Contracts

The `StakingManager` contract has a bug that affects the exchange rate between HYPE and kHYPE tokens. This bug can cause incorrect token accounting and value loss for users. The contract has a function called `getExchangeRatio()` that calculates the exchange rate based on various factors, but this r

**Example 2.1** [HIGH] — Kinetiq_2025-02-26
Source: `h-07-exchange-rate-implementation-not-used-in-token-operations.md`
```solidity
// ❌ VULNERABLE: Exchange Rate Calculation Error
kHYPE.mint(msg.sender, msg.value);
```

**Example 2.2** [HIGH] — Kinetiq_2025-02-26
Source: `h-07-exchange-rate-implementation-not-used-in-token-operations.md`
```solidity
// ❌ VULNERABLE: Exchange Rate Calculation Error
function stake() external payable nonReentrant whenNotPaused {
    // ... existing validation code ...

    uint256 kHYPEAmount = HYPEToKHYPE(msg.value);
    totalStaked += msg.value;
    kHYPE.mint(msg.sender, kHYPEAmount);
}
```

#### Pattern 3: Exchange Rate Stale

**Frequency**: 2/10 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Ion Protocol Audit, Cooler

This bug report is about an issue (M-5) found in the code of the "2023-01-cooler-judging" project on GitHub. The issue involves the DAI/gOHM exchange rate, which is currently hard-coded in the code and could become stale. This could lead to under-collateralized loans being given, and borrowers takin

**Example 3.1** [MEDIUM] — Cooler
Source: `m-5-daigohm-exchange-rate-may-be-stale.md`
```solidity
// ❌ VULNERABLE: Exchange Rate Stale
// File: src/aux/ClearingHouse.sol : ClearingHouse.maxLTC   #1

34:@>     uint256 public constant maxLTC = 2_500 * 1e18; // 2,500
```

**Example 3.2** [MEDIUM] — Cooler
Source: `m-5-daigohm-exchange-rate-may-be-stale.md`
```solidity
// ❌ VULNERABLE: Exchange Rate Stale
// File: src/Cooler.sol : Cooler.collateralFor()   #2

236        function collateralFor(uint256 amount, uint256 loanToCollateral) public pure returns (uint256) {
237 @>         return amount * decimals / loanToCollateral;
238:       }
```

#### Pattern 4: Rate During Slash

**Frequency**: 1/10 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: CAP Labs Covered Agent Protocol

This bug report highlights a problem with the protocol where there is a discrepancy between how an agent's health is calculated and how their collateral is determined to be slashable. This could lead to the protocol absorbing losses during liquidation events, which goes against the intended security

**Example 4.1** [HIGH] — CAP Labs Covered Agent Protocol
Source: `discrepancy-between-health-calculation-and-slashable-collateral-computation.md`
```solidity
// ❌ VULNERABLE: Rate During Slash
function slashTimestamp(address _agent) public view returns (uint48 _slashTimestamp) {
    DelegationStorage storage $ = getDelegationStorage();
    _slashTimestamp = uint48(Math.max((epoch() - 1) * $.epochDuration, $.agentData[_agent].lastBorrow));
}
```

**Example 4.2** [HIGH] — CAP Labs Covered Agent Protocol
Source: `discrepancy-between-health-calculation-and-slashable-collateral-computation.md`
```solidity
// ❌ VULNERABLE: Rate During Slash
function coverage(address _agent) public view returns (uint256 delegation) {
    NetworkMiddlewareStorage storage $ = getNetworkMiddlewareStorage();
    ...
    uint48 _timestamp = uint48(block.timestamp);
    for (uint256 i = 0; i < _vaults.length; i++) {
        (uint256 value,) = coverageByVault(_network, _agent, _vaults[i], _oracle, _timestamp);
        delegation += value;
    }
}
```

#### Pattern 5: Conversion Rounding

**Frequency**: 1/10 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Ethereum Credit Guild

This bug report discusses a vulnerability found in the ERC20RebaseDistributor smart contract. The vulnerability is caused by rounding errors during token transfers, which can result in the transfer failing. This can be exploited to disrupt sensitive operations such as liquidations. The bug is caused

**Example 5.1** [MEDIUM] — Ethereum Credit Guild
Source: `m-23-rounding-errors-can-cause-erc20rebasedistributor-transfers-and-mints-to-fai.md`
```solidity
// ❌ VULNERABLE: Conversion Rounding
It is possible that due to rounding, `rebasingStateTo.nShares` is higher than `toSharesAfter` by `1 wei`, causing the transfer to fail.

A similar issue can happen when unminted rewards are taken off the rebase pool:
```

**Example 5.2** [MEDIUM] — Ethereum Credit Guild
Source: `m-23-rounding-errors-can-cause-erc20rebasedistributor-transfers-and-mints-to-fai.md`
```solidity
// ❌ VULNERABLE: Conversion Rounding
Here it is possible that the `amount` is higher than `_unmintedRebaseRewards`, introducing also in this place a revert condition.

### Impact

Transfers and mints from or towards addresses that are rebasing may fail in real-world scenarios. This failure can be used as a means to DoS sensitive operations like liquidations. Addresses who enter this scenario aren't also able to exit rebase to fix their transfers.

### Proof of Concept

Below a foundry PoC (full setup [here](https://gist.github.com/3docSec/a54c62acdcf2f7bf0a532ff8e0aab805)) which shows a scenario where a transfer (or mint) to a rebasing user can fail by underflow on the `_unmintedRebaseRewards - amount` operation:
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
- Unique protocols affected: 9
- Independent audit firms: 7
- Patterns with 3+ auditor validation (Strong): 0

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

> `exchange-rate`, `share-price`, `rate-manipulation`, `stale-rate`, `donation-attack`, `share-inflation`, `conversion-rounding`, `rate-update`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
