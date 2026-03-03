---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: rewards
vulnerability_type: reward_theft_manipulation

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - flashloan_reward_theft
  - reward_frontrunning
  - orphaned_reward_capture
  - reward_replay
  - reward_dilution
  - cross_contract_reward
  - fake_stake_reward
  - commission_theft

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - rewards
  - reward_theft
  - flashloan_staking
  - reward_frontrunning
  - orphaned_rewards
  - reward_dilution
  - commission_theft
  - MEV_rewards
  
language: go
version: all
---

## References
- [h-01-cross-contract-signature-replay-allows-users-to-inflate-rewards.md](../../../../reports/cosmos_cometbft_findings/h-01-cross-contract-signature-replay-allows-users-to-inflate-rewards.md)
- [signature-replay-attack-possible-between-stake-unstake-and-reward-functions-enab.md](../../../../reports/cosmos_cometbft_findings/signature-replay-attack-possible-between-stake-unstake-and-reward-functions-enab.md)
- [h-1-flashloan-tel-tokens-to-stake-and-exit-in-the-same-block-can-fake-a-huge-amo.md](../../../../reports/cosmos_cometbft_findings/h-1-flashloan-tel-tokens-to-stake-and-exit-in-the-same-block-can-fake-a-huge-amo.md)
- [spoofing-stake-information.md](../../../../reports/cosmos_cometbft_findings/spoofing-stake-information.md)
- [m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md](../../../../reports/cosmos_cometbft_findings/m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md)
- [m-1-flashloan-tel-tokens-to-stake-and-exit-in-the-same-block-can-fake-a-huge-amo.md](../../../../reports/cosmos_cometbft_findings/m-1-flashloan-tel-tokens-to-stake-and-exit-in-the-same-block-can-fake-a-huge-amo.md)
- [m-11-zivoeydldistributeyield-yield-distribution-is-flash-loan-manipulatable.md](../../../../reports/cosmos_cometbft_findings/m-11-zivoeydldistributeyield-yield-distribution-is-flash-loan-manipulatable.md)
- [m-02-orphaned-rewards-captured-by-first-staker.md](../../../../reports/cosmos_cometbft_findings/m-02-orphaned-rewards-captured-by-first-staker.md)
- [m-10-unsafe-casting-from-uint256-to-uint128-in-rewardsmanager.md](../../../../reports/cosmos_cometbft_findings/m-10-unsafe-casting-from-uint256-to-uint128-in-rewardsmanager.md)
- [m-20-claiming-delegation-rewards-via-the-precompile-can-result-in-a-loss-of-zeta.md](../../../../reports/cosmos_cometbft_findings/m-20-claiming-delegation-rewards-via-the-precompile-can-result-in-a-loss-of-zeta.md)
- [m-3-a-part-of-eth-rewards-can-be-stolen-by-sandwiching-claimdelayedwithdrawals.md](../../../../reports/cosmos_cometbft_findings/m-3-a-part-of-eth-rewards-can-be-stolen-by-sandwiching-claimdelayedwithdrawals.md)

## Vulnerability Title

**Reward Theft and Manipulation Vulnerabilities**

### Overview

This entry documents 6 distinct vulnerability patterns extracted from 11 audit reports (4 HIGH, 7 MEDIUM severity) across 10 protocols by 5 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Flashloan Reward Theft

**Frequency**: 4/11 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Virtuals Protocol, Zivoe, Telcoin

This bug report is about an issue found in the Telcoin Staking Module. It was found by WATCHPUG and is known as Issue H-1. It is related to a vulnerability in the Checkpoints#getAtBlock() function. This vulnerability allows a malicious user to fake their stake and gain high rewards with minimal mate

**Example 1.1** [MEDIUM] — Virtuals Protocol
Source: `m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md`
```solidity
// ❌ VULNERABLE: Flashloan Reward Theft
//contracts/fun/Bonding.sol
    function unwrapToken(address srcTokenAddress, address[] memory accounts) public {
        Token memory info = tokenInfo[srcTokenAddress];
        require(info.tradingOnUniswap, "Token is not graduated yet");

        FERC20 token = FERC20(srcTokenAddress);
        IERC20 agentToken = IERC20(info.agentToken);
        address pairAddress = factory.getPair(srcTokenAddress, router.assetToken());
        for (uint i = 0; i < accounts.length; i++) {
            address acc = accounts[i];
            uint256 balance = token.balanceOf(acc);
            if (balance > 0) {
                token.burnFrom(acc, balance);
|>              agentToken.transferFrom(pairAddress, acc, balance);//@audit no time restrictions, unwrapToken allows atomic agentToken conversion upon g
```

**Example 1.2** [MEDIUM] — Virtuals Protocol
Source: `m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md`
```solidity
// ❌ VULNERABLE: Flashloan Reward Theft
Flows: flashswap/flashloan -> bonding::buy -> bonding::unwrapToken -> uniswapV2router::swapExactTokensForETHSupportingFeeOnTransferTokens -> paypack flashswap/flashloan
```

#### Pattern 2: Reward Replay

**Frequency**: 2/11 reports | **Severity**: HIGH | **Validation**: Moderate (2 auditors)
**Protocols affected**: HYBUX_2025-11-11, Sapien

This bug report states that there is a problem with the signature verification in the `NFTStaking._stakeNFTs()` function. This means that an attacker can use the same signature on different contracts and exploit the system by staking low-rarity NFTs and receiving rewards as if they were high-rarity.

