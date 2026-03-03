---
protocol: generic
chain: cosmos
category: consensus
vulnerability_type: consensus_finality_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: consensus_logic

primitives:
  - proposer_dos
  - finality_bypass
  - reorg
  - vote_extension
  - block_sync
  - non_determinism
  - proposer_selection
  - equivocation
  - liveness

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - consensus
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Consensus Proposer Dos
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| AnteHandler Skipped In Non-CheckTx Mode | `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md` | HIGH | OtterSec |
| Block Proposer DDoS | `reports/cosmos_cometbft_findings/block-proposer-ddos.md` | MEDIUM | TrailOfBits |
| Malicious proposer can submit a request with large invalid t | `reports/cosmos_cometbft_findings/h-10-malicious-proposer-can-submit-a-request-with-large-invalid-transactions-bec.md` | HIGH | Sherlock |
| Incorrect Injected Vote Extensions Validation | `reports/cosmos_cometbft_findings/incorrect-injected-vote-extensions-validation.md` | HIGH | OtterSec |
| Lack Of Signature Verification | `reports/cosmos_cometbft_findings/lack-of-signature-verification.md` | HIGH | OtterSec |
| Malicious proposer can include additional transactions in Be | `reports/cosmos_cometbft_findings/malicious-proposer-can-include-additional-transactions-in-beaconblock.md` | MEDIUM | Cantina |
| static_validate_system_transaction missing EIP-155 chain ID  | `reports/cosmos_cometbft_findings/static_validate_system_transaction-missing-eip-155-chain-id-validation.md` | HIGH | Spearbit |
| Unvalidated ExecutionPayload.Timestamp can halt chain | `reports/cosmos_cometbft_findings/unvalidated-executionpayloadtimestamp-can-halt-chain.md` | HIGH | Spearbit |

### Consensus Finality Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| RocketMinipoolDelegate - Redundant refund() call on forced f | `reports/cosmos_cometbft_findings/rocketminipooldelegate-redundant-refund-call-on-forced-finalization-fixed.md` | MEDIUM | ConsenSys |

### Consensus Reorg
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Consensus on staking transaction status can be bricked in ca | `reports/cosmos_cometbft_findings/consensus-on-staking-transaction-status-can-be-bricked-in-case-of-bitcoin-reorg-.md` | MEDIUM | Cantina |
| [M-08] Factory::create() is vulnerable to reorg attacks | `reports/cosmos_cometbft_findings/m-08-factorycreate-is-vulnerable-to-reorg-attacks.md` | MEDIUM | Code4rena |

### Consensus Vote Extension
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect Injected Vote Extensions Validation | `reports/cosmos_cometbft_findings/incorrect-injected-vote-extensions-validation.md` | HIGH | OtterSec |
| Lack Of Signature Verification | `reports/cosmos_cometbft_findings/lack-of-signature-verification.md` | HIGH | OtterSec |
| Mismatch Between CometBFT and Application Views | `reports/cosmos_cometbft_findings/mismatch-between-cometbft-and-application-views.md` | MEDIUM | OtterSec |
| Vote Extension Risks | `reports/cosmos_cometbft_findings/vote-extension-risks.md` | HIGH | OtterSec |

### Consensus Block Sync
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-03] Attacker Can Desynchronize Supply Snapshot During Sam | `reports/cosmos_cometbft_findings/m-03-attacker-can-desynchronize-supply-snapshot-during-same-block-unstake-reduci.md` | MEDIUM | Code4rena |
| Malicious peer can cause a syncing node to panic during bloc | `reports/cosmos_cometbft_findings/m-8-malicious-peer-can-cause-a-syncing-node-to-panic-during-blocksync.md` | MEDIUM | Sherlock |

### Consensus Non Determinism
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| BlobSidecars data availability race condition | `reports/cosmos_cometbft_findings/blobsidecars-data-availability-race-condition.md` | MEDIUM | Spearbit |
| Use of Vulnerable IBC-Go v8.4.0 - Non-Deterministic JSON Unm | `reports/cosmos_cometbft_findings/h-7-use-of-vulnerable-ibc-go-v840-non-deterministic-json-unmarshalling-can-cause.md` | HIGH | Sherlock |
| Potential Non-Determinism Issue In FinalizeBlock | `reports/cosmos_cometbft_findings/potential-non-determinism-issue-in-finalizeblock.md` | MEDIUM | Halborn |

