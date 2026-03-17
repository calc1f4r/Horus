---
protocol: generic
chain: cosmos
category: governance
vulnerability_type: governance_voting_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: governance_logic

primitives:
  - voting_power_manipulation
  - proposal_exploit
  - quorum_manipulation
  - voting_lock
  - ballot_spam
  - bribe_manipulation
  - offboard_exploit
  - voting_zero_weight
  - parameter_change
  - timelock_bypass

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - governance
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | governance_logic | governance_voting_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - AnteHandle
  - _initValidatorScore
  - any
  - argmaxBlockByStake
  - ballot_spam
  - block.number
  - block.timestamp
  - bribe_manipulation
  - burn
  - deposit
  - dismissSlashProposal
  - execute
  - mint
  - msg.sender
  - new
  - offboard
  - offboard_exploit
  - parameter_change
  - proposal_exploit
  - quorum_manipulation
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Governance Voting Power Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect Injected Vote Extensions Validation | `reports/cosmos_cometbft_findings/incorrect-injected-vote-extensions-validation.md` | HIGH | OtterSec |
| Lack Of Signature Verification | `reports/cosmos_cometbft_findings/lack-of-signature-verification.md` | HIGH | OtterSec |
| Attacker will manipulate voting power calculations as `getOp | `reports/cosmos_cometbft_findings/m-1-attacker-will-manipulate-voting-power-calculations-as-getoperatorvotingpower.md` | MEDIUM | Sherlock |
| A malicious operator will control consensus without risking  | `reports/cosmos_cometbft_findings/m-7-a-malicious-operator-will-control-consensus-without-risking-stake-stake-exit.md` | MEDIUM | Sherlock |

### Governance Proposal Exploit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| A single unfreeze dismisses all other slashing proposal free | `reports/cosmos_cometbft_findings/a-single-unfreeze-dismisses-all-other-slashing-proposal-freezes-fixed.md` | HIGH | ConsenSys |
| AnteHandler Skipped In Non-CheckTx Mode | `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md` | HIGH | OtterSec |
| Block Proposer DDoS | `reports/cosmos_cometbft_findings/block-proposer-ddos.md` | MEDIUM | TrailOfBits |
| [H-05] `ValidatorRegistry::validatorScore/getPastValidatorSc | `reports/cosmos_cometbft_findings/h-05-validatorregistryvalidatorscoregetpastvalidatorscore-allows-validator-to-ea.md` | HIGH | Code4rena |
| Malicious proposer can submit a request with large invalid t | `reports/cosmos_cometbft_findings/h-10-malicious-proposer-can-submit-a-request-with-large-invalid-transactions-bec.md` | HIGH | Sherlock |
| ASA-2025-003: Groups module can halt chain when handling a m | `reports/cosmos_cometbft_findings/h-18-asa-2025-003-groups-module-can-halt-chain-when-handling-a-malicious-proposa.md` | HIGH | Sherlock |
| [M-05] Admin Can Break All Functionality Through Weth Addres | `reports/cosmos_cometbft_findings/m-05-admin-can-break-all-functionality-through-weth-address.md` | MEDIUM | Code4rena |
| castVote can be called by anyone even those without votes | `reports/cosmos_cometbft_findings/m-5-castvote-can-be-called-by-anyone-even-those-without-votes.md` | MEDIUM | Sherlock |

### Governance Quorum Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [EIGEN2-14] Stake deviations due to adding/removing strategy | `reports/cosmos_cometbft_findings/eigen2-14-stake-deviations-due-to-addingremoving-strategy-may-allow-for-ejector-.md` | MEDIUM | Hexens |
| Adversary can abuse delegating to lower quorum | `reports/cosmos_cometbft_findings/m-8-adversary-can-abuse-delegating-to-lower-quorum.md` | MEDIUM | Sherlock |

