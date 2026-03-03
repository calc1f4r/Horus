---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: ibc
vulnerability_type: cross_chain_bridge_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - bridge_replay_attack
  - bridge_token_accounting
  - relayer_manipulation
  - bridge_freeze
  - bridge_message_validation
  - relayer_slash
  - bridge_denom_handling
  - observer_manipulation

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - ibc
  - bridge
  - cross_chain
  - relayer
  - replay_attack
  - token_accounting
  - bridge_freeze
  - message_validation
  - observer
  
language: go
version: all
---

## References
- [h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md](../../../../reports/cosmos_cometbft_findings/h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md)
- [relayer-and-system-owner-roles-must-be-separated.md](../../../../reports/cosmos_cometbft_findings/relayer-and-system-owner-roles-must-be-separated.md)
- [relayer-can-set-arbitrary-supported-tokens-for-upward-trades-on-l2.md](../../../../reports/cosmos_cometbft_findings/relayer-can-set-arbitrary-supported-tokens-for-upward-trades-on-l2.md)
- [cross-chain-transactions-can-be-replayed-when-the-chain-undergoes-a-hard-fork.md](../../../../reports/cosmos_cometbft_findings/cross-chain-transactions-can-be-replayed-when-the-chain-undergoes-a-hard-fork.md)
- [m-04-retry-payload-channel-collision.md](../../../../reports/cosmos_cometbft_findings/m-04-retry-payload-channel-collision.md)
- [m-05-limited-voting-options-allow-ballot-creation-spam.md](../../../../reports/cosmos_cometbft_findings/m-05-limited-voting-options-allow-ballot-creation-spam.md)
- [m-10-removed-observers-are-still-able-to-vote.md](../../../../reports/cosmos_cometbft_findings/m-10-removed-observers-are-still-able-to-vote.md)

## Vulnerability Title

**Cross-Chain Bridge and Relay Vulnerabilities**

### Overview

This entry documents 4 distinct vulnerability patterns extracted from 7 audit reports (3 HIGH, 4 MEDIUM severity) across 6 protocols by 5 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Bridge Replay Attack

**Frequency**: 2/7 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Toki Bridge, Wormhole

The bug report discusses a potential issue with the NttManager.sol code, specifically in the function "completeInboundQueuedTransfer". During a hard fork, if there are still pending transactions in the InboundQueued, they can be replayed on another chain. This is due to the lack of a checkFork(evmCh

**Example 1.1** [MEDIUM] — Toki Bridge
Source: `m-04-retry-payload-channel-collision.md`
```solidity
// ❌ VULNERABLE: Bridge Replay Attack
mapping(uint256 => mapping(uint64 => bytes)) revertReceive; // [chainId][sequence] = payload
```

**Example 1.2** [MEDIUM] — Toki Bridge
Source: `m-04-retry-payload-channel-collision.md`
```solidity
// ❌ VULNERABLE: Bridge Replay Attack
function getChainId(string memory localChannel, bool checksAppVersion) public view returns (uint256 counterpartyChainId) {
    ChannelInfo memory channelInfo = $.channelInfos[localChannel];
    counterpartyChainId = channelInfo.counterpartyChainId;
    if (checksAppVersion && channelInfo.appVersion != APP_VERSION) {
        revert TokiInvalidAppVersion(channelInfo.appVersion, APP_VERSION);
    }
}
```

#### Pattern 2: Observer Manipulation

**Frequency**: 2/7 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: ZetaChain Cross-Chain, ZetaChain

The bug report discusses a problem with the voting system for certain types of votes. It allows compromised or faulty observers to create spam ballots with false observations, and honest observers are unable to vote against them. This results in wasted resources for honest observers without any puni

**Example 2.1** [MEDIUM] — ZetaChain
Source: `m-05-limited-voting-options-allow-ballot-creation-spam.md`
```solidity
// ❌ VULNERABLE: Observer Manipulation
ballot, err = k.zetaObserverKeeper.AddVoteToBallot(ctx, ballot, msg.Creator, observerTypes.VoteType_SuccessObservation)
```

**Example 2.2** [MEDIUM] — ZetaChain
Source: `m-05-limited-voting-options-allow-ballot-creation-spam.md`
```solidity
// ❌ VULNERABLE: Observer Manipulation
ballot, err = k.AddVoteToBallot(ctx, ballot, vote.Creator, types.VoteType_SuccessObservation)
```

#### Pattern 3: Relayer Slash

**Frequency**: 2/7 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Pheasant Network

The report discusses a potential security issue with the current system where a relayer can use a function to modify important contract addresses. This could lead to misuse of the system and put users at risk. The report suggests separating roles and clearly defining the actions that can be performe

#### Pattern 4: Bridge Denom Handling

**Frequency**: 1/7 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Initia

The bug report is about a flaw in the MiniEVM system, specifically in the ERC20 contracts that allow users to interact with the system. When a user creates an ERC20 contract through Cosmos, it is saved as `evm/ADDRESS` and the corresponding EVM address is also saved. However, there is a flaw in the 

**Example 4.1** [HIGH] — Initia
Source: `h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md`
```solidity
// ❌ VULNERABLE: Bridge Denom Handling
func (k ERC20Keeper) MintCoins(ctx context.Context, addr sdk.AccAddress, amount sdk.Coins) error {
	// ... snip ...

	for _, coin := range amount {
		denom := coin.Denom
		if types.IsERC20Denom(denom) {
			return moderrors.Wrapf(types.ErrInvalidRequest, "cannot mint erc20 coin: %s", coin.Denom)
		}

		// ... snip ...

		inputBz, err := k.ERC20ABI.Pack("sudoMint", evmAddr, coin.Amount.BigInt())
		if err != nil {
			return types.ErrFailedToPackABI.Wrap(err.Error())
		}

		// ... snip ...
	}

	// ... snip ...
}
```

**Example 4.2** [HIGH] — Initia
Source: `h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md`
```solidity
// ❌ VULNERABLE: Bridge Denom Handling
func (k ERC20Keeper) BurnCoins(ctx context.Context, addr sdk.AccAddress, amount sdk.Coins) error {
	// ... snip ...

	for _, coin := range amount {
		// if a coin is not generated from 0x1, then send the coin to community pool
		// because we don't have burn capability.
		if types.IsERC20Denom(coin.Denom) {
			if err := k.communityPoolKeeper.FundCommunityPool(ctx, amount, evmAddr.Bytes()); err != nil {
				return err
			}

			continue
		}

		// ... snip ...
	}

	// ... snip ...
}
```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 3 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 7
- HIGH severity: 3 (42%)
- MEDIUM severity: 4 (57%)
- Unique protocols affected: 6
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

> `bridge`, `cross-chain`, `relayer`, `replay-attack`, `token-accounting`, `bridge-freeze`, `message-validation`, `observer`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