### Consensus Proposer Selection
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing highestVotingPower Update in argmaxBlockByStake Resu | `reports/cosmos_cometbft_findings/h-6-missing-highestvotingpower-update-in-argmaxblockbystake-resulting-in-incorre.md` | HIGH | Sherlock |
| Mismatch between proposer selection algorithm | `reports/cosmos_cometbft_findings/mismatch-between-proposer-selection-algorithm.md` | HIGH | Halborn |

### Consensus Equivocation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Denial Of Slashing | `reports/cosmos_cometbft_findings/denial-of-slashing.md` | HIGH | OtterSec |
| Deprecated GetSigners Usage | `reports/cosmos_cometbft_findings/deprecated-getsigners-usage.md` | HIGH | OtterSec |
| Btcstaking module allows `stakingTx` to be coinbase transact | `reports/cosmos_cometbft_findings/m-1-btcstaking-module-allows-stakingtx-to-be-coinbase-transaction-which-is-unsla.md` | MEDIUM | Sherlock |
| [M-17] Wrong slashing calculation rewards for operator that  | `reports/cosmos_cometbft_findings/m-17-wrong-slashing-calculation-rewards-for-operator-that-did-not-do-his-job.md` | MEDIUM | Code4rena |
| Risk of double-spend attacks due to use of single-node Cliqu | `reports/cosmos_cometbft_findings/risk-of-double-spend-attacks-due-to-use-of-single-node-clique-consensus-without-.md` | MEDIUM | TrailOfBits |
| Slashing of re-delegated stake is computed incorrectly | `reports/cosmos_cometbft_findings/slashing-of-re-delegated-stake-is-computed-incorrectly.md` | MEDIUM | TrailOfBits |

### Consensus Liveness
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Lack of validator penalties enables risk-free economic censo | `reports/cosmos_cometbft_findings/lack-of-validator-penalties-enables-risk-free-economic-censorship-and-liveness-a.md` | MEDIUM | Spearbit |

---