### Governance Voting Lock
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Voting does not take into account end of staking lock period | `reports/cosmos_cometbft_findings/h-5-voting-does-not-take-into-account-end-of-staking-lock-period.md` | HIGH | Sherlock |
| Missing highestVotingPower Update in argmaxBlockByStake Resu | `reports/cosmos_cometbft_findings/h-6-missing-highestvotingpower-update-in-argmaxblockbystake-resulting-in-incorre.md` | HIGH | Sherlock |
| [H06] AUD lending market could affect the protocol | `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md` | HIGH | OpenZeppelin |
| [H09] Slash process can be bypassed | `reports/cosmos_cometbft_findings/h09-slash-process-can-be-bypassed.md` | HIGH | OpenZeppelin |
| [M-03] Attacker Can Desynchronize Supply Snapshot During Sam | `reports/cosmos_cometbft_findings/m-03-attacker-can-desynchronize-supply-snapshot-during-same-block-unstake-reduci.md` | MEDIUM | Code4rena |
| Attacker will manipulate voting power calculations as `getOp | `reports/cosmos_cometbft_findings/m-1-attacker-will-manipulate-voting-power-calculations-as-getoperatorvotingpower.md` | MEDIUM | Sherlock |
| castVote can be called by anyone even those without votes | `reports/cosmos_cometbft_findings/m-5-castvote-can-be-called-by-anyone-even-those-without-votes.md` | MEDIUM | Sherlock |
| `getCommunityVotingPower` doesn't calculate voting Power cor | `reports/cosmos_cometbft_findings/m-5-getcommunityvotingpower-doesnt-calculate-voting-power-correctly-due-to-preci.md` | MEDIUM | Sherlock |

### Governance Ballot Spam
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-05] Limited Voting Options Allow Ballot Creation Spam | `reports/cosmos_cometbft_findings/m-05-limited-voting-options-allow-ballot-creation-spam.md` | MEDIUM | Code4rena |

### Governance Bribe Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Voting and bribe rewards can be hijacked during emergency un | `reports/cosmos_cometbft_findings/m-5-voting-and-bribe-rewards-can-be-hijacked-during-emergency-unlock-by-already-.md` | MEDIUM | Sherlock |

### Governance Offboard Exploit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-05] Replay attack to suddenly offboard the re-onboarded l | `reports/cosmos_cometbft_findings/m-05-replay-attack-to-suddenly-offboard-the-re-onboarded-lending-term.md` | MEDIUM | Code4rena |
| [M-06] Re-triggering the `canOffboard[term]` flag to bypass  | `reports/cosmos_cometbft_findings/m-06-re-triggering-the-canoffboardterm-flag-to-bypass-the-dao-vote-of-the-lendin.md` | MEDIUM | Code4rena |
| [M-17] The gauge status wasn't checked before reducing the u | `reports/cosmos_cometbft_findings/m-17-the-gauge-status-wasnt-checked-before-reducing-the-users-gauge-weight.md` | MEDIUM | Code4rena |
| [M-19] Over 90% of the Guild staked in a gauge can be unstak | `reports/cosmos_cometbft_findings/m-19-over-90-of-the-guild-staked-in-a-gauge-can-be-unstaked-despite-the-gauge-ut.md` | MEDIUM | Code4rena |
| [M-20] Inability to offboard term twice in a 7-day period ma | `reports/cosmos_cometbft_findings/m-20-inability-to-offboard-term-twice-in-a-7-day-period-may-lead-to-bad-debt-to-.md` | MEDIUM | Code4rena |

### Governance Voting Zero Weight
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Lack Of Signature Verification | `reports/cosmos_cometbft_findings/lack-of-signature-verification.md` | HIGH | OtterSec |
| [M-02] Fully slashed transcoder can vote with 0 weight messi | `reports/cosmos_cometbft_findings/m-02-fully-slashed-transcoder-can-vote-with-0-weight-messing-up-the-voting-calcu.md` | MEDIUM | Code4rena |
| [M-05] Limited Voting Options Allow Ballot Creation Spam | `reports/cosmos_cometbft_findings/m-05-limited-voting-options-allow-ballot-creation-spam.md` | MEDIUM | Code4rena |
| [M-06] Re-triggering the `canOffboard[term]` flag to bypass  | `reports/cosmos_cometbft_findings/m-06-re-triggering-the-canoffboardterm-flag-to-bypass-the-dao-vote-of-the-lendin.md` | MEDIUM | Code4rena |
| [M-18] A single malicious observer can fill the block space  | `reports/cosmos_cometbft_findings/m-18-a-single-malicious-observer-can-fill-the-block-space-with-msggaspricevoter-.md` | MEDIUM | Code4rena |
| castVote can be called by anyone even those without votes | `reports/cosmos_cometbft_findings/m-5-castvote-can-be-called-by-anyone-even-those-without-votes.md` | MEDIUM | Sherlock |
| castVote can be called by anyone even those without votes | `reports/cosmos_cometbft_findings/m-7-castvote-can-be-called-by-anyone-even-those-without-votes.md` | MEDIUM | Sherlock |
| Quick buy and sell allows vote manipulation | `reports/cosmos_cometbft_findings/quick-buy-and-sell-allows-vote-manipulation.md` | HIGH | TrailOfBits |

### Governance Parameter Change
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Attackers can prevent new challenges/listings/backends, para | `reports/cosmos_cometbft_findings/attackers-can-prevent-new-challengeslistingsbackends-parameter-changes-and-stake.md` | MEDIUM | TrailOfBits |
| [H-02] Arbitrary tokens and data can be bridged to `GnosisTa | `reports/cosmos_cometbft_findings/h-02-arbitrary-tokens-and-data-can-be-bridged-to-gnosistargetdispenserl2-to-mani.md` | HIGH | Code4rena |
| [H-02] It is impossible to slash queued withdrawals that con | `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md` | HIGH | Code4rena |
| Any public vault without a delegate can be drained | `reports/cosmos_cometbft_findings/h-30-any-public-vault-without-a-delegate-can-be-drained.md` | HIGH | Sherlock |
| [H08] Endpoint registration can be frontrun | `reports/cosmos_cometbft_findings/h08-endpoint-registration-can-be-frontrun.md` | HIGH | OpenZeppelin |
| [LID-5] Deposit call data not included in guardian signature | `reports/cosmos_cometbft_findings/lid-5-deposit-call-data-not-included-in-guardian-signature.md` | MEDIUM | Hexens |
| Unrestricted Validator Registration May Lead To DoS | `reports/cosmos_cometbft_findings/unrestricted-validator-registration-may-lead-to-dos.md` | MEDIUM | OtterSec |

### Governance Timelock Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H02] Delegators can prevent service providers from deregist | `reports/cosmos_cometbft_findings/h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md` | HIGH | OpenZeppelin |
| [H06] AUD lending market could affect the protocol | `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md` | HIGH | OpenZeppelin |
| [M-05] Replay attack to suddenly offboard the re-onboarded l | `reports/cosmos_cometbft_findings/m-05-replay-attack-to-suddenly-offboard-the-re-onboarded-lending-term.md` | MEDIUM | Code4rena |
| [M-06] Re-triggering the `canOffboard[term]` flag to bypass  | `reports/cosmos_cometbft_findings/m-06-re-triggering-the-canoffboardterm-flag-to-bypass-the-dao-vote-of-the-lendin.md` | MEDIUM | Code4rena |
| Withdraw delay can be bypassed | `reports/cosmos_cometbft_findings/m-5-withdraw-delay-can-be-bypassed.md` | MEDIUM | Sherlock |
| Missing Expiration Check when Adding to Existing Stake Allow | `reports/cosmos_cometbft_findings/missing-expiration-check-when-adding-to-existing-stake-allows-timelock-bypass.md` | MEDIUM | Quantstamp |
| Withdrawal Delay Can Be Bypassed When L1 Operations Processe | `reports/cosmos_cometbft_findings/withdrawal-delay-can-be-bypassed-when-l1-operations-processed-more-than-once-per.md` | MEDIUM | Spearbit |