**Example 2.1** [HIGH] — HYBUX_2025-11-11
Source: `h-01-cross-contract-signature-replay-allows-users-to-inflate-rewards.md`
```solidity
// ❌ VULNERABLE: Reward Replay
bytes32 hash = keccak256(abi.encode(_sender, _tokenIds, _rarityWeightIndexes));
```

**Example 2.2** [HIGH] — HYBUX_2025-11-11
Source: `h-01-cross-contract-signature-replay-allows-users-to-inflate-rewards.md`
```solidity
// ❌ VULNERABLE: Reward Replay
bytes32 hash = keccak256(abi.encode(_sender, _tokenIds, _rarityWeightIndexes, address(this)));
```

#### Pattern 3: Orphaned Reward Capture

**Frequency**: 2/11 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Elixir_2025-08-17, Ajna Protocol

The report describes a bug in a contract called `sdeusd.move`. This bug occurs when rewards are distributed while there are no `sdeUSD` holders. The bug allows the first subsequent staker to capture all orphaned rewards at a 1:1 conversion rate, which means they get all the rewards without having to

**Example 3.1** [MEDIUM] — Elixir_2025-08-17
Source: `m-02-orphaned-rewards-captured-by-first-staker.md`
```solidity
// ❌ VULNERABLE: Orphaned Reward Capture
// transfer_in_rewards() - No check for active stakers
public fun transfer_in_rewards(...) {
    // Missing: assert!(total_supply(management) > 0, ENoActiveStakers);
    update_vesting_amount(management, amount, clock);
}

// convert_to_shares() - 1:1 ratio when no existing stakers
if (total_supply == 0 || total_assets == 0) {
    assets  // First staker gets 1:1 regardless of unvested rewards
}
```

**Example 3.2** [MEDIUM] — Elixir_2025-08-17
Source: `m-02-orphaned-rewards-captured-by-first-staker.md`
```solidity
// ❌ VULNERABLE: Orphaned Reward Capture
public fun transfer_in_rewards(...) {
    assert!(total_supply(management) > 0, ENoActiveStakers);
    update_vesting_amount(management, amount, clock);
    // ... rest of function
}
```

#### Pattern 4: Cross Contract Reward

**Frequency**: 1/11 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: ZetaChain Cross-Chain

This bug report discusses an issue with the Zetachain cross-chain protocol where ZETA rewards are not properly added to the EVM statedb when claiming Cosmos delegation rewards. This results in a loss of ZETA rewards when the EVM state is committed to the Cosmos state. The root cause of this issue is

#### Pattern 5: Reward Frontrunning

**Frequency**: 1/11 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Rio Network

This bug report highlights an issue where a part of ETH rewards can be stolen by an attacker by taking advantage of a delay in the claiming process. This can happen in three different scenarios, all of which end up sending funds to the rewards distributor. After a delay, the rewards can be claimed b

**Example 5.1** [MEDIUM] — Rio Network
Source: `m-3-a-part-of-eth-rewards-can-be-stolen-by-sandwiching-claimdelayedwithdrawals.md`
```solidity
// ❌ VULNERABLE: Reward Frontrunning
receive() external payable {
    (bool success,) = address(rewardDistributor()).call{value: msg.value}('');
    require(success);
}
```

**Example 5.2** [MEDIUM] — Rio Network
Source: `m-3-a-part-of-eth-rewards-can-be-stolen-by-sandwiching-claimdelayedwithdrawals.md`
```solidity
// ❌ VULNERABLE: Reward Frontrunning
import {IRioLRTWithdrawalQueue} from 'contracts/interfaces/IRioLRTWithdrawalQueue.sol';
import {IRioLRTOperatorRegistry} from 'contracts/interfaces/IRioLRTOperatorRegistry.sol';
import {CredentialsProofs, BeaconWithdrawal} from 'test/utils/beacon-chain/MockBeaconChain.sol';
```

#### Pattern 6: Fake Stake Reward

**Frequency**: 1/11 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Convergent

This bug report discusses a vulnerability in the staking function of the CVGTStakingPoolState account. The staking_info account, which is associated with the staking operation, can be spoofed by a malicious CVGTStakingPoolState account, allowing for unauthorized changes and potential security risks.

**Example 6.1** [HIGH] — Convergent
Source: `spoofing-stake-information.md`
```solidity
// ❌ VULNERABLE: Fake Stake Reward
pub struct Stake<'info> {
    [...]
    #[account(
        init_if_needed,
        space = 8 + CVGTStakingInfo::INIT_SPACE,
        payer = user,
        seeds = [
            b"info",
            user.key().as_ref()
        ],
        bump
    )]
    pub staking_info: Box<Account<'info, CVGTStakingInfo>>,
    [...]
}
```

**Example 6.2** [HIGH] — Convergent
Source: `spoofing-stake-information.md`
```solidity
// ❌ VULNERABLE: Fake Stake Reward
[...]
    #[account()]
    pub cvgt: Account<'info, Mint>,
    [...]
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
- Total reports analyzed: 11
- HIGH severity: 4 (36%)
- MEDIUM severity: 7 (63%)
- Unique protocols affected: 10
- Independent audit firms: 5
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

> `reward-theft`, `flashloan-staking`, `reward-frontrunning`, `orphaned-rewards`, `reward-dilution`, `commission-theft`, `MEV-rewards`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
