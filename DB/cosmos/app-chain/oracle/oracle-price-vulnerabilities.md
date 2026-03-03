---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: oracle
vulnerability_type: oracle_price_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - stale_price_data
  - price_manipulation_attack
  - oracle_dos
  - price_deviation_exploit
  - oracle_frontrunning
  - multi_oracle_inconsistency
  - oracle_stake_requirement
  - price_feed_reliability

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - oracle
  - oracle
  - price_feed
  - stale_price
  - manipulation
  - TWAP
  - deviation
  - frontrunning
  - Chainlink
  
language: go
version: all
---

## References
- [h-24-loans-can-exceed-the-maximum-potential-debt-leading-to-vault-insolvency-and.md](../../../../reports/cosmos_cometbft_findings/h-24-loans-can-exceed-the-maximum-potential-debt-leading-to-vault-insolvency-and.md)
- [malicious-user-can-prevent-other-users-from-unbonding-due-to-missing-input-valid.md](../../../../reports/cosmos_cometbft_findings/malicious-user-can-prevent-other-users-from-unbonding-due-to-missing-input-valid.md)
- [failure-to-enforce-minimum-oracle-stake-requirement.md](../../../../reports/cosmos_cometbft_findings/failure-to-enforce-minimum-oracle-stake-requirement.md)
- [h-2-users-can-frontrun-lstslrts-tokens-prices-decrease-in-order-to-avoid-losses.md](../../../../reports/cosmos_cometbft_findings/h-2-users-can-frontrun-lstslrts-tokens-prices-decrease-in-order-to-avoid-losses.md)
- [m-3-funding-rate-calculation-is-not-correct.md](../../../../reports/cosmos_cometbft_findings/m-3-funding-rate-calculation-is-not-correct.md)
- [m-6-the-rewards-distribution-in-the-nftpositionmanager-is-unfair.md](../../../../reports/cosmos_cometbft_findings/m-6-the-rewards-distribution-in-the-nftpositionmanager-is-unfair.md)
- [price-feeder-is-at-risk-of-rate-limiting-by-public-apis.md](../../../../reports/cosmos_cometbft_findings/price-feeder-is-at-risk-of-rate-limiting-by-public-apis.md)

## Vulnerability Title

**Oracle and Price Feed Vulnerabilities in Cosmos Protocols**

### Overview

This entry documents 3 distinct vulnerability patterns extracted from 8 audit reports (4 HIGH, 3 MEDIUM severity) across 7 protocols by 3 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Price Feed Reliability

**Frequency**: 6/8 reports | **Severity**: MEDIUM | **Validation**: Strong (3 auditors)
**Protocols affected**: Umee, Astaria, Babylonchain, ZeroLend One, Float Capital

This bug report discusses a bug found in the Shardus-core repository, which is used for blockchain and distributed ledger technology. The bug allows for more archivers to join the network than the maximum limit, which can cause issues such as network shutdown and crashes in RPC API. This can also le

**Example 1.1** [UNKNOWN] — unknown
Source: `archiver-join-limit-logic-error.md`
```solidity
// ❌ VULNERABLE: Price Feed Reliability
export function registerRoutes() {
  network.registerExternalPost('joinarchiver', async (req, res) => {
    const err = validateTypes(req, { body: 'o' })
    if (err) {
      warn(`joinarchiver: bad req ${err}`)
      return res.send({ success: false, error: err })
    }

    const joinRequest = req.body
    if (logFlags.p2pNonFatal) info(`Archiver join request received: ${Utils.safeStringify(joinRequest)}`)

    const accepted = await addArchiverJoinRequest(joinRequest)
...
  }
}
```

**Example 1.2** [MEDIUM] — Float Capital
Source: `m-3-funding-rate-calculation-is-not-correct.md`
```solidity
// ❌ VULNERABLE: Price Feed Reliability
uint256 totalFunding = (2 * overbalancedValue * fundingRateMultiplier * oracleManager.EPOCH_LENGTH()) / (365.25 days * 10000);
```

#### Pattern 2: Oracle Stake Requirement

**Frequency**: 1/8 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Advanced Blockchain

This bug report is about data validation in the runtime/picasso/src/weights/balances.rs and runtime/picasso/src/weights/democracy.rs files. When a user requests the price of an asset, oracles submit prices by calling the submit_price function. This function checks whether the oracle has staked the m

**Example 2.1** [HIGH] — Advanced Blockchain
Source: `failure-to-enforce-minimum-oracle-stake-requirement.md`
```solidity
// ❌ VULNERABLE: Oracle Stake Requirement
pub fn handle_payout(
    pre_prices: &[PrePrice<T::PriceValue, T::BlockNumber, T::AccountId>],
    price: T::PriceValue,
    asset_id: T::AssetId,
) {
    for answer in pre_prices {
        let accuracy: Percent;
        if answer.price < price {
            accuracy = PerThing::from_rational(answer.price, price);
        } else {
            let adjusted_number = price.saturating_sub(answer.price - price);
            accuracy = PerThing::from_rational(adjusted_number, price);
        }
        let min_accuracy = AssetsInfo::<T>::get(asset_id).threshold;
        if accuracy < min_accuracy {
            let slash_amount = T::SlashAmount::get();
            let try_slash = T::Currency::can_slash(&answer.who, slash_amount);
            if !try_slash {
                log::warn!("Failed to s
```

#### Pattern 3: Oracle Frontrunning

**Frequency**: 1/8 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Napier Finance - LST/LRT Integrations

This bug report highlights an issue where users can avoid losses on their tokens by redeeming them before a price decrease. This is possible through the use of certain adapters in the Napier protocol, which allow for instant redemption of tokens for ETH if the amount is within the available ETH buff


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
- Total reports analyzed: 8
- HIGH severity: 4 (50%)
- MEDIUM severity: 3 (37%)
- Unique protocols affected: 7
- Independent audit firms: 3
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

> `oracle`, `price-feed`, `stale-price`, `manipulation`, `TWAP`, `deviation`, `frontrunning`, `Chainlink`, `price-oracle`, `staleness`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
