---
protocol: generic
chain: cosmos
category: abci_lifecycle
vulnerability_type: abci_lifecycle_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: abci_lifecycle_logic

primitives:
  - beginblock_error
  - endblock_error
  - checktx_bypass
  - prepare_process
  - vote_extension_abuse
  - finalize_block

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - abci_lifecycle
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Abci Endblock Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| RemoveStakes and RemoveDelegateStakes silently handle errors | `reports/cosmos_cometbft_findings/h-7-removestakes-and-removedelegatestakes-silently-handle-errors-in-endblocker.md` | HIGH | Sherlock |
| The issue of SLOW ABCI METHODS has not been resolved. | `reports/cosmos_cometbft_findings/m-28-the-issue-of-slow-abci-methods-has-not-been-resolved.md` | MEDIUM | Sherlock |

### Abci Checktx Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| AnteHandler Skipped In Non-CheckTx Mode | `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md` | HIGH | OtterSec |

### Abci Vote Extension Abuse
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect Injected Vote Extensions Validation | `reports/cosmos_cometbft_findings/incorrect-injected-vote-extensions-validation.md` | HIGH | OtterSec |
| Lack Of Signature Verification | `reports/cosmos_cometbft_findings/lack-of-signature-verification.md` | HIGH | OtterSec |
| Vote Extension Risks | `reports/cosmos_cometbft_findings/vote-extension-risks.md` | HIGH | OtterSec |

### Abci Finalize Block
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-02] A regular Cosmos SDK message can be disguised as an E | `reports/cosmos_cometbft_findings/h-02-a-regular-cosmos-sdk-message-can-be-disguised-as-an-evm-transaction-causing.md` | HIGH | Code4rena |
| Potential Non-Determinism Issue In FinalizeBlock | `reports/cosmos_cometbft_findings/potential-non-determinism-issue-in-finalizeblock.md` | MEDIUM | Halborn |

---

# Abci Lifecycle Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Abci Lifecycle Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Abci Endblock Error](#1-abci-endblock-error)
2. [Abci Checktx Bypass](#2-abci-checktx-bypass)
3. [Abci Vote Extension Abuse](#3-abci-vote-extension-abuse)
4. [Abci Finalize Block](#4-abci-finalize-block)

---

## 1. Abci Endblock Error

### Overview

Implementation flaw in abci endblock error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: The bug report highlights an issue with the RemoveStakes and RemoveDelegateStakes functions in the Allora network's code. These functions are responsible for removing stakes from users' accounts. The bug allows for errors to occur during the removal process, which can result in an inconsistent state

### Vulnerability Description

#### Root Cause

Implementation flaw in abci endblock error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies abci endblock error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to abci operations

### Vulnerable Pattern Examples

**Example 1: RemoveStakes and RemoveDelegateStakes silently handle errors in EndBlocker** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-7-removestakes-and-removedelegatestakes-silently-handle-errors-in-endblocker.md`
```go
[RemoveStakes](https://github.com/sherlock-audit/2024-06-allora/blob/main/allora-chain/x/emissions/module/stake_removals.go#L13-L63)
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

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in abci endblock error logic allows exploitation through missing validation, inc
func secureAbciEndblockError(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 1
- **Affected Protocols**: Allora
- **Validation Strength**: Single auditor

---

## 2. Abci Checktx Bypass

### Overview

Implementation flaw in abci checktx bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: The Cosmos AnteHandlers are used to check the validity of transactions and prevent malicious transactions from being executed. However, some of the validators are skipped when not in CheckTx mode, allowing attackers to insert malformed transactions into block proposals. This can lead to incorrect ex

### Vulnerability Description

#### Root Cause

Implementation flaw in abci checktx bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies abci checktx bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to abci operations

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

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in abci checktx bypass logic allows exploitation through missing validation, inc
func secureAbciChecktxBypass(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1
- **Affected Protocols**: Sei EVM
- **Validation Strength**: Single auditor

---

## 3. Abci Vote Extension Abuse

### Overview

Implementation flaw in abci vote extension abuse logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 3.

> **Key Finding**: The bug report is about a function called ValidateVoteExtensions that relies on data injected by the proposer, which can be manipulated to misrepresent the voting power of validators. This can lead to incorrect consensus decisions and compromised voting process. The report recommends applying a patc

### Vulnerability Description

#### Root Cause

Implementation flaw in abci vote extension abuse logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies abci vote extension abuse in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to abci operations

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

**Example 3: Vote Extension Risks** [HIGH]
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
// Addresses: Implementation flaw in abci vote extension abuse logic allows exploitation through missing validatio
func secureAbciVoteExtensionAbuse(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 3
- **Affected Protocols**: Cosmos SDK, Ethos Cosmos
- **Validation Strength**: Single auditor

---

## 4. Abci Finalize Block

### Overview

Implementation flaw in abci finalize block logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: This bug report discusses an issue with the `ListenFinalizeBlock()` function in the `txutils.go` file of the `minievm` repository. This function is called when a block is finalized and processes the transactions. The problem occurs when the function tries to extract logs and a contract address from 

### Vulnerability Description

#### Root Cause

Implementation flaw in abci finalize block logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies abci finalize block in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to abci operations

### Vulnerable Pattern Examples

**Example 1: [H-02] A regular Cosmos SDK message can be disguised as an EVM transaction, caus** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-a-regular-cosmos-sdk-message-can-be-disguised-as-an-evm-transaction-causing.md`
```go
func (app *BaseApp) FinalizeBlock(req *abci.RequestFinalizeBlock) (res *abci.ResponseFinalizeBlock, err error) {
	defer func() {
		// call the streaming service hooks with the FinalizeBlock messages
		for _, streamingListener := range app.streamingManager.ABCIListeners {
			if err := streamingListener.ListenFinalizeBlock(app.finalizeBlockState.Context(), *req, *res); err != nil {
				app.logger.Error("ListenFinalizeBlock listening hook failed", "height", req.Height, "err", err)
			}
		}
	}()
```

**Example 2: Potential Non-Determinism Issue In FinalizeBlock** [MEDIUM]
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
// Addresses: Implementation flaw in abci finalize block logic allows exploitation through missing validation, inc
func secureAbciFinalizeBlock(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 1
- **Affected Protocols**: Layer 1 Assessment, Initia
- **Validation Strength**: Moderate (2 auditors)

---

## Detection Patterns

### Automated Detection
```
# Abci Endblock Error
grep -rn 'abci|endblock|error' --include='*.go' --include='*.sol'
# Abci Checktx Bypass
grep -rn 'abci|checktx|bypass' --include='*.go' --include='*.sol'
# Abci Vote Extension Abuse
grep -rn 'abci|vote|extension|abuse' --include='*.go' --include='*.sol'
# Abci Finalize Block
grep -rn 'abci|finalize|block' --include='*.go' --include='*.sol'
```

## Keywords

`abci`, `abci lifecycle`, `abuse`, `antehandler`, `appchain`, `been`, `beginblock`, `being`, `block`, `bypass`, `causing`, `checktx`, `cosmos`, `disguised`, `endblock`, `endblocker`, `error`, `errors`, `extension`, `extensions`, `finalize`, `finalizeblock`, `from`, `handle`, `incorrect`, `indexed`, `injected`, `issue`, `lack`, `message`