---

# Governance Voting Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Governance Voting Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Governance Voting Power Manipulation](#1-governance-voting-power-manipulation)
2. [Governance Proposal Exploit](#2-governance-proposal-exploit)
3. [Governance Quorum Manipulation](#3-governance-quorum-manipulation)
4. [Governance Voting Lock](#4-governance-voting-lock)
5. [Governance Ballot Spam](#5-governance-ballot-spam)
6. [Governance Bribe Manipulation](#6-governance-bribe-manipulation)
7. [Governance Offboard Exploit](#7-governance-offboard-exploit)
8. [Governance Voting Zero Weight](#8-governance-voting-zero-weight)
9. [Governance Parameter Change](#9-governance-parameter-change)
10. [Governance Timelock Bypass](#10-governance-timelock-bypass)

---

## 1. Governance Voting Power Manipulation

### Overview

Implementation flaw in governance voting power manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 2, MEDIUM: 2.

> **Key Finding**: The bug report is about a function called ValidateVoteExtensions that relies on data injected by the proposer, which can be manipulated to misrepresent the voting power of validators. This can lead to incorrect consensus decisions and compromised voting process. The report recommends applying a patc



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | governance_logic | governance_voting_vulnerabilities`
- Interaction scope: `multi_contract`
- Primary affected component(s): `governance_logic`
- High-signal code keywords: `AnteHandle`, `_initValidatorScore`, `any`, `argmaxBlockByStake`, `ballot_spam`, `block.number`, `block.timestamp`, `bribe_manipulation`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `allows.function -> receives.function -> where.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Critical input parameter not validated against expected range or format
- Signal 2: Oracle data consumed without staleness check or sanity bounds
- Signal 3: User-supplied address or calldata forwarded without validation
- Signal 4: Missing check allows operation under invalid or stale state

#### False Positive Guards

- Not this bug when: Validation exists but is in an upstream function caller
- Safe if: Parameter range is inherently bounded by the type or protocol invariant
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Implementation flaw in governance voting power manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies governance voting power manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to governance operations

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

**Example 3: Attacker will manipulate voting power calculations as `getOperatorVotingPower()`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-attacker-will-manipulate-voting-power-calculations-as-getoperatorvotingpower.md`
```go
// Add vault validation
if (!isSharedVaultRegistered(vault) && !isOperatorVaultRegistered(vault)) {
    return 0;
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in governance voting power manipulation logic allows exploitation through missin
func secureGovernanceVotingPowerManipulation(ctx sdk.Context) error {
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
- **Affected Protocols**: Symbiotic Relay, Ethos Cosmos
- **Validation Strength**: Moderate (2 auditors)

---

## 2. Governance Proposal Exploit

### Overview

Implementation flaw in governance proposal exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 13 audit reports with severity distribution: HIGH: 6, MEDIUM: 7.

> **Key Finding**: The Forta team has identified a bug in their staking system that allows malicious actors to avoid punishment intended by the slashes and freezes. This is due to the fact that when any one of the active proposals against a subject gets to the end of its lifecycle, be it rejected, dismissed, executed,

### Vulnerability Description

#### Root Cause

Implementation flaw in governance proposal exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies governance proposal exploit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to governance operations

### Vulnerable Pattern Examples

**Example 1: A single unfreeze dismisses all other slashing proposal freezes ✓ Fixed** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/a-single-unfreeze-dismisses-all-other-slashing-proposal-freezes-fixed.md`
```solidity
function dismissSlashProposal(uint256 \_proposalId, string[] calldata \_evidence) external onlyRole(SLASHING\_ARBITER\_ROLE) {
    \_transition(\_proposalId, DISMISSED);
    \_submitEvidence(\_proposalId, DISMISSED, \_evidence);
    \_returnDeposit(\_proposalId);
    \_unfreeze(\_proposalId);
}
```

**Example 2: AnteHandler Skipped In Non-CheckTx Mode** [HIGH]
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

**Example 3: Block Proposer DDoS** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/block-proposer-ddos.md`
```
// Vulnerable pattern from Prysm:
## Diﬃculty: High
```

**Example 4: [H-05] `ValidatorRegistry::validatorScore/getPastValidatorScore` allows validato** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-05-validatorregistryvalidatorscoregetpastvalidatorscore-allows-validator-to-ea.md`
```solidity
function _initValidatorScore(
    uint256 virtualId,
    address validator
) internal {
    _baseValidatorScore[validator][virtualId] = _getMaxScore(virtualId);
}
```

**Example 5: Malicious proposer can submit a request with large invalid transactions because ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-10-malicious-proposer-can-submit-a-request-with-large-invalid-transactions-bec.md`
```
// Vulnerable pattern from SEDA Protocol:
Source: https://github.com/sherlock-audit/2024-12-seda-protocol-judging/issues/241
```

**Variant: Governance Proposal Exploit - MEDIUM Severity Cases** [MEDIUM]
> Found in 7 reports:
> - `reports/cosmos_cometbft_findings/block-proposer-ddos.md`
> - `reports/cosmos_cometbft_findings/m-05-admin-can-break-all-functionality-through-weth-address.md`
> - `reports/cosmos_cometbft_findings/m-5-castvote-can-be-called-by-anyone-even-those-without-votes.md`

**Variant: Governance Proposal Exploit in SEDA Protocol** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-10-malicious-proposer-can-submit-a-request-with-large-invalid-transactions-bec.md`
> - `reports/cosmos_cometbft_findings/h-18-asa-2025-003-groups-module-can-halt-chain-when-handling-a-malicious-proposa.md`

**Variant: Governance Proposal Exploit in FrankenDAO** [MEDIUM]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/m-5-castvote-can-be-called-by-anyone-even-those-without-votes.md`
> - `reports/cosmos_cometbft_findings/m-6-delegate-can-keep-can-keep-delegatee-trapped-indefinitely.md`
> - `reports/cosmos_cometbft_findings/m-9-delegate-can-keep-can-keep-delegatee-trapped-indefinitely.md`

**Variant: Governance Proposal Exploit in Berachain Beaconkit** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/max_tx_bytes-default-1mb-can-be-exceeded-in-prepareproposal.md`
> - `reports/cosmos_cometbft_findings/unvalidated-proposerindex-in-beaconblock.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in governance proposal exploit logic allows exploitation through missing validat
func secureGovernanceProposalExploit(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 6, MEDIUM: 7
- **Affected Protocols**: Virtuals Protocol, Canto, Forta Delegated Staking, Berachain Beaconkit, Prysm
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Governance Quorum Manipulation

### Overview

Implementation flaw in governance quorum manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: This bug report discusses a problem in the StakeRegistry contract where the `updateOperatorsStake()` function is not updating all operators' stakes immediately after a strategy is added or removed from a quorum. This can lead to unfair competition and manipulation by the ejector role. The suggested 

### Vulnerability Description

#### Root Cause

Implementation flaw in governance quorum manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies governance quorum manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to governance operations

### Vulnerable Pattern Examples

**Example 1: [EIGEN2-14] Stake deviations due to adding/removing strategy may allow for eject** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/eigen2-14-stake-deviations-due-to-addingremoving-strategy-may-allow-for-ejector-.md`
```go
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

    totalStakeDelta += stakeDelta;
}

// Apply the delta to the quorum's total stake
_recordTotalStakeUpdate(quorumNumber, totalStakeDelta);
```

**Example 2: Adversary can abuse delegating to lower quorum** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-8-adversary-can-abuse-delegating-to-lower-quorum.md`
```
// Vulnerable pattern from FrankenDAO:
Source: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/24
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in governance quorum manipulation logic allows exploitation through missing vali
func secureGovernanceQuorumManipulation(ctx sdk.Context) error {
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
- **Affected Protocols**: Eigenlayer, FrankenDAO
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Governance Voting Lock

### Overview

Implementation flaw in governance voting lock logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 16 audit reports with severity distribution: HIGH: 6, MEDIUM: 10.

> **Key Finding**: This bug report discusses an issue with the voting system in the Magicsea protocol. Users are able to vote using staked positions in the MlumStaking contract, but the voting system does not check if the remaining lock period of a staking position is longer than the voting epoch. This means that user

### Vulnerability Description

#### Root Cause

Implementation flaw in governance voting lock logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies governance voting lock in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to governance operations

### Vulnerable Pattern Examples

**Example 1: Voting does not take into account end of staking lock period** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-5-voting-does-not-take-into-account-end-of-staking-lock-period.md`
```solidity
function vote(uint256 tokenId, address[] calldata pools, uint256[] calldata deltaAmounts) external {
        if (pools.length != deltaAmounts.length) revert IVoter__InvalidLength();

        // check voting started
        if (!_votingStarted()) revert IVoter_VotingPeriodNotStarted();
        if (_votingEnded()) revert IVoter_VotingPeriodEnded();

        // check ownership of tokenId
        if (_mlumStaking.ownerOf(tokenId) != msg.sender) {
            revert IVoter__NotOwner();
        }

        uint256 currentPeriodId = _currentVotingPeriodId;
        // check if alreay voted
        if (_hasVotedInPeriod[currentPeriodId][tokenId]) {
            revert IVoter__AlreadyVoted();
        }

        // check if _minimumLockTime >= initialLockDuration and it is locked
        if (_mlumStaking.getStakingPosition(tokenId).initialLockDuration < _minimumLockTime) {
            revert IVoter__InsufficientLockTime();
        }
        if (_mlumStaking.getStakingPosition(tokenId).lockDuration < _periodDuration) {
            revert IVoter__InsufficientLockTime();
        }

        uint256 votingPower = _mlumStaking.getStakingPosition(tokenId).amountWithMultiplier;

        // check if deltaAmounts > votingPower
        uint256 totalUserVotes;
        for (uint256 i = 0; i < pools.length; ++i) {
            totalUserVotes += deltaAmounts[i];
        }

        if (totalUserVotes > votingPower) {
// ... (truncated)
```

**Example 2: Missing highestVotingPower Update in argmaxBlockByStake Resulting in Incorrect B** [HIGH]
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

**Example 3: [H06] AUD lending market could affect the protocol** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`
```
// Vulnerable pattern from Audius Contracts Audit:
In case an AUD token lending market appears, an attacker could use this market to influence the result of a governance’s proposal, which could lead to a take over of the protocol.


An attacker would only need to stake tokens for a brief moment without waiting for the [`votingPeriod`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L23) to request an unstake. This aggravates the attack, as the attacker would on
```

**Example 4: [M-03] Attacker Can Desynchronize Supply Snapshot During Same-Block Unstake, Red** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-attacker-can-desynchronize-supply-snapshot-during-same-block-unstake-reduci.md`
```
// Vulnerable pattern from Cabal:
<https://github.com/code-423n4/2025-04-cabal/blob/5b5f92ab4f95e5f9f405bbfa252860472d164705/sources/cabal_token.move# L219-L227>

### Finding description and impact

An attacker holding Cabal LSTs (like sxINIT) can monitor the mempool for the manager’s `voting_reward::snapshot()` transaction. By submitting his own `cabal::initiate_unstake` transaction to execute in the *same block* (`H`) as the manager’s snapshot, the attacker can use two flaws:

1. `cabal_token::burn` (called by their unstake) d
```

**Example 5: Attacker will manipulate voting power calculations as `getOperatorVotingPower()`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-attacker-will-manipulate-voting-power-calculations-as-getoperatorvotingpower.md`
```go
// Add vault validation
if (!isSharedVaultRegistered(vault) && !isOperatorVaultRegistered(vault)) {
    return 0;
}
```

**Variant: Governance Voting Lock - MEDIUM Severity Cases** [MEDIUM]
> Found in 10 reports:
> - `reports/cosmos_cometbft_findings/m-03-attacker-can-desynchronize-supply-snapshot-during-same-block-unstake-reduci.md`
> - `reports/cosmos_cometbft_findings/m-1-attacker-will-manipulate-voting-power-calculations-as-getoperatorvotingpower.md`
> - `reports/cosmos_cometbft_findings/m-5-castvote-can-be-called-by-anyone-even-those-without-votes.md`

**Variant: Governance Voting Lock in MagicSea - the native DEX on the IotaEVM** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-5-voting-does-not-take-into-account-end-of-staking-lock-period.md`
> - `reports/cosmos_cometbft_findings/m-5-voting-and-bribe-rewards-can-be-hijacked-during-emergency-unlock-by-already-.md`

**Variant: Governance Voting Lock in Audius Contracts Audit** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`
> - `reports/cosmos_cometbft_findings/h09-slash-process-can-be-bypassed.md`

**Variant: Governance Voting Lock in Symbiotic Relay** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-1-attacker-will-manipulate-voting-power-calculations-as-getoperatorvotingpower.md`
> - `reports/cosmos_cometbft_findings/m-7-a-malicious-operator-will-control-consensus-without-risking-stake-stake-exit.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in governance voting lock logic allows exploitation through missing validation, 
func secureGovernanceVotingLock(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 16 audit reports
- **Severity Distribution**: HIGH: 6, MEDIUM: 10
- **Affected Protocols**: Celo Contracts Audit, Symbiotic Relay, MagicSea - the native DEX on the IotaEVM, Streamr, Berachain Beaconkit
- **Validation Strength**: Strong (3+ auditors)

---

## 5. Governance Ballot Spam

### Overview

Implementation flaw in governance ballot spam logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The bug report discusses a problem with the voting system for certain types of votes. It allows compromised or faulty observers to create spam ballots with false observations, and honest observers are unable to vote against them. This results in wasted resources for honest observers without any puni

### Vulnerability Description

#### Root Cause

Implementation flaw in governance ballot spam logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies governance ballot spam in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to governance operations

### Vulnerable Pattern Examples

**Example 1: [M-05] Limited Voting Options Allow Ballot Creation Spam** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-05-limited-voting-options-allow-ballot-creation-spam.md`
```go
ballot, err = k.zetaObserverKeeper.AddVoteToBallot(ctx, ballot, msg.Creator, observerTypes.VoteType_SuccessObservation)
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in governance ballot spam logic allows exploitation through missing validation, 
func secureGovernanceBallotSpam(ctx sdk.Context) error {
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

## 6. Governance Bribe Manipulation

### Overview

Implementation flaw in governance bribe manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report discusses a vulnerability in the MagicSea Judging system where an attacker can manipulate the voting process during an emergency unlock by using existing positions. This can give them an unfair advantage in controlling the outcome of the vote and receiving rewards. The vulnerability 

### Vulnerability Description

#### Root Cause

Implementation flaw in governance bribe manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies governance bribe manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to governance operations

### Vulnerable Pattern Examples

**Example 1: Voting and bribe rewards can be hijacked during emergency unlock by already exis** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-5-voting-and-bribe-rewards-can-be-hijacked-during-emergency-unlock-by-already-.md`
```
// Vulnerable pattern from MagicSea - the native DEX on the IotaEVM:
Source: https://github.com/sherlock-audit/2024-06-magicsea-judging/issues/290
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in governance bribe manipulation logic allows exploitation through missing valid
func secureGovernanceBribeManipulation(ctx sdk.Context) error {
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
- **Affected Protocols**: MagicSea - the native DEX on the IotaEVM
- **Validation Strength**: Single auditor

---

## 7. Governance Offboard Exploit

### Overview

Implementation flaw in governance offboard exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: MEDIUM: 5.

> **Key Finding**: The `LendingTermOffboarding` contract allows for the removal of a lending term through a voting mechanism. However, a vulnerability has been found that allows an attacker to bypass this voting process and force the removal of a re-onboarded term. This could potentially put user funds at risk and imp

### Vulnerability Description

#### Root Cause

Implementation flaw in governance offboard exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies governance offboard exploit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to governance operations

### Vulnerable Pattern Examples

**Example 1: [M-05] Replay attack to suddenly offboard the re-onboarded lending term** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-05-replay-attack-to-suddenly-offboard-the-re-onboarded-lending-term.md`
```solidity
function supportOffboard(
        uint256 snapshotBlock,
        address term
    ) external whenNotPaused {
        require(
            block.number <= snapshotBlock + POLL_DURATION_BLOCKS,
            "LendingTermOffboarding: poll expired"
        );
        uint256 _weight = polls[snapshotBlock][term];
        require(_weight != 0, "LendingTermOffboarding: poll not found");
        uint256 userWeight = GuildToken(guildToken).getPastVotes(
            msg.sender,
            snapshotBlock
        );
        require(userWeight != 0, "LendingTermOffboarding: zero weight");
        require(
            userPollVotes[msg.sender][snapshotBlock][term] == 0,
            "LendingTermOffboarding: already voted"
        );

        userPollVotes[msg.sender][snapshotBlock][term] = userWeight;
        polls[snapshotBlock][term] = _weight + userWeight;
@1      if (_weight + userWeight >= quorum) {
@1          canOffboard[term] = true; //@audit -- Once the voting weight is enough, the canOffboard[term] flag will be set
@1      }
        emit OffboardSupport(
            block.timestamp,
            term,
            snapshotBlock,
            msg.sender,
            userWeight
        );
    }

    function offboard(address term) external whenNotPaused {
// ... (truncated)
```

**Example 2: [M-06] Re-triggering the `canOffboard[term]` flag to bypass the DAO vote of the ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-06-re-triggering-the-canoffboardterm-flag-to-bypass-the-dao-vote-of-the-lendin.md`
```
// Vulnerable pattern from Ethereum Credit Guild:
The `LendingTermOffboarding` contract allows guild holders to poll to remove a lending term. If the voting weight is enough, the lending term can be offboarded without delay. Further, the offboarded term can be re-onboarded to become an active term through the `LendingTermOnboarding::proposeOnboard()` following up with the voting mechanism.

The following briefly describes the steps for offboarding the lending term through the `LendingTermOffboarding` contract:

1. Anyone executes the `proposeOf
```

**Example 3: [M-17] The gauge status wasn't checked before reducing the user's gauge weight.** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-17-the-gauge-status-wasnt-checked-before-reducing-the-users-gauge-weight.md`
```go
161:        // pause psm redemptions
162:        if (
163:            nOffboardingsInProgress++ == 0 &&
164:            !SimplePSM(psm).redemptionsPaused()
165:        ) {
167:            SimplePSM(psm).setRedemptionsPaused(true);
168:        }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in governance offboard exploit logic allows exploitation through missing validat
func secureGovernanceOffboardExploit(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 5 audit reports
- **Severity Distribution**: MEDIUM: 5
- **Affected Protocols**: Ethereum Credit Guild
- **Validation Strength**: Single auditor

---

## 8. Governance Voting Zero Weight

### Overview

Implementation flaw in governance voting zero weight logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 8 audit reports with severity distribution: HIGH: 2, MEDIUM: 6.

> **Key Finding**: The bug report is about a lack of verification for signatures on vote extensions. This means that there is a possibility for incorrect calculations of voting power and for a malicious proposer to influence the outcome. The function responsible for validating vote extensions does not raise an error i

### Vulnerability Description

#### Root Cause

Implementation flaw in governance voting zero weight logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies governance voting zero weight in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to governance operations

### Vulnerable Pattern Examples

**Example 1: Lack Of Signature Verification** [HIGH]
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

**Example 2: [M-02] Fully slashed transcoder can vote with 0 weight messing up the voting cal** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-fully-slashed-transcoder-can-vote-with-0-weight-messing-up-the-voting-calcu.md`
```
// Vulnerable pattern from Livepeer:
If a transcoder gets slashed fully he can still vote with 0 amount of `weight` making any other delegated user that wants to change his vote to subtract their `weight` amount from other delegators/transcoders.

### Proof of Concept

In `BondingManager.sol` any transcoder can gets slashed by a specific percentage, and that specific transcoder gets resigned and that specific percentage gets deducted from his `bondedAmount`.<br>
<https://github.com/code-423n4/2023-08-livepeer/blob/a3d801fa4690119b6
```

**Example 3: [M-05] Limited Voting Options Allow Ballot Creation Spam** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-05-limited-voting-options-allow-ballot-creation-spam.md`
```go
ballot, err = k.zetaObserverKeeper.AddVoteToBallot(ctx, ballot, msg.Creator, observerTypes.VoteType_SuccessObservation)
```

**Example 4: [M-06] Re-triggering the `canOffboard[term]` flag to bypass the DAO vote of the ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-06-re-triggering-the-canoffboardterm-flag-to-bypass-the-dao-vote-of-the-lendin.md`
```
// Vulnerable pattern from Ethereum Credit Guild:
The `LendingTermOffboarding` contract allows guild holders to poll to remove a lending term. If the voting weight is enough, the lending term can be offboarded without delay. Further, the offboarded term can be re-onboarded to become an active term through the `LendingTermOnboarding::proposeOnboard()` following up with the voting mechanism.

The following briefly describes the steps for offboarding the lending term through the `LendingTermOffboarding` contract:

1. Anyone executes the `proposeOf
```

**Example 5: castVote can be called by anyone even those without votes** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-5-castvote-can-be-called-by-anyone-even-those-without-votes.md`
```
// Vulnerable pattern from FrankenDAO:
Source: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/25
```

**Variant: Governance Voting Zero Weight - MEDIUM Severity Cases** [MEDIUM]
> Found in 6 reports:
> - `reports/cosmos_cometbft_findings/m-02-fully-slashed-transcoder-can-vote-with-0-weight-messing-up-the-voting-calcu.md`
> - `reports/cosmos_cometbft_findings/m-05-limited-voting-options-allow-ballot-creation-spam.md`
> - `reports/cosmos_cometbft_findings/m-06-re-triggering-the-canoffboardterm-flag-to-bypass-the-dao-vote-of-the-lendin.md`

**Variant: Governance Voting Zero Weight in ZetaChain** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-05-limited-voting-options-allow-ballot-creation-spam.md`
> - `reports/cosmos_cometbft_findings/m-18-a-single-malicious-observer-can-fill-the-block-space-with-msggaspricevoter-.md`

**Variant: Governance Voting Zero Weight in FrankenDAO** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-5-castvote-can-be-called-by-anyone-even-those-without-votes.md`
> - `reports/cosmos_cometbft_findings/m-7-castvote-can-be-called-by-anyone-even-those-without-votes.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in governance voting zero weight logic allows exploitation through missing valid
func secureGovernanceVotingZeroWeight(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 8 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 6
- **Affected Protocols**: Ethos Cosmos, Livepeer, ZetaChain, The Computable Protocol, Ethereum Credit Guild
- **Validation Strength**: Strong (3+ auditors)

---

## 9. Governance Parameter Change

### Overview

Implementation flaw in governance parameter change logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 7 audit reports with severity distribution: HIGH: 4, MEDIUM: 3.

> **Key Finding**: This bug report is related to Data Validation in Datatrust. It is classified as a low difficulty bug. The addCandidate function enables users to propose new challenges, listings, or Backend and parameter changes. However, this can be exploited by attackers to block essential operations performed by 

### Vulnerability Description

#### Root Cause

Implementation flaw in governance parameter change logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies governance parameter change in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to governance operations

### Vulnerable Pattern Examples

**Example 1: Attackers can prevent new challenges/listings/backends, parameter changes, and s** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/attackers-can-prevent-new-challengeslistingsbackends-parameter-changes-and-stake.md`
```go
def addCandidate(hash: bytes32, kind: uint256, owner: address, stake: wei_value, vote_by: timedelta):
    """
    @notice Given a listing or parameter hash, create a new voting candidate
    @dev Only privileged contracts may call this method
    @param hash The identifier for the listing or reparameterization candidate
    @param kind The type of candidate we are adding
    @param owner The address which owns this created candidate
    @param stake How much, in wei, must be staked to vote or challenge
    @param vote_by How long into the future until polls for this candidate close
    """
    assert self.hasPrivilege(msg.sender)
    assert self.candidates[hash].owner == ZERO_ADDRESS
    
    if kind == CHALLENGE:  # a challenger must successfully stake a challenge
        self.market_token.transferFrom(owner, self, stake)
    self.stakes[owner][hash] = stake
    end = timestamp = block.timestamp + vote_by
    self.candidates[hash].kind = kind
    self.candidates[hash].owner = owner
    self.candidates[hash].stake = stake
    self.candidates[hash].vote_by = end
    log.CandidateAdded(hash, kind, owner, end)
```

**Example 2: [H-02] Arbitrary tokens and data can be bridged to `GnosisTargetDispenserL2` to ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-arbitrary-tokens-and-data-can-be-bridged-to-gnosistargetdispenserl2-to-mani.md`
```
// Vulnerable pattern from Olas:
The [`GnosisTargetDispenserL2`](https://github.com/code-423n4/2024-05-olas/blob/3ce502ec8b475885b90668e617f3983cea3ae29f/tokenomics/contracts/staking/GnosisTargetDispenserL2.sol) contract receives OLAS tokens and data from L1 to L2 via the Omnibridge, or just data via the AMB. When tokens are bridged, the `onTokenBridged()` callback is invoked on the contract. This callback processes the received tokens and associated data by calling the internal `_receiveMessage()` function.

However, the `onTo
```

**Example 3: [H-02] It is impossible to slash queued withdrawals that contain a malicious str** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md`
```go
// keeps track of the index in the `indicesToSkip` array
    uint256 indicesToSkipIndex = 0;

    uint256 strategiesLength = queuedWithdrawal.strategies.length;
    for (uint256 i = 0; i < strategiesLength;) {
        // check if the index i matches one of the indices specified in the `indicesToSkip` array
        if (indicesToSkipIndex < indicesToSkip.length && indicesToSkip[indicesToSkipIndex] == i) {
            unchecked {
                ++indicesToSkipIndex;
            }
        } else {
            if (queuedWithdrawal.strategies[i] == beaconChainETHStrategy){
                    //withdraw the beaconChainETH to the recipient
                _withdrawBeaconChainETH(queuedWithdrawal.depositor, recipient, queuedWithdrawal.shares[i]);
            } else {
                // tell the strategy to send the appropriate amount of funds to the recipient
                queuedWithdrawal.strategies[i].withdraw(recipient, tokens[i], queuedWithdrawal.shares[i]);
            }
            unchecked {
                ++i; // @audit
            }
        }
    }
```

**Example 4: Any public vault without a delegate can be drained** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-30-any-public-vault-without-a-delegate-can-be-drained.md`
```go
VaultImplementation(vaultAddr).init(
  VaultImplementation.InitParams(delegate)
);
```

**Example 5: [H08] Endpoint registration can be frontrun** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h08-endpoint-registration-can-be-frontrun.md`
```
// Vulnerable pattern from Audius Contracts Audit:
An honest service provider’s call to the [`ServiceProviderFactory.register` function](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/ServiceProviderFactory.sol#L141) can be frontrun by a malicious actor in order to prevent any honest user from being able to register any endpoint.


The attacker can monitor the mempool for any calls to the `register` function, then frontrun them with their own call to the `register` function 
```

**Variant: Governance Parameter Change - HIGH Severity Cases** [HIGH]
> Found in 4 reports:
> - `reports/cosmos_cometbft_findings/h-02-arbitrary-tokens-and-data-can-be-bridged-to-gnosistargetdispenserl2-to-mani.md`
> - `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md`
> - `reports/cosmos_cometbft_findings/h-30-any-public-vault-without-a-delegate-can-be-drained.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in governance parameter change logic allows exploitation through missing validat
func secureGovernanceParameterChange(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 7 audit reports
- **Severity Distribution**: HIGH: 4, MEDIUM: 3
- **Affected Protocols**: Ditto, Astaria, Lido, Olas, Audius Contracts Audit
- **Validation Strength**: Strong (3+ auditors)

---

## 10. Governance Timelock Bypass

### Overview

Implementation flaw in governance timelock bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 7 audit reports with severity distribution: HIGH: 2, MEDIUM: 5.

> **Key Finding**: This bug report discusses an issue where under certain conditions, delegators may prevent service providers from deregistering endpoints. This can happen innocently or maliciously. When a service provider attempts to deregister an endpoint, their call to the `deregister` function may fail due to the

### Vulnerability Description

#### Root Cause

Implementation flaw in governance timelock bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies governance timelock bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to governance operations

### Vulnerable Pattern Examples

**Example 1: [H02] Delegators can prevent service providers from deregistering endpoints** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md`
```
// Vulnerable pattern from Audius Contracts Audit:
Under some conditions, delegators may prevent service providers from deregistering endpoints. This can happen innocently or maliciously.


Consider the case where a service provider has registered more than one endpoint and that the service provider has staked the minimum amount of stake. Suppose delegators have delegated to this service provider the maximum amount of stake.


When the service provider attempts to deregister one of the endpoints, their call to the [`deregister` function](https:/
```

**Example 2: [H06] AUD lending market could affect the protocol** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`
```
// Vulnerable pattern from Audius Contracts Audit:
In case an AUD token lending market appears, an attacker could use this market to influence the result of a governance’s proposal, which could lead to a take over of the protocol.


An attacker would only need to stake tokens for a brief moment without waiting for the [`votingPeriod`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L23) to request an unstake. This aggravates the attack, as the attacker would on
```

**Example 3: [M-05] Replay attack to suddenly offboard the re-onboarded lending term** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-05-replay-attack-to-suddenly-offboard-the-re-onboarded-lending-term.md`
```solidity
function supportOffboard(
        uint256 snapshotBlock,
        address term
    ) external whenNotPaused {
        require(
            block.number <= snapshotBlock + POLL_DURATION_BLOCKS,
            "LendingTermOffboarding: poll expired"
        );
        uint256 _weight = polls[snapshotBlock][term];
        require(_weight != 0, "LendingTermOffboarding: poll not found");
        uint256 userWeight = GuildToken(guildToken).getPastVotes(
            msg.sender,
            snapshotBlock
        );
        require(userWeight != 0, "LendingTermOffboarding: zero weight");
        require(
            userPollVotes[msg.sender][snapshotBlock][term] == 0,
            "LendingTermOffboarding: already voted"
        );

        userPollVotes[msg.sender][snapshotBlock][term] = userWeight;
        polls[snapshotBlock][term] = _weight + userWeight;
@1      if (_weight + userWeight >= quorum) {
@1          canOffboard[term] = true; //@audit -- Once the voting weight is enough, the canOffboard[term] flag will be set
@1      }
        emit OffboardSupport(
            block.timestamp,
            term,
            snapshotBlock,
            msg.sender,
            userWeight
        );
    }

    function offboard(address term) external whenNotPaused {
// ... (truncated)
```

**Example 4: Withdraw delay can be bypassed** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-5-withdraw-delay-can-be-bypassed.md`
```go
## Tool used

Manual Review

## Recommendation
Consider resetting `withdrawalRequestTimestamps` when user stake any amount of token.
```

**Example 5: Missing Expiration Check when Adding to Existing Stake Allows Timelock Bypass** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-expiration-check-when-adding-to-existing-stake-allows-timelock-bypass.md`
```
// Vulnerable pattern from Sapien - 2:
**Update**
Marked as "Fixed" by the client. Addressed in: `ffda07756c53963c20a254c11c97f6809d08cfaf`.

**File(s) affected:**`SapienVault.sol`

**Description:** The `stake()` and `increaseAmount()` functions allow users to add tokens to stakes without validation that the initial stake's lockup period has not ended. This can allow for some stakes where the new `weightedStartTime + effectiveLockUpPeriod < block.timestamp` meaning the stake is immediately unlocked. This allows users to benefit from 
```

**Variant: Governance Timelock Bypass - MEDIUM Severity Cases** [MEDIUM]
> Found in 5 reports:
> - `reports/cosmos_cometbft_findings/m-05-replay-attack-to-suddenly-offboard-the-re-onboarded-lending-term.md`
> - `reports/cosmos_cometbft_findings/m-06-re-triggering-the-canoffboardterm-flag-to-bypass-the-dao-vote-of-the-lendin.md`
> - `reports/cosmos_cometbft_findings/m-5-withdraw-delay-can-be-bypassed.md`

**Variant: Governance Timelock Bypass in Audius Contracts Audit** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md`
> - `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`

**Variant: Governance Timelock Bypass in Ethereum Credit Guild** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-05-replay-attack-to-suddenly-offboard-the-re-onboarded-lending-term.md`
> - `reports/cosmos_cometbft_findings/m-06-re-triggering-the-canoffboardterm-flag-to-bypass-the-dao-vote-of-the-lendin.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in governance timelock bypass logic allows exploitation through missing validati
func secureGovernanceTimelockBypass(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 7 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 5
- **Affected Protocols**: Sapien - 2, Kinetiq LST Protocol, Audius Contracts Audit, Ethereum Credit Guild, Telcoin Update
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Governance Voting Power Manipulation
grep -rn 'governance|voting|power|manipulation' --include='*.go' --include='*.sol'
# Governance Proposal Exploit
grep -rn 'governance|proposal|exploit' --include='*.go' --include='*.sol'
# Governance Quorum Manipulation
grep -rn 'governance|quorum|manipulation' --include='*.go' --include='*.sol'
# Governance Voting Lock
grep -rn 'governance|voting|lock' --include='*.go' --include='*.sol'
# Governance Ballot Spam
grep -rn 'governance|ballot|spam' --include='*.go' --include='*.sol'
# Governance Bribe Manipulation
grep -rn 'governance|bribe|manipulation' --include='*.go' --include='*.sol'
# Governance Offboard Exploit
grep -rn 'governance|offboard|exploit' --include='*.go' --include='*.sol'
# Governance Voting Zero Weight
grep -rn 'governance|voting|zero|weight' --include='*.go' --include='*.sol'
# Governance Parameter Change
grep -rn 'governance|parameter|change' --include='*.go' --include='*.sol'
# Governance Timelock Bypass
grep -rn 'governance|timelock|bypass' --include='*.go' --include='*.sol'
```

## Keywords

`abuse`, `account`, `adversary`, `affect`, `allow`, `already`, `antehandler`, `appchain`, `arbitrary`, `argmaxblockbystake`, `attack`, `attacker`, `attackers`, `ballot`, `before`, `block`, `bribe`, `bridged`, `bypass`, `calculations`, `change`, `checked`, `contain`, `cosmos`, `could`, `creation`, `data`, `ddos`, `delegating`, `delegators`

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

`AnteHandle`, `_initValidatorScore`, `any`, `appchain`, `argmaxBlockByStake`, `ballot_spam`, `block.number`, `block.timestamp`, `bribe_manipulation`, `burn`, `cosmos`, `defi`, `deposit`, `dismissSlashProposal`, `execute`, `governance`, `governance_voting_vulnerabilities`, `mint`, `msg.sender`, `new`, `offboard`, `offboard_exploit`, `parameter_change`, `proposal_exploit`, `quorum_manipulation`, `staking`, `timelock_bypass`, `voting_lock`, `voting_power_manipulation`, `voting_zero_weight`
