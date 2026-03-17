---
protocol: generic
chain: cosmos
category: dos
vulnerability_type: chain_halt_consensus_dos

attack_type: logical_error|economic_exploit|dos
affected_component: dos_logic

primitives:
  - block_production_halt
  - consensus_halt
  - state_machine
  - unbounded_beginblock
  - unbounded_endblock
  - unbounded_array
  - panic_crash
  - message_flooding
  - deposit_spam
  - proposal_spam

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - dos
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: denial_of_service
pattern_key: denial_of_service | dos_logic | chain_halt_consensus_dos

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - TestAllocateRewards_RewardsPlanFlood
  - TestAllocateRewards_TokenFlood
  - TestTerminateEndedRewardsPlan_TokenFlood
  - _calculateChallengerEligibility
  - balance
  - block_production_halt
  - consensus_halt
  - deposit
  - deposit_spam
  - message_flooding
  - panic_crash
  - proposal_spam
  - state_machine
  - such
  - unbounded_array
  - unbounded_beginblock
  - unbounded_endblock
  - verifyDoubleSigning
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Dos Block Production Halt
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Chain halt by spamming deposits request with minimum staking | `reports/cosmos_cometbft_findings/chain-halt-by-spamming-deposits-request-with-minimum-staking-amount.md` | MEDIUM | Cantina |
| [H-06] Hardcoded gas used in ERC20 queries allows for block  | `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md` | HIGH | Code4rena |
| Malformed blob tx causes Nethermind validators to stop produ | `reports/cosmos_cometbft_findings/h-2-malformed-blob-tx-causes-nethermind-validators-to-stop-producing-blocks.md` | HIGH | Sherlock |
| Adversary can arbitrarily trigger a chain halt by sending `M | `reports/cosmos_cometbft_findings/h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md` | HIGH | Sherlock |
| Incompatibility with blobs lead to halt of block processing | `reports/cosmos_cometbft_findings/incompatibility-with-blobs-lead-to-halt-of-block-processing.md` | HIGH | Halborn |
| Linear iteration over Rewards Plans in BeginBlock exposes pe | `reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md` | HIGH | Cantina |
| Linear iteration over undelegations with unmetered token tra | `reports/cosmos_cometbft_findings/linear-iteration-over-undelegations-with-unmetered-token-transfers-expose-a-perm.md` | HIGH | Cantina |
| [M-25] Observer Can Temporarily Halt Chain | `reports/cosmos_cometbft_findings/m-25-observer-can-temporarily-halt-chain.md` | MEDIUM | Code4rena |

### Dos Consensus Halt
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Chain halt by spamming deposits request with minimum staking | `reports/cosmos_cometbft_findings/chain-halt-by-spamming-deposits-request-with-minimum-staking-amount.md` | MEDIUM | Cantina |
| DoS in Cosmos SDK Crisis Module (github.com/cosmos/cosmos-sd | `reports/cosmos_cometbft_findings/dos-in-cosmos-sdk-crisis-module-githubcomcosmoscosmos-sdkxcrisis.md` | MEDIUM | Zokyo |
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| ASA-2025-003: Groups module can halt chain when handling a m | `reports/cosmos_cometbft_findings/h-18-asa-2025-003-groups-module-can-halt-chain-when-handling-a-malicious-proposa.md` | HIGH | Sherlock |
| Attacker can freeze chain and steal challenge deposits using | `reports/cosmos_cometbft_findings/h-2-attacker-can-freeze-chain-and-steal-challenge-deposits-using-fake-prevstater.md` | HIGH | Sherlock |
| Adversary can arbitrarily trigger a chain halt by sending `M | `reports/cosmos_cometbft_findings/h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md` | HIGH | Sherlock |
| Use of Vulnerable IBC-Go v8.4.0 - Non-Deterministic JSON Unm | `reports/cosmos_cometbft_findings/h-7-use-of-vulnerable-ibc-go-v840-non-deterministic-json-unmarshalling-can-cause.md` | HIGH | Sherlock |
| Linear iteration over Rewards Plans in BeginBlock exposes pe | `reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md` | HIGH | Cantina |

### Dos State Machine
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Linear iteration over Rewards Plans in BeginBlock exposes pe | `reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md` | HIGH | Cantina |
| The issue of SLOW ABCI METHODS has not been resolved. | `reports/cosmos_cometbft_findings/m-28-the-issue-of-slow-abci-methods-has-not-been-resolved.md` | MEDIUM | Sherlock |
| Unmetered BeginBlock iteration over balances exposes low-cos | `reports/cosmos_cometbft_findings/unmetered-beginblock-iteration-over-balances-exposes-low-cost-on-demand-chain-ha.md` | HIGH | Cantina |

### Dos Unbounded Beginblock
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Linear iteration over Rewards Plans in BeginBlock exposes pe | `reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md` | HIGH | Cantina |
| Unmetered BeginBlock iteration over balances exposes low-cos | `reports/cosmos_cometbft_findings/unmetered-beginblock-iteration-over-balances-exposes-low-cost-on-demand-chain-ha.md` | HIGH | Cantina |