# Consensus Finality Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Consensus Finality Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Consensus Proposer Dos](#1-consensus-proposer-dos)
2. [Consensus Finality Bypass](#2-consensus-finality-bypass)
3. [Consensus Reorg](#3-consensus-reorg)
4. [Consensus Vote Extension](#4-consensus-vote-extension)
5. [Consensus Block Sync](#5-consensus-block-sync)
6. [Consensus Non Determinism](#6-consensus-non-determinism)
7. [Consensus Proposer Selection](#7-consensus-proposer-selection)
8. [Consensus Equivocation](#8-consensus-equivocation)
9. [Consensus Liveness](#9-consensus-liveness)

---

## 1. Consensus Proposer Dos

### Overview

Implementation flaw in consensus proposer dos logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 10 audit reports with severity distribution: HIGH: 7, MEDIUM: 3.

> **Key Finding**: The Cosmos AnteHandlers are used to check the validity of transactions and prevent malicious transactions from being executed. However, some of the validators are skipped when not in CheckTx mode, allowing attackers to insert malformed transactions into block proposals. This can lead to incorrect ex

### Vulnerability Description

#### Root Cause

Implementation flaw in consensus proposer dos logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies consensus proposer dos in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to consensus operations

### Vulnerable Pattern Examples

**Example 1: AnteHandler Skipped In Non-CheckTx Mode** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md`
```go
// sei-tendermint/internal/mempool/mempool.go
func (fc EVMFeeCheckDecorator) AnteHandle(ctx sdk.Context, tx sdk.Tx, simulate bool, next sdk.AnteHandler) (sdk.Context, error) {
    // Only check fee in CheckTx (similar to normal Sei tx)
    if !ctx.IsCheckTx() || simulate {
        return next(ctx, tx, simulate)
    }
    [...]
    anteCharge := txData.Cost()
    senderEVMAddr := evmtypes.MustGetEVMTransactionMessage(tx).Derived.SenderEVMAddr
    if state.NewDBImpl(ctx, fc.evmKeeper, true).GetBalance(senderEVMAddr).Cmp(anteCharge) < 0 {
        return ctx, sdkerrors.ErrInsufficientFunds
    }
    [...]
}
```

**Example 2: Block Proposer DDoS** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/block-proposer-ddos.md`
```
// Vulnerable pattern from Prysm:
## Diﬃculty: High
```

**Example 3: Malicious proposer can submit a request with large invalid transactions because ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-10-malicious-proposer-can-submit-a-request-with-large-invalid-transactions-bec.md`
```
// Vulnerable pattern from SEDA Protocol:
Source: https://github.com/sherlock-audit/2024-12-seda-protocol-judging/issues/241
```

**Example 4: Incorrect Injected Vote Extensions Validation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/incorrect-injected-vote-extensions-validation.md`
```go
// Sample code for ValidateVoteExtensions function
func ValidateVoteExtensions(
[...]
) error {
    cp := ctx.ConsensusParams()
    // Start checking vote extensions only **after** the vote extensions enable height,
    // because when `currentHeight == VoteExtensionsEnableHeight`
    // PrepareProposal doesn't get any vote extensions in its request.
    extsEnabled := cp.Abci != nil && currentHeight > cp.Abci.VoteExtensionsEnableHeight &&
    cp.Abci.VoteExtensionsEnableHeight != 0

    marshalDelimitedFn := func(msg proto.Message) ([]byte, error) {
        var buf bytes.Buffer
        if err := protoio.NewDelimitedWriter(&buf).WriteMsg(msg); err != nil {
            return nil, err
        }
        return buf.Bytes(), nil
    }

    var (
        // Total voting power of all vote extensions.
        totalVP int64
        // Total voting power of all validators that submitted valid vote extensions.
        sumVP int64
    )
    [...]
}
```

**Example 5: Malicious proposer can include additional transactions in BeaconBlock** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/malicious-proposer-can-include-additional-transactions-in-beaconblock.md`
```go
// Iterate over all raw transactions in the proposal and attempt to execute
// them, gathering the execution results.
//
// NOTE: Not all raw transactions may adhere to the sdk.Tx interface, e.g.
// vote extensions, so skip those.
txResults := make([]*cmtabci.ExecTxResult, len(req.Txs))
for i := range req.Txs {
    //nolint:mnd // its okay for now.
    txResults[i] = &cmtabci.ExecTxResult{
        Codespace: "sdk",
        Code: 2,
        Log: "skip decoding",
        GasWanted: 0,
        GasUsed: 0,
    }
}
```

**Variant: Consensus Proposer Dos - MEDIUM Severity Cases** [MEDIUM]
> Found in 3 reports:
> - `reports/cosmos_cometbft_findings/block-proposer-ddos.md`
> - `reports/cosmos_cometbft_findings/malicious-proposer-can-include-additional-transactions-in-beaconblock.md`
> - `reports/cosmos_cometbft_findings/unvalidated-proposerindex-in-beaconblock.md`

**Variant: Consensus Proposer Dos in Ethos Cosmos** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/incorrect-injected-vote-extensions-validation.md`
> - `reports/cosmos_cometbft_findings/lack-of-signature-verification.md`

**Variant: Consensus Proposer Dos in Berachain Beaconkit** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/unvalidated-executionpayloadtimestamp-can-halt-chain.md`
> - `reports/cosmos_cometbft_findings/unvalidated-proposerindex-in-beaconblock.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in consensus proposer dos logic allows exploitation through missing validation, 
func secureConsensusProposerDos(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 10 audit reports
- **Severity Distribution**: HIGH: 7, MEDIUM: 3
- **Affected Protocols**: Ethos Cosmos, Berachain Beaconkit, Cosmos SDK, Prysm, Sei EVM
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Consensus Finality Bypass

### Overview

Implementation flaw in consensus finality bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report is about an issue with the `RocketMinipoolDelegate.refund` function in the code of the RocketPool project. The function will force finalization if a user previously distributed the pool, however, the `_finalise()` function already calls `_refund()` if there is a node refund balance t

### Vulnerability Description

#### Root Cause

Implementation flaw in consensus finality bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies consensus finality bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to consensus operations

### Vulnerable Pattern Examples

**Example 1: RocketMinipoolDelegate - Redundant refund() call on forced finalization ✓ Fixed** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/rocketminipooldelegate-redundant-refund-call-on-forced-finalization-fixed.md`
```solidity
function refund() override external onlyMinipoolOwnerOrWithdrawalAddress(msg.sender) onlyInitialised {
    // Check refund balance
    require(nodeRefundBalance > 0, "No amount of the node deposit is available for refund");
    // If this minipool was distributed by a user, force finalisation on the node operator
    if (!finalised && userDistributed) {
        \_finalise();
    }
    // Refund node
    \_refund();
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in consensus finality bypass logic allows exploitation through missing validatio
func secureConsensusFinalityBypass(ctx sdk.Context) error {
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
- **Affected Protocols**: Rocket Pool Atlas (v1.2)
- **Validation Strength**: Single auditor

---

## 3. Consensus Reorg

### Overview

Implementation flaw in consensus reorg logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: This bug report discusses a potential issue with the Staking-Indexer, a tool used to manage staking transactions in the Bitcoin network. The report explains that while the tool is generally robust against minor reorganizations of the blockchain, major reorganizations (of 20 blocks or more) are rare 

### Vulnerability Description

#### Root Cause

Implementation flaw in consensus reorg logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies consensus reorg in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to consensus operations

### Vulnerable Pattern Examples

**Example 1: Consensus on staking transaction status can be bricked in case of Bitcoin reorg ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/consensus-on-staking-transaction-status-can-be-bricked-in-case-of-bitcoin-reorg-.md`
```go
BTCNode1: genesis -> bA(0) -> bB(1) -> bC(2) -> bD(3) -> bE(4) -> bF(5) -> bG(6) (good chain)
BTCNode2: -> bH(3) -> bI(4) -> bJ(5) -> bK(6) (bad chain)
```

**Example 2: [M-08] Factory::create() is vulnerable to reorg attacks** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-08-factorycreate-is-vulnerable-to-reorg-attacks.md`
```solidity
function create(address baseToken_, address quoteToken_, uint256 lpFeeRate_, uint256 i_, uint256 k_) external returns (address clone) {
        address creator = tx.origin;

        bytes32 salt = _computeSalt(creator, baseToken_, quoteToken_, lpFeeRate_, i_, k_);
        clone = LibClone.cloneDeterministic(address(implementation), salt);
        IMagicLP(clone).init(address(baseToken_), address(quoteToken_), lpFeeRate_, address(maintainerFeeRateModel), i_, k_);

        emit LogCreated(clone, baseToken_, quoteToken_, creator, lpFeeRate_, maintainerFeeRateModel, i_, k_);
        _addPool(creator, baseToken_, quoteToken_, clone);
    }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in consensus reorg logic allows exploitation through missing validation, incorre
func secureConsensusReorg(ctx sdk.Context) error {
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
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: Abracadabra Money, Babylonchain
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Consensus Vote Extension

### Overview

Implementation flaw in consensus vote extension logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 3, MEDIUM: 1.

> **Key Finding**: The bug report is about a function called ValidateVoteExtensions that relies on data injected by the proposer, which can be manipulated to misrepresent the voting power of validators. This can lead to incorrect consensus decisions and compromised voting process. The report recommends applying a patc

### Vulnerability Description

#### Root Cause

Implementation flaw in consensus vote extension logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies consensus vote extension in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to consensus operations

### Vulnerable Pattern Examples

**Example 1: Incorrect Injected Vote Extensions Validation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/incorrect-injected-vote-extensions-validation.md`
```go
// Sample code for ValidateVoteExtensions function
func ValidateVoteExtensions(
[...]
) error {
    cp := ctx.ConsensusParams()
    // Start checking vote extensions only **after** the vote extensions enable height,
    // because when `currentHeight == VoteExtensionsEnableHeight`
    // PrepareProposal doesn't get any vote extensions in its request.
    extsEnabled := cp.Abci != nil && currentHeight > cp.Abci.VoteExtensionsEnableHeight &&
    cp.Abci.VoteExtensionsEnableHeight != 0

    marshalDelimitedFn := func(msg proto.Message) ([]byte, error) {
        var buf bytes.Buffer
        if err := protoio.NewDelimitedWriter(&buf).WriteMsg(msg); err != nil {
            return nil, err
        }
        return buf.Bytes(), nil
    }

    var (
        // Total voting power of all vote extensions.
        totalVP int64
        // Total voting power of all validators that submitted valid vote extensions.
        sumVP int64
    )
    [...]
}
```

**Example 2: Lack Of Signature Verification** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-signature-verification.md`
```go
// Code snippet from the context
func FindSuperMajorityVoteExtension(ctx context.Context, currentHeight int64, extCommit abci.ExtendedCommitInfo, valStore baseapp.ValidatorStore, chainID string) (types.VoteExtension, error) {
    // Check if the max voting power is greater than 2/3 of the total voting power
    if requiredVP := ((totalVP * 2) / 3) + 1; maxVotingPower < requiredVP {
        return types.VoteExtension{}, fmt.Errorf("%d < %d: %w", maxVotingPower, requiredVP, types.ErrInsufficientVotingPowerVE)
    }

    var voteExt types.VoteExtension
    err := json.Unmarshal(highestVoteExtensionBz, &voteExt)
    if err != nil {
        return types.VoteExtension{}, err
    }

    // Verify the super majority VE has valid values
    if (voteExt.EthBlockHeight == 0) || (voteExt.EthBlockHash == common.Hash{}) {
        return types.VoteExtension{}, fmt.Errorf("super majority VE is invalid")
    }
    return voteExt, nil
}
```

**Example 3: Mismatch Between CometBFT and Application Views** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/mismatch-between-cometbft-and-application-views.md`
```
// Vulnerable pattern from Skip Slinky Oracle:
## Comet BFT’s View of Validators

Comet BFT’s view of validators differs from the application’s view, making it imperative to handle and utilize these views appropriately. Failure to appropriately manage these disparate views can lead to unintended liveness issues.
```

**Example 4: Vote Extension Risks** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/vote-extension-risks.md`
```go
func ValidateVoteExtensions(
       ctx sdk.Context,
       valStore ValidatorStore,
       currentHeight int64,
       chainID string,
       extCommit abci.ExtendedCommitInfo,
   ) error {
       [...]
       for _, vote := range extCommit.Votes {
           totalVP += vote.Validator.Power
           [...]
       }
       [...]
   }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in consensus vote extension logic allows exploitation through missing validation
func secureConsensusVoteExtension(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 3, MEDIUM: 1
- **Affected Protocols**: Cosmos SDK, Skip Slinky Oracle, Ethos Cosmos
- **Validation Strength**: Single auditor

---

## 5. Consensus Block Sync

### Overview

Implementation flaw in consensus block sync logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: This bug report discusses a vulnerability in the Cabal token contract that allows an attacker to manipulate the supply and reward distribution of the token. By initiating an unstake transaction in the same block as the manager's snapshot, the attacker can exploit flaws in the contract to artificiall

### Vulnerability Description

#### Root Cause

Implementation flaw in consensus block sync logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies consensus block sync in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to consensus operations

### Vulnerable Pattern Examples

**Example 1: [M-03] Attacker Can Desynchronize Supply Snapshot During Same-Block Unstake, Red** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-attacker-can-desynchronize-supply-snapshot-during-same-block-unstake-reduci.md`
```
// Vulnerable pattern from Cabal:
<https://github.com/code-423n4/2025-04-cabal/blob/5b5f92ab4f95e5f9f405bbfa252860472d164705/sources/cabal_token.move# L219-L227>

### Finding description and impact

An attacker holding Cabal LSTs (like sxINIT) can monitor the mempool for the manager’s `voting_reward::snapshot()` transaction. By submitting his own `cabal::initiate_unstake` transaction to execute in the *same block* (`H`) as the manager’s snapshot, the attacker can use two flaws:

1. `cabal_token::burn` (called by their unstake) d
```

**Example 2: Malicious peer can cause a syncing node to panic during blocksync** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-8-malicious-peer-can-cause-a-syncing-node-to-panic-during-blocksync.md`
```
// Vulnerable pattern from Allora:
Source: https://github.com/sherlock-audit/2024-06-allora-judging/issues/28
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in consensus block sync logic allows exploitation through missing validation, in
func secureConsensusBlockSync(ctx sdk.Context) error {
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
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: Cabal, Allora
- **Validation Strength**: Moderate (2 auditors)

---

## 6. Consensus Non Determinism

### Overview

Implementation flaw in consensus non determinism logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: This bug report describes a race condition that occurs when processing a block in the CometBFT system. Two event handlers, handleBeaconBlockFinalization() and handleFinalSidecarsReceived(), run in parallel and can cause a non-deterministic outcome when accessing the AvailabilityStore. This can lead 

### Vulnerability Description

#### Root Cause

Implementation flaw in consensus non determinism logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies consensus non determinism in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to consensus operations

### Vulnerable Pattern Examples

**Example 1: BlobSidecars data availability race condition** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/blobsidecars-data-availability-race-condition.md`
```
// Vulnerable pattern from Berachain Beaconkit:
## Medium Risk Severity Report

**Context:** `beacon/blockchain/process.go#L74-L78`
```

**Example 2: Use of Vulnerable IBC-Go v8.4.0 - Non-Deterministic JSON Unmarshalling Can Cause** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-7-use-of-vulnerable-ibc-go-v840-non-deterministic-json-unmarshalling-can-cause.md`
```
// Vulnerable pattern from SEDA Protocol:
Source: https://github.com/sherlock-audit/2024-12-seda-protocol-judging/issues/222
```

**Example 3: Potential Non-Determinism Issue In FinalizeBlock** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/potential-non-determinism-issue-in-finalizeblock.md`
```go
// FinalizeBlock calls BeginBlock -> DeliverTx (for all txs) -> EndBlock.
func (l abciWrapper) FinalizeBlock(ctx context.Context, req *abci.RequestFinalizeBlock) (*abci.ResponseFinalizeBlock, error) {

	...

	if err := l.postFinalize(sdkCtx); err != nil {
		log.Error(ctx, "PostFinalize callback failed [BUG]", err, "height", req.Height)
		return resp, err
	}

        ...
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in consensus non determinism logic allows exploitation through missing validatio
func secureConsensusNonDeterminism(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 2
- **Affected Protocols**: Layer 1 Assessment, SEDA Protocol, Berachain Beaconkit
- **Validation Strength**: Strong (3+ auditors)

---

## 7. Consensus Proposer Selection

### Overview

Implementation flaw in consensus proposer selection logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: This bug report discusses an issue with the argmaxBlockByStake function, which is used to identify the block height with the highest cumulative voting power based on the stakes of voting reputers. The calculation for highestVotingPower is flawed, as it fails to update when a new block with higher vo

### Vulnerability Description

#### Root Cause

Implementation flaw in consensus proposer selection logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies consensus proposer selection in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to consensus operations

### Vulnerable Pattern Examples

**Example 1: Missing highestVotingPower Update in argmaxBlockByStake Resulting in Incorrect B** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-6-missing-highestvotingpower-update-in-argmaxblockbystake-resulting-in-incorre.md`
```go
func (ap *AppChain) argmaxBlockByStake(
	blockToReputer *map[int64][]string,
	stakesPerReputer map[string]cosmossdk_io_math.Int,
) int64 {
	// Find the current block height with the highest voting power
	firstIter := true
	highestVotingPower := cosmossdk_io_math.ZeroInt()
	blockOfMaxPower := int64(-1)
	for block, reputersWhoVotedForBlock := range *blockToReputer {
		// Calc voting power of this candidate block by total voting reputer stake
		blockVotingPower := cosmossdk_io_math.ZeroInt()
		for _, reputerAddr := range reputersWhoVotedForBlock {
			blockVotingPower = blockVotingPower.Add(stakesPerReputer[reputerAddr])
		}

		// Decide if voting power exceeds that of current front-runner
		if firstIter || blockVotingPower.GT(highestVotingPower) {
@>			blockOfMaxPower = block // Correctly updates the block
@>			// Missing highestVotingPower = blockVotingPower
		}

		firstIter = false
	}

	return blockOfMaxPower
}
```

**Example 2: Mismatch between proposer selection algorithm** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/mismatch-between-proposer-selection-algorithm.md`
```go
// isNextProposer returns true if the local node is the proposer
// for the next block. It also returns the next block height.
//
// Note that the validator set can change, so this is an optimistic check.
func (k *Keeper) isNextProposer(ctx context.Context, currentProposer []byte, currentHeight int64) (bool, error) {
	// PostFinalize can be called during block replay (performed in newCometNode),
	// but cmtAPI is set only after newCometNode completes (see app.SetCometAPI), so a nil check is necessary.
	if k.cmtAPI == nil {
		return false, nil
	}

	valset, ok, err := k.cmtAPI.Validators(ctx, currentHeight)
	if err != nil {
		return false, err
	} else if !ok || len(valset.Validators) == 0 {
		return false, errors.New("validators not available")
	}

	idx, _ := valset.GetByAddress(currentProposer)
	if idx < 0 {
		return false, errors.New("proposer not in validator set")
	}

	nextIdx := int(idx+1) % len(valset.Validators)
	nextProposer := valset.Validators[nextIdx]
	nextAddr, err := k1util.PubKeyToAddress(nextProposer.PubKey)
	if err != nil {
		return false, err
	}

	isNextProposer := nextAddr == k.validatorAddr

	return isNextProposer, nil
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in consensus proposer selection logic allows exploitation through missing valida
func secureConsensusProposerSelection(ctx sdk.Context) error {
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
- **Affected Protocols**: Layer 1 Assessment, Allora
- **Validation Strength**: Moderate (2 auditors)

---

## 8. Consensus Equivocation

### Overview

Implementation flaw in consensus equivocation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 2, MEDIUM: 4.

> **Key Finding**: This report discusses a vulnerability in the verifyDoubleSigning function, which can be exploited by a malicious operator to evade slashing. This vulnerability is due to the linear complexity of the function, which can be increased indefinitely by repeatedly calling the updateDelegation function. Th

### Vulnerability Description

#### Root Cause

Implementation flaw in consensus equivocation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies consensus equivocation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to consensus operations

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

**Example 2: Deprecated GetSigners Usage** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/deprecated-getsigners-usage.md`
```go
// File: ethos-chain/x/ccv/provider/types/msg.go
func (msg MsgSubmitConsumerMisbehaviour) GetSigners() []sdk.AccAddress {
    addr, err := sdk.AccAddressFromBech32(msg.Submitter)
    if err != nil {
        // same behavior as in cosmos-sdk
        panic(err)
    }
    return []sdk.AccAddress{addr}
}

func (msg MsgSubmitConsumerDoubleVoting) GetSigners() []sdk.AccAddress {
    addr, err := sdk.AccAddressFromBech32(msg.Submitter)
    if err != nil {
        // same behavior as in cosmos-sdk
        panic(err)
    }
    return []sdk.AccAddress{addr}
}
```

**Example 3: Btcstaking module allows `stakingTx` to be coinbase transaction which is unslash** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-btcstaking-module-allows-stakingtx-to-be-coinbase-transaction-which-is-unsla.md`
```
// Vulnerable pattern from Babylon chain launch (phase-2):
Source: https://github.com/sherlock-audit/2024-12-babylon-judging/issues/6
```

**Example 4: [M-17] Wrong slashing calculation rewards for operator that did not do his job** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-17-wrong-slashing-calculation-rewards-for-operator-that-did-not-do-his-job.md`
```
// Vulnerable pattern from Holograph:
Wrong slashing calculation may create unfair punishment for operators that accidentally forgot to execute their job.

### Proof of Concept

[Docs](https://docs.holograph.xyz/holograph-protocol/operator-network-specification): If an operator acts maliciously, a percentage of their bonded HLG will get slashed. Misbehavior includes (i) downtime, (ii) double-signing transactions, and (iii) abusing transaction speeds. 50% of the slashed HLG will be rewarded to the next operator to execute the transac
```

**Example 5: Risk of double-spend attacks due to use of single-node Clique consensus without ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/risk-of-double-spend-attacks-due-to-use-of-single-node-clique-consensus-without-.md`
```
// Vulnerable pattern from Scroll, l2geth:
## Diﬃculty: Medium
```

**Variant: Consensus Equivocation - MEDIUM Severity Cases** [MEDIUM]
> Found in 4 reports:
> - `reports/cosmos_cometbft_findings/m-1-btcstaking-module-allows-stakingtx-to-be-coinbase-transaction-which-is-unsla.md`
> - `reports/cosmos_cometbft_findings/m-17-wrong-slashing-calculation-rewards-for-operator-that-did-not-do-his-job.md`
> - `reports/cosmos_cometbft_findings/risk-of-double-spend-attacks-due-to-use-of-single-node-clique-consensus-without-.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in consensus equivocation logic allows exploitation through missing validation, 
func secureConsensusEquivocation(ctx sdk.Context) error {
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
- **Affected Protocols**: Scroll, l2geth, Ethos Cosmos, Orga and Merk, Ethos EVM, Holograph
- **Validation Strength**: Strong (3+ auditors)

---

## 9. Consensus Liveness

### Overview

Implementation flaw in consensus liveness logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The bug report discusses issues with the current economic security and consensus safety model in the mod/state-transition/pkg/core/state_processor.go file. The report notes that the current model allows for easy bypassing of deposit barriers and has no penalties or slashing mechanisms. This can lead

### Vulnerability Description

#### Root Cause

Implementation flaw in consensus liveness logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies consensus liveness in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to consensus operations

### Vulnerable Pattern Examples

**Example 1: Lack of validator penalties enables risk-free economic censorship and liveness a** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-validator-penalties-enables-risk-free-economic-censorship-and-liveness-a.md`
```
// Vulnerable pattern from Berachain Beaconkit:
## Severity: Medium Risk
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in consensus liveness logic allows exploitation through missing validation, inco
func secureConsensusLiveness(ctx sdk.Context) error {
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
- **Affected Protocols**: Berachain Beaconkit
- **Validation Strength**: Single auditor

---

## Detection Patterns

### Automated Detection
```
# Consensus Proposer Dos
grep -rn 'consensus|proposer|dos' --include='*.go' --include='*.sol'
# Consensus Finality Bypass
grep -rn 'consensus|finality|bypass' --include='*.go' --include='*.sol'
# Consensus Reorg
grep -rn 'consensus|reorg' --include='*.go' --include='*.sol'
# Consensus Vote Extension
grep -rn 'consensus|vote|extension' --include='*.go' --include='*.sol'
# Consensus Block Sync
grep -rn 'consensus|block|sync' --include='*.go' --include='*.sol'
# Consensus Non Determinism
grep -rn 'consensus|non|determinism' --include='*.go' --include='*.sol'
# Consensus Proposer Selection
grep -rn 'consensus|proposer|selection' --include='*.go' --include='*.sol'
# Consensus Equivocation
grep -rn 'consensus|equivocation' --include='*.go' --include='*.sol'
# Consensus Liveness
grep -rn 'consensus|liveness' --include='*.go' --include='*.sol'
```

## Keywords

`algorithm`, `allows`, `antehandler`, `appchain`, `application`, `argmaxblockbystake`, `attacker`, `attacks`, `availability`, `because`, `between`, `bitcoin`, `bloat`, `blobsidecars`, `block`, `blocks`, `blocksync`, `bricked`, `btcstaking`, `bypass`, `call`, `case`, `cause`, `censorship`, `chain`, `coinbase`, `cometbft`, `condition`, `configurationdepth`, `consensus`