### Dos Unbounded Array
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Denial Of Slashing | `reports/cosmos_cometbft_findings/denial-of-slashing.md` | HIGH | OtterSec |
| Looping over an array of unbounded size can cause a denial o | `reports/cosmos_cometbft_findings/looping-over-an-array-of-unbounded-size-can-cause-a-denial-of-service.md` | MEDIUM | TrailOfBits |
| Slashing mechanism grants exponentially more rewards than ex | `reports/cosmos_cometbft_findings/slashing-mechanism-grants-exponentially-more-rewards-than-expected.md` | HIGH | OpenZeppelin |
| Unbounded size of request in Covenant signer service | `reports/cosmos_cometbft_findings/unbounded-size-of-request-in-covenant-signer-service.md` | MEDIUM | Cantina |

### Dos Panic Crash
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Malicious peer can cause a syncing node to panic during bloc | `reports/cosmos_cometbft_findings/m-8-malicious-peer-can-cause-a-syncing-node-to-panic-during-blocksync.md` | MEDIUM | Sherlock |

### Dos Message Flooding
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-05] Limited Voting Options Allow Ballot Creation Spam | `reports/cosmos_cometbft_findings/m-05-limited-voting-options-allow-ballot-creation-spam.md` | MEDIUM | Code4rena |

### Dos Deposit Spam
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Chain halt by spamming deposits request with minimum staking | `reports/cosmos_cometbft_findings/chain-halt-by-spamming-deposits-request-with-minimum-staking-amount.md` | MEDIUM | Cantina |
| DoS Risk Due to Small Deposits and Front-Running in `deposit | `reports/cosmos_cometbft_findings/dos-risk-due-to-small-deposits-and-front-running-in-deposit-function.md` | MEDIUM | MixBytes |
| Lack of validator penalties enables risk-free economic censo | `reports/cosmos_cometbft_findings/lack-of-validator-penalties-enables-risk-free-economic-censorship-and-liveness-a.md` | MEDIUM | Spearbit |
| [M-05] Attacker can partially DoS L1 operations in StakingMa | `reports/cosmos_cometbft_findings/m-05-attacker-can-partially-dos-l1-operations-in-stakingmanager-by-making-huge-n.md` | MEDIUM | Code4rena |
| Unmetered balance iteration in reward termination can be exp | `reports/cosmos_cometbft_findings/unmetered-balance-iteration-in-reward-termination-can-be-exploited-to-permission.md` | HIGH | Cantina |
| Unmetered BeginBlock iteration over balances exposes low-cos | `reports/cosmos_cometbft_findings/unmetered-beginblock-iteration-over-balances-exposes-low-cost-on-demand-chain-ha.md` | HIGH | Cantina |

---

# Chain Halt Consensus Dos - Comprehensive Database

**A Complete Pattern-Matching Guide for Chain Halt Consensus Dos in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Dos Block Production Halt](#1-dos-block-production-halt)
2. [Dos Consensus Halt](#2-dos-consensus-halt)
3. [Dos State Machine](#3-dos-state-machine)
4. [Dos Unbounded Beginblock](#4-dos-unbounded-beginblock)
5. [Dos Unbounded Array](#5-dos-unbounded-array)
6. [Dos Panic Crash](#6-dos-panic-crash)
7. [Dos Message Flooding](#7-dos-message-flooding)
8. [Dos Deposit Spam](#8-dos-deposit-spam)

---

## 1. Dos Block Production Halt

### Overview

Implementation flaw in dos block production halt logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 13 audit reports with severity distribution: HIGH: 10, MEDIUM: 3.

> **Key Finding**: The report describes a bug in the Beacon Kit, which is used to compute the hash tree root when proposing a block in order to set the Eth1Data field in the Beacon block. The bug is that deposits in the Beacon Kit are never pruned, which means that when proposing a block, it will always retrieve all t



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of denial_of_service"
- Pattern key: `denial_of_service | dos_logic | chain_halt_consensus_dos`
- Interaction scope: `single_contract`
- Primary affected component(s): `dos_logic`
- High-signal code keywords: `TestAllocateRewards_RewardsPlanFlood`, `TestAllocateRewards_TokenFlood`, `TestTerminateEndedRewardsPlan_TokenFlood`, `_calculateChallengerEligibility`, `balance`, `block_production_halt`, `consensus_halt`, `deposit`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Unbounded loop over user-controlled array can exceed block gas limit
- Signal 2: External call failure causes entire transaction to revert
- Signal 3: Attacker can grief operations by manipulating state to cause reverts
- Signal 4: Resource exhaustion through repeated operations without rate limiting

#### False Positive Guards

- Not this bug when: Loop iterations are bounded by a reasonable constant
- Safe if: External call failures are handled gracefully (try/catch or pull pattern)
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Implementation flaw in dos block production halt logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies dos block production halt in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to dos operations

### Vulnerable Pattern Examples

**Example 1: Chain halt by spamming deposits request with minimum staking amount** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/chain-halt-by-spamming-deposits-request-with-minimum-staking-amount.md`
```go
// Grab all previous deposits from genesis up to the current index + max deposits per block.
deposits, err := s.sb.DepositStore().GetDepositsByIndex(
    0, depositIndex+s.chainSpec.MaxDepositsPerBlock(),
)
```

**Example 2: [H-06] Hardcoded gas used in ERC20 queries allows for block production halt from** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md`
```go
File: funtoken.go
265: func (p precompileFunToken) balance(
266: 	start OnRunStartResult,
267: 	contract *vm.Contract,
268: ) (bz []byte, err error) {
---
285: 	erc20Bal, err := p.evmKeeper.ERC20().BalanceOf(funtoken.Erc20Addr.Address, addrEth, ctx)
286: 	if err != nil {
287: 		return
288: 	}
```

**Example 3: Malformed blob tx causes Nethermind validators to stop producing blocks** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-2-malformed-blob-tx-causes-nethermind-validators-to-stop-producing-blocks.md`
```
// Vulnerable pattern from Fusaka Upgrade:
Source: https://github.com/sherlock-audit/2025-09-ethereum-fusaka-upgrade-judging/issues/176 

This issue has been acknowledged by the team but won't be fixed at this time.
```

**Example 4: Adversary can arbitrarily trigger a chain halt by sending `MsgRemove{Delegate}St** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md`
```go
func RemoveStakes(
	sdkCtx sdk.Context,
	currentBlock int64,
	k emissionskeeper.Keeper,
) {
	removals, err := k.GetStakeRemovalsForBlock(sdkCtx, currentBlock)
	...
	for _, stakeRemoval := range removals {
		...
		coins := sdk.NewCoins(sdk.NewCoin(chainParams.DefaultBondDenom, stakeRemoval.Amount))
```

**Example 5: Incompatibility with blobs lead to halt of block processing** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/incompatibility-with-blobs-lead-to-halt-of-block-processing.md`
```go
err = retryForever(ctx, func(ctx context.Context) (bool, error) {
	status, err := pushPayload(ctx, s.engineCl, payload)
	if err != nil || isUnknown(status) {
		// We need to retry forever on networking errors, but can't easily identify them, so retry all errors.
		log.Warn(ctx, "Verifying proposal failed: push new payload to evm (will retry)", err,
			"status", status.Status)

		return false, nil // Retry
	} else if invalid, err := isInvalid(status); invalid {
		return false, errors.Wrap(err, "invalid payload, rejecting proposal") // Don't retry
	} else if isSyncing(status) {
		// If this is initial sync, we need to continue and set a target head to sync to, so don't retry.
		log.Warn(ctx, "Can't properly verifying proposal: evm syncing", err,
			"payload_height", payload.Number)
	}

	return true, nil // We are done, don't retry.
})
if err != nil {
	return nil, err
}
```

**Variant: Dos Block Production Halt - HIGH Severity Cases** [HIGH]
> Found in 10 reports:
> - `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md`
> - `reports/cosmos_cometbft_findings/h-2-malformed-blob-tx-causes-nethermind-validators-to-stop-producing-blocks.md`
> - `reports/cosmos_cometbft_findings/h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md`

**Variant: Dos Block Production Halt in Berachain** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/chain-halt-by-spamming-deposits-request-with-minimum-staking-amount.md`
> - `reports/cosmos_cometbft_findings/malicious-user-can-halt-evm-chain-by-providing-two-similar-blobs-in-a-single-evm.md`

**Variant: Dos Block Production Halt in Allora** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md`
> - `reports/cosmos_cometbft_findings/m-28-the-issue-of-slow-abci-methods-has-not-been-resolved.md`

**Variant: Dos Block Production Halt in MilkyWay** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md`
> - `reports/cosmos_cometbft_findings/linear-iteration-over-undelegations-with-unmetered-token-transfers-expose-a-perm.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in dos block production halt logic allows exploitation through missing validatio
func secureDosBlockProductionHalt(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 13 audit reports
- **Severity Distribution**: HIGH: 10, MEDIUM: 3
- **Affected Protocols**: Berachain Beaconkit, Sei EVM, MilkyWay, Nibiru, ZetaChain
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Dos Consensus Halt

### Overview

Implementation flaw in dos consensus halt logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 15 audit reports with severity distribution: HIGH: 12, MEDIUM: 3.

> **Key Finding**: The report describes a bug in the Beacon Kit, which is used to compute the hash tree root when proposing a block in order to set the Eth1Data field in the Beacon block. The bug is that deposits in the Beacon Kit are never pruned, which means that when proposing a block, it will always retrieve all t

### Vulnerability Description

#### Root Cause

Implementation flaw in dos consensus halt logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies dos consensus halt in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to dos operations

### Vulnerable Pattern Examples

**Example 1: Chain halt by spamming deposits request with minimum staking amount** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/chain-halt-by-spamming-deposits-request-with-minimum-staking-amount.md`
```go
// Grab all previous deposits from genesis up to the current index + max deposits per block.
deposits, err := s.sb.DepositStore().GetDepositsByIndex(
    0, depositIndex+s.chainSpec.MaxDepositsPerBlock(),
)
```

**Example 2: DoS in Cosmos SDK Crisis Module (github.com/cosmos/cosmos-sdk/x/crisis)** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/dos-in-cosmos-sdk-crisis-module-githubcomcosmoscosmos-sdkxcrisis.md`
```
// Vulnerable pattern from Shido:
**Severity:** Medium

**Status**: Acknowledged

**Description:** 

The chain does not halt when an invariant check fails on a Cosmos SDK network, and a transaction is sent to the x/crisis module.

**Impact**: 

This can lead to a denial-of-service (DoS) attack, in which an attacker repeatedly triggers invariant failures to disrupt the network.

**Likelihood:** 

Moderate, as it requires knowledge of the invariant checks and the ability to craft malicious transactions.

**Recommendation:** 

Ther
```

**Example 3: [H-01] `BlockBeforeSend` hook can be exploited to perform a denial of service** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md`
```go
poc: build
   	@echo "starting POC.."

   	# clear port 26657 if old process still running
   	@if lsof -i :26657; then \
   		kill -9 $$(lsof -t -i :26657) || echo "cannot kill process"; \
   	fi

   	# remove old setup and init new one
   	@rm -rf .mantrapoc
   	@mkdir -p .mantrapoc

   	./build/mantrachaind init poc-test --chain-id test-chain --home .mantrapoc
   	./build/mantrachaind keys add validator --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add validator2 --keyring-backend test --home .mantrapoc

   	# create alice and bob account
   	./build/mantrachaind keys add alice --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add bob --keyring-backend test --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator2 -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show alice -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show bob -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc

   	./build/mantrachaind genesis gentx validator 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc
   	# ./build/mantrachaind genesis gentx validator2 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc

   	./build/mantrachaind genesis collect-gentxs --home .mantrapoc

   	# start node
   	./build/mantrachaind start --home .mantrapoc --minimum-gas-prices 0stake
```

**Example 4: ASA-2025-003: Groups module can halt chain when handling a malicious proposal** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-18-asa-2025-003-groups-module-can-halt-chain-when-handling-a-malicious-proposa.md`
```
// Vulnerable pattern from SEDA Protocol:
Source: https://github.com/sherlock-audit/2024-12-seda-protocol-judging/issues/271
```

**Example 5: Attacker can freeze chain and steal challenge deposits using fake `prevStateRoot** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-2-attacker-can-freeze-chain-and-steal-challenge-deposits-using-fake-prevstater.md`
```go
require(
    finalizedStateRoots[_batchIndex - 1] == BatchHeaderCodecV0.getPrevStateHash(memPtr),
    "incorrect previous state root"
);
```

**Variant: Dos Consensus Halt - HIGH Severity Cases** [HIGH]
> Found in 12 reports:
> - `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md`
> - `reports/cosmos_cometbft_findings/h-18-asa-2025-003-groups-module-can-halt-chain-when-handling-a-malicious-proposa.md`
> - `reports/cosmos_cometbft_findings/h-2-attacker-can-freeze-chain-and-steal-challenge-deposits-using-fake-prevstater.md`

**Variant: Dos Consensus Halt in Berachain** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/chain-halt-by-spamming-deposits-request-with-minimum-staking-amount.md`
> - `reports/cosmos_cometbft_findings/malicious-user-can-halt-evm-chain-by-providing-two-similar-blobs-in-a-single-evm.md`

**Variant: Dos Consensus Halt in SEDA Protocol** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-18-asa-2025-003-groups-module-can-halt-chain-when-handling-a-malicious-proposa.md`
> - `reports/cosmos_cometbft_findings/h-7-use-of-vulnerable-ibc-go-v840-non-deterministic-json-unmarshalling-can-cause.md`

**Variant: Dos Consensus Halt in MilkyWay** [HIGH]
> Protocol-specific variant found in 4 reports:
> - `reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md`
> - `reports/cosmos_cometbft_findings/linear-iteration-over-undelegations-with-unmetered-token-transfers-expose-a-perm.md`
> - `reports/cosmos_cometbft_findings/unmetered-balance-iteration-in-reward-termination-can-be-exploited-to-permission.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in dos consensus halt logic allows exploitation through missing validation, inco
func secureDosConsensusHalt(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 15 audit reports
- **Severity Distribution**: HIGH: 12, MEDIUM: 3
- **Affected Protocols**: Berachain Beaconkit, MorphL2, Shido, MilkyWay, Sei EVM
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Dos State Machine

### Overview

Implementation flaw in dos state machine logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 2, MEDIUM: 1.

> **Key Finding**: This bug report discusses a vulnerability in the rewards plan feature of a software. The bug allows an attacker to create an unlimited number of plans and cause a chain halt on the next block. Even though there is a fee for plan creation, it is not high enough to protect against this attack. The lik

### Vulnerability Description

#### Root Cause

Implementation flaw in dos state machine logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies dos state machine in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to dos operations

### Vulnerable Pattern Examples

**Example 1: Linear iteration over Rewards Plans in BeginBlock exposes permissionless chain h** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md`
```go
func (suite *KeeperTestSuite) TestAllocateRewards_RewardsPlanFlood() {
    // Modify this value to simulate different number of plans
    numPlans := 10000
    // Modify this value to simulate different spreads of plans per block
    plansPerBlock := 10000
    
    // --- Setup ---
    // Cache the context to avoid conflicts
    ctx, _ := suite.ctx.CacheContext()
    // Set up a sample service and operator
    service, _ := suite.setupSampleServiceAndOperator(ctx)
    // Fund the admin account to create rewards plans
    adminAddr := testutil.TestAddress(10000)
    initialFunds := sdk.NewCoins(sdk.NewInt64Coin("umilk", 1_000_000_000_000))
    suite.FundAccount(ctx, adminAddr.String(), initialFunds)
    
    // Create a delegator to make plans active
    delegatorAddr := testutil.TestAddress(1)
    suite.DelegateService(
        ctx,
        service.ID,
        sdk.NewCoins(sdk.NewInt64Coin("umilk", 100_000_000)),
        delegatorAddr.String(),
        true,
    )
    
    // Simulate creating many rewards plans across multiple blocks
    planStartTime := ctx.BlockTime()
    planEndTime := planStartTime.Add(1 * time.Hour).Add(1 * time.Second)
    for i := 0; i < numPlans; i += plansPerBlock {
        end := i + plansPerBlock
        if end > numPlans {
            end = numPlans
        }
        // Create plans for this block
// ... (truncated)
```

**Example 2: The issue of SLOW ABCI METHODS has not been resolved.** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-28-the-issue-of-slow-abci-methods-has-not-been-resolved.md`
```go
// Apply a function on all active topics that also have an epoch ending at this block
// Active topics have more than a globally-set minimum weight, a function of revenue and stake
// "Safe" because bounded by max number of pages and apply running, online operations.
func SafeApplyFuncOnAllActiveEpochEndingTopics(
	ctx sdk.Context,
	k keeper.Keeper,
	block BlockHeight,
	fn func(sdkCtx sdk.Context, topic *types.Topic) error,
	topicPageLimit uint64,
	maxTopicPages uint64,
) error {
	topicPageKey := make([]byte, 0)
	i := uint64(0)
@>	for {
		topicPageRequest := &types.SimpleCursorPaginationRequest{Limit: topicPageLimit, Key: topicPageKey}
		topicsActive, topicPageResponse, err := k.GetIdsOfActiveTopics(ctx, topicPageRequest)
		if err != nil {
			Logger(ctx).Warn(fmt.Sprintf("Error getting ids of active topics: %s", err.Error()))
			continue
		}

@>		for _, topicId := range topicsActive {
			topic, err := k.GetTopic(ctx, topicId)
			if err != nil {
				Logger(ctx).Warn(fmt.Sprintf("Error getting topic: %s", err.Error()))
				continue
			}

			if k.CheckCadence(block, topic) {
				// All checks passed => Apply function on the topic
				err = fn(ctx, &topic)
				if err != nil {
					Logger(ctx).Warn(fmt.Sprintf("Error applying function on topic: %s", err.Error()))
					continue
				}
// ... (truncated)
```

**Example 3: Unmetered BeginBlock iteration over balances exposes low-cost, on-demand chain h** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/unmetered-beginblock-iteration-over-balances-exposes-low-cost-on-demand-chain-ha.md`
```go
func (suite *KeeperTestSuite) TestAllocateRewards_TokenFlood() {
	// Modify these values to simulate different scenarios
	numTokens := 10000
	tokensPerBlock := 500
	
	// --- Setup ---
	// Cache the context to avoid conflicts
	ctx, _ := suite.ctx.CacheContext()
	
	// Set up a sample service and operator
	service, _ := suite.setupSampleServiceAndOperator(ctx)
	
	// Create a rewards plan
	planStartTime := ctx.BlockTime()
	planEndTime := planStartTime.Add(24 * time.Hour)
	amountPerDay := sdk.NewCoins(sdk.NewInt64Coin("umilk", 1_000_000_000))
	plan := suite.CreateBasicRewardsPlan(
		ctx,
		service.ID,
		amountPerDay,
		planStartTime,
		planEndTime,
		amountPerDay,
	)

	// Get the plan rewards pool address
	planRewardsPoolAddr := plan.MustGetRewardsPoolAddress(suite.accountKeeper.AddressCodec())
	
	// Simulate an attacker sending tokens across multiple blocks
	attackerAddr := testutil.TestAddress(9999)
	for i := 0; i < numTokens; i += tokensPerBlock {
		blockCoins := sdk.NewCoins()
		end := i + tokensPerBlock
		if end > numTokens {
			end = numTokens
// ... (truncated)
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in dos state machine logic allows exploitation through missing validation, incor
func secureDosStateMachine(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 3 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 1
- **Affected Protocols**: Allora, MilkyWay
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Dos Unbounded Beginblock

### Overview

Implementation flaw in dos unbounded beginblock logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: This bug report discusses a vulnerability in the rewards plan feature of a software. The bug allows an attacker to create an unlimited number of plans and cause a chain halt on the next block. Even though there is a fee for plan creation, it is not high enough to protect against this attack. The lik

### Vulnerability Description

#### Root Cause

Implementation flaw in dos unbounded beginblock logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies dos unbounded beginblock in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to dos operations

### Vulnerable Pattern Examples

**Example 1: Linear iteration over Rewards Plans in BeginBlock exposes permissionless chain h** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md`
```go
func (suite *KeeperTestSuite) TestAllocateRewards_RewardsPlanFlood() {
    // Modify this value to simulate different number of plans
    numPlans := 10000
    // Modify this value to simulate different spreads of plans per block
    plansPerBlock := 10000
    
    // --- Setup ---
    // Cache the context to avoid conflicts
    ctx, _ := suite.ctx.CacheContext()
    // Set up a sample service and operator
    service, _ := suite.setupSampleServiceAndOperator(ctx)
    // Fund the admin account to create rewards plans
    adminAddr := testutil.TestAddress(10000)
    initialFunds := sdk.NewCoins(sdk.NewInt64Coin("umilk", 1_000_000_000_000))
    suite.FundAccount(ctx, adminAddr.String(), initialFunds)
    
    // Create a delegator to make plans active
    delegatorAddr := testutil.TestAddress(1)
    suite.DelegateService(
        ctx,
        service.ID,
        sdk.NewCoins(sdk.NewInt64Coin("umilk", 100_000_000)),
        delegatorAddr.String(),
        true,
    )
    
    // Simulate creating many rewards plans across multiple blocks
    planStartTime := ctx.BlockTime()
    planEndTime := planStartTime.Add(1 * time.Hour).Add(1 * time.Second)
    for i := 0; i < numPlans; i += plansPerBlock {
        end := i + plansPerBlock
        if end > numPlans {
            end = numPlans
        }
        // Create plans for this block
// ... (truncated)
```

**Example 2: Unmetered BeginBlock iteration over balances exposes low-cost, on-demand chain h** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/unmetered-beginblock-iteration-over-balances-exposes-low-cost-on-demand-chain-ha.md`
```go
func (suite *KeeperTestSuite) TestAllocateRewards_TokenFlood() {
	// Modify these values to simulate different scenarios
	numTokens := 10000
	tokensPerBlock := 500
	
	// --- Setup ---
	// Cache the context to avoid conflicts
	ctx, _ := suite.ctx.CacheContext()
	
	// Set up a sample service and operator
	service, _ := suite.setupSampleServiceAndOperator(ctx)
	
	// Create a rewards plan
	planStartTime := ctx.BlockTime()
	planEndTime := planStartTime.Add(24 * time.Hour)
	amountPerDay := sdk.NewCoins(sdk.NewInt64Coin("umilk", 1_000_000_000))
	plan := suite.CreateBasicRewardsPlan(
		ctx,
		service.ID,
		amountPerDay,
		planStartTime,
		planEndTime,
		amountPerDay,
	)

	// Get the plan rewards pool address
	planRewardsPoolAddr := plan.MustGetRewardsPoolAddress(suite.accountKeeper.AddressCodec())
	
	// Simulate an attacker sending tokens across multiple blocks
	attackerAddr := testutil.TestAddress(9999)
	for i := 0; i < numTokens; i += tokensPerBlock {
		blockCoins := sdk.NewCoins()
		end := i + tokensPerBlock
		if end > numTokens {
			end = numTokens
// ... (truncated)
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in dos unbounded beginblock logic allows exploitation through missing validation
func secureDosUnboundedBeginblock(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: HIGH: 2
- **Affected Protocols**: MilkyWay
- **Validation Strength**: Single auditor

---

## 5. Dos Unbounded Array

### Overview

Implementation flaw in dos unbounded array logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 2, MEDIUM: 2.

> **Key Finding**: This report discusses a vulnerability in the verifyDoubleSigning function, which can be exploited by a malicious operator to evade slashing. This vulnerability is due to the linear complexity of the function, which can be increased indefinitely by repeatedly calling the updateDelegation function. Th

### Vulnerability Description

#### Root Cause

Implementation flaw in dos unbounded array logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies dos unbounded array in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to dos operations

### Vulnerable Pattern Examples

**Example 1: Denial Of Slashing** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/denial-of-slashing.md`
```solidity
function verifyDoubleSigning(
    address operator,
    DoubleSigningEvidence memory e
) external {
    [...]
    for (uint256 i = 0; i < delegatedValidators.length; i++) {
        [...]
        if (EthosAVSUtils.compareStrings(delegatedValidators[i].validatorPubkey,
                                          e.validatorPubkey) &&
            isDelegationSlashable(delegatedValidators[i].endTimestamp))
        {
            timestampValid = true;
            stake = EthosAVSUtils.maxUint96(stake, delegatedValidators[i].stake);
        }
    }
    [...]
}
```

**Example 2: Looping over an array of unbounded size can cause a denial of service** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/looping-over-an-array-of-unbounded-size-can-cause-a-denial-of-service.md`
```solidity
function _calculateChallengerEligibility() internal {
    uint256 cutoffBlock = failedBlock.sub(CHALLENGER_BLOCK_DELAY);
    for (uint256 i = 0; i < challengers.addresses.length; i++) {
        address challenger = challengers.addresses[i];
        if (eligibilityInfo.lastStakedBlock[challenger] < cutoffBlock) {
            eligibilityInfo.eligibleAmount = eligibilityInfo.eligibleAmount.add(
                _storedBalance(challengerInfo.userInfo[challenger], challengerInfo)
            );
        }
    }
}
```

**Example 3: Slashing mechanism grants exponentially more rewards than expected** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/slashing-mechanism-grants-exponentially-more-rewards-than-expected.md`
```
// Vulnerable pattern from UMA DVM 2.0 Audit:
In the [`VotingV2`](https://github.com/UMAprotocol/protocol/blob/7938617bf79854811959eb605237edf6bdccbc90/packages/core/contracts/oracle/implementation/VotingV2.sol) contract the function [`updateTrackers`](https://github.com/UMAprotocol/protocol/blob/7938617bf79854811959eb605237edf6bdccbc90/packages/core/contracts/oracle/implementation/VotingV2.sol#798) calls the internal function [`_updateAccountSlashingTrackers`](https://github.com/UMAprotocol/protocol/blob/7938617bf79854811959eb605237edf6bdc
```

**Example 4: Unbounded size of request in Covenant signer service** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/unbounded-size-of-request-in-covenant-signer-service.md`
```go
#### Then, import the following attacking script in `exploit-dos.py`:
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in dos unbounded array logic allows exploitation through missing validation, inc
func secureDosUnboundedArray(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 4 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 2
- **Affected Protocols**: Ethos EVM, Babylonchain, Ante Protocol, UMA DVM 2.0 Audit
- **Validation Strength**: Strong (3+ auditors)

---

## 6. Dos Panic Crash

### Overview

Implementation flaw in dos panic crash logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report discusses a vulnerability found in the system's use of a vulnerable version of CometBFT. This vulnerability, known as GO-2024-2951, allows an attacker to cause a panic during blocksync, which can lead to a denial of service (DoS) attack on the network. The vulnerability is present in

### Vulnerability Description

#### Root Cause

Implementation flaw in dos panic crash logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies dos panic crash in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to dos operations

### Vulnerable Pattern Examples

**Example 1: Malicious peer can cause a syncing node to panic during blocksync** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-8-malicious-peer-can-cause-a-syncing-node-to-panic-during-blocksync.md`
```
// Vulnerable pattern from Allora:
Source: https://github.com/sherlock-audit/2024-06-allora-judging/issues/28
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in dos panic crash logic allows exploitation through missing validation, incorre
func secureDosPanicCrash(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: Allora
- **Validation Strength**: Single auditor

---

## 7. Dos Message Flooding

### Overview

Implementation flaw in dos message flooding logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The bug report discusses a problem with the voting system for certain types of votes. It allows compromised or faulty observers to create spam ballots with false observations, and honest observers are unable to vote against them. This results in wasted resources for honest observers without any puni

### Vulnerability Description

#### Root Cause

Implementation flaw in dos message flooding logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies dos message flooding in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to dos operations

### Vulnerable Pattern Examples

**Example 1: [M-05] Limited Voting Options Allow Ballot Creation Spam** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-05-limited-voting-options-allow-ballot-creation-spam.md`
```go
ballot, err = k.zetaObserverKeeper.AddVoteToBallot(ctx, ballot, msg.Creator, observerTypes.VoteType_SuccessObservation)
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in dos message flooding logic allows exploitation through missing validation, in
func secureDosMessageFlooding(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: ZetaChain
- **Validation Strength**: Single auditor

---

## 8. Dos Deposit Spam

### Overview

Implementation flaw in dos deposit spam logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 2, MEDIUM: 4.

> **Key Finding**: The report describes a bug in the Beacon Kit, which is used to compute the hash tree root when proposing a block in order to set the Eth1Data field in the Beacon block. The bug is that deposits in the Beacon Kit are never pruned, which means that when proposing a block, it will always retrieve all t

### Vulnerability Description

#### Root Cause

Implementation flaw in dos deposit spam logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies dos deposit spam in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to dos operations

### Vulnerable Pattern Examples

**Example 1: Chain halt by spamming deposits request with minimum staking amount** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/chain-halt-by-spamming-deposits-request-with-minimum-staking-amount.md`
```go
// Grab all previous deposits from genesis up to the current index + max deposits per block.
deposits, err := s.sb.DepositStore().GetDepositsByIndex(
    0, depositIndex+s.chainSpec.MaxDepositsPerBlock(),
)
```

**Example 2: DoS Risk Due to Small Deposits and Front-Running in `deposit` Function** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/dos-risk-due-to-small-deposits-and-front-running-in-deposit-function.md`
```
// Vulnerable pattern from DIA:
##### Description
This issue has been identified in the `deposit` function of the `Prestaking` contract.
There are two potential attack vectors that could be used to DoS the system:

1. **Small Deposits (1 wei deposits)**: Malicious users can fill the `stakingWallets` with extremely small deposits (e.g., 1 wei), which would make it harder to use the system effectively. Adding a minimum deposit amount would prevent such attacks by ensuring that deposits are meaningful, thus limiting the attacker'
```

**Example 3: Lack of validator penalties enables risk-free economic censorship and liveness a** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-validator-penalties-enables-risk-free-economic-censorship-and-liveness-a.md`
```
// Vulnerable pattern from Berachain Beaconkit:
## Severity: Medium Risk
```

**Example 4: [M-05] Attacker can partially DoS L1 operations in StakingManager by making huge** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-05-attacker-can-partially-dos-l1-operations-in-stakingmanager-by-making-huge-n.md`
```go
L1Operation[] private _pendingDeposits;
```

**Example 5: Unmetered balance iteration in reward termination can be exploited to permission** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/unmetered-balance-iteration-in-reward-termination-can-be-exploited-to-permission.md`
```go
func (suite *KeeperTestSuite) TestTerminateEndedRewardsPlan_TokenFlood() {
    // Modify these values to simulate different scenarios
    numTokens := 10000
    tokensPerBlock := 500
    // Cache the context to avoid conflicts
    ctx, _ := suite.ctx.CacheContext()
    // Set up a sample service
    service, _ := suite.setupSampleServiceAndOperator(ctx)
    // Create a rewards plan that will be terminated
    planStartTime := ctx.BlockTime()
    planEndTime := planStartTime.Add(24 * time.Hour)
    amountPerDay := sdk.NewCoins(sdk.NewInt64Coin("umilk", 1_000_000_000))
    plan := suite.CreateBasicRewardsPlan(
        ctx,
        service.ID,
        amountPerDay,
        planStartTime,
        planEndTime,
        amountPerDay,
    )
    // Get the plan rewards pool address
    planRewardsPoolAddr := plan.MustGetRewardsPoolAddress(suite.accountKeeper.AddressCodec())
    // Simulate an attacker sending tokens across multiple blocks
    attackerAddr := testutil.TestAddress(9999)
    for i := 0; i < numTokens; i += tokensPerBlock {
        blockCoins := sdk.NewCoins()
        end := i + tokensPerBlock
        if end > numTokens {
            end = numTokens
        }
        // Create coins for this block's transfers
        for j := i; j < end; j++ {
            denom := fmt.Sprintf("ibc/%d", j)
            coin := sdk.NewInt64Coin(denom, 1)
            blockCoins = blockCoins.Add(coin)
// ... (truncated)
```

**Variant: Dos Deposit Spam - HIGH Severity Cases** [HIGH]
> Found in 2 reports:
> - `reports/cosmos_cometbft_findings/unmetered-balance-iteration-in-reward-termination-can-be-exploited-to-permission.md`
> - `reports/cosmos_cometbft_findings/unmetered-beginblock-iteration-over-balances-exposes-low-cost-on-demand-chain-ha.md`

**Variant: Dos Deposit Spam in MilkyWay** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/unmetered-balance-iteration-in-reward-termination-can-be-exploited-to-permission.md`
> - `reports/cosmos_cometbft_findings/unmetered-beginblock-iteration-over-balances-exposes-low-cost-on-demand-chain-ha.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in dos deposit spam logic allows exploitation through missing validation, incorr
func secureDosDepositSpam(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 6 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 4
- **Affected Protocols**: Berachain Beaconkit, DIA, MilkyWay, Kinetiq, Berachain
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Dos Block Production Halt
grep -rn 'dos|block|production|halt' --include='*.go' --include='*.sol'
# Dos Consensus Halt
grep -rn 'dos|consensus|halt' --include='*.go' --include='*.sol'
# Dos State Machine
grep -rn 'dos|state|machine' --include='*.go' --include='*.sol'
# Dos Unbounded Beginblock
grep -rn 'dos|unbounded|beginblock' --include='*.go' --include='*.sol'
# Dos Unbounded Array
grep -rn 'dos|unbounded|array' --include='*.go' --include='*.sol'
# Dos Panic Crash
grep -rn 'dos|panic|crash' --include='*.go' --include='*.sol'
# Dos Message Flooding
grep -rn 'dos|message|flooding' --include='*.go' --include='*.sol'
# Dos Deposit Spam
grep -rn 'dos|deposit|spam' --include='*.go' --include='*.sol'
```

## Keywords

`abci`, `allow`, `allows`, `amount`, `appchain`, `array`, `attacks`, `balances`, `ballot`, `been`, `beginblock`, `blob`, `block`, `blocks`, `blocksync`, `cause`, `causes`, `censorship`, `chain`, `consensus`, `cosmos`, `crash`, `creation`, `crisis`, `denial`, `deposit`, `deposits`, `dos`, `during`, `economic`

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`TestAllocateRewards_RewardsPlanFlood`, `TestAllocateRewards_TokenFlood`, `TestTerminateEndedRewardsPlan_TokenFlood`, `_calculateChallengerEligibility`, `appchain`, `balance`, `block_production_halt`, `chain_halt_consensus_dos`, `consensus_halt`, `cosmos`, `defi`, `deposit`, `deposit_spam`, `dos`, `message_flooding`, `panic_crash`, `proposal_spam`, `staking`, `state_machine`, `such`, `unbounded_array`, `unbounded_beginblock`, `unbounded_endblock`, `verifyDoubleSigning`
