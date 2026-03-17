---
protocol: generic
chain: cosmos
category: signature
vulnerability_type: signature_replay_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: signature_logic

primitives:
  - verification_missing
  - replay
  - cross_chain_replay
  - forgery
  - duplicate
  - eip155_missing
  - key_management
  - malleability
  - nonce_manipulation

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - signature
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | signature_logic | signature_replay_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - AnteHandle
  - Indexers
  - _verifySignatures
  - block.number
  - cross_chain_replay
  - deposit
  - depositBufferedEther
  - duplicate
  - eip155_missing
  - forgery
  - key_management
  - malicious
  - malleability
  - markBeetleSafe
  - mint
  - msg.sender
  - nonce_manipulation
  - receive
  - replay
  - verification_missing
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Signature Verification Missing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Front-Running redeem Can Prevent Indexers From Receiving Rew | `reports/cosmos_cometbft_findings/front-running-redeem-can-prevent-indexers-from-receiving-rewards-for-allocations.md` | HIGH | OpenZeppelin |
| [H-03] `SettlementSignatureVerifier` is missing check for du | `reports/cosmos_cometbft_findings/h-03-settlementsignatureverifier-is-missing-check-for-duplicate-validator-signat.md` | HIGH | Code4rena |
| Lack Of Signature Verification | `reports/cosmos_cometbft_findings/lack-of-signature-verification.md` | HIGH | OtterSec |
| [LID-5] Deposit call data not included in guardian signature | `reports/cosmos_cometbft_findings/lid-5-deposit-call-data-not-included-in-guardian-signature.md` | MEDIUM | Hexens |
| Unbounded size of request in Covenant signer service | `reports/cosmos_cometbft_findings/unbounded-size-of-request-in-covenant-signer-service.md` | MEDIUM | Cantina |

### Signature Replay
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] Cross-contract signature replay allows users to infla | `reports/cosmos_cometbft_findings/h-01-cross-contract-signature-replay-allows-users-to-inflate-rewards.md` | HIGH | Pashov Audit Group |
| Signature Replay Attack Possible Between Stake, Unstake and  | `reports/cosmos_cometbft_findings/signature-replay-attack-possible-between-stake-unstake-and-reward-functions-enab.md` | HIGH | Quantstamp |

### Signature Cross Chain Replay
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Cross-chain transactions can be replayed when the chain unde | `reports/cosmos_cometbft_findings/cross-chain-transactions-can-be-replayed-when-the-chain-undergoes-a-hard-fork.md` | MEDIUM | Cantina |
| [M-04] Retry Payload Channel Collision | `reports/cosmos_cometbft_findings/m-04-retry-payload-channel-collision.md` | MEDIUM | Shieldify |

### Signature Forgery
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Lack Of Signature Verification | `reports/cosmos_cometbft_findings/lack-of-signature-verification.md` | HIGH | OtterSec |
| shred tile overflow | `reports/cosmos_cometbft_findings/shred-tile-overflow.md` | MEDIUM | Immunefi |

### Signature Duplicate
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-03] `SettlementSignatureVerifier` is missing check for du | `reports/cosmos_cometbft_findings/h-03-settlementsignatureverifier-is-missing-check-for-duplicate-validator-signat.md` | HIGH | Code4rena |

### Signature Eip155 Missing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Historical reward loss due to `NodeId` reuse in `AvalancheL1 | `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md` | MEDIUM | Cyfrin |
| Lack of Liquid Staking Accounting | `reports/cosmos_cometbft_findings/lack-of-liquid-staking-accounting.md` | MEDIUM | OtterSec |
| [M-12] `ValidatorWithdrawalVault.settleFunds` doesn't check  | `reports/cosmos_cometbft_findings/m-12-validatorwithdrawalvaultsettlefunds-doesnt-check-amount-that-user-has-insid.md` | MEDIUM | Code4rena |
| static_validate_system_transaction missing EIP-155 chain ID  | `reports/cosmos_cometbft_findings/static_validate_system_transaction-missing-eip-155-chain-id-validation.md` | HIGH | Spearbit |

### Signature Key Management
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Insecure storage of price-feeder keyring passwords | `reports/cosmos_cometbft_findings/insecure-storage-of-price-feeder-keyring-passwords.md` | MEDIUM | TrailOfBits |
| Peggo takes an Ethereum private key as a command-line argume | `reports/cosmos_cometbft_findings/peggo-takes-an-ethereum-private-key-as-a-command-line-argument.md` | MEDIUM | TrailOfBits |

### Signature Malleability
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| AnteHandler Skipped In Non-CheckTx Mode | `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md` | HIGH | OtterSec |
| Bypassing of NFT Collection Integrity Checks | `reports/cosmos_cometbft_findings/bypassing-of-nft-collection-integrity-checks.md` | HIGH | OtterSec |
| [C-01] User Can Deny Opponent NFT Rewards By Marking Safe Po | `reports/cosmos_cometbft_findings/c-01-user-can-deny-opponent-nft-rewards-by-marking-safe-post-battle.md` | HIGH | Shieldify |
| CASE SENSITIVE CHECK ALLOWS ADDING THE SAME NEAR FUNGIBLE TO | `reports/cosmos_cometbft_findings/case-sensitive-check-allows-adding-the-same-near-fungible-token-more-than-once.md` | MEDIUM | Halborn |
| CVGT Staking Pool State Manipulation | `reports/cosmos_cometbft_findings/cvgt-staking-pool-state-manipulation.md` | HIGH | OtterSec |
| Denial Of Slashing | `reports/cosmos_cometbft_findings/denial-of-slashing.md` | HIGH | OtterSec |
| Deposited Stakes Can Be Locked in StakeManager if the Valida | `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md` | HIGH | OpenZeppelin |
| Due Diligence into Farm managers | `reports/cosmos_cometbft_findings/due-diligence-into-farm-managers.md` | HIGH | OtterSec |

---

# Signature Replay Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Signature Replay Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Signature Verification Missing](#1-signature-verification-missing)
2. [Signature Replay](#2-signature-replay)
3. [Signature Cross Chain Replay](#3-signature-cross-chain-replay)
4. [Signature Forgery](#4-signature-forgery)
5. [Signature Duplicate](#5-signature-duplicate)
6. [Signature Eip155 Missing](#6-signature-eip155-missing)
7. [Signature Key Management](#7-signature-key-management)
8. [Signature Malleability](#8-signature-malleability)

---

## 1. Signature Verification Missing

### Overview

Implementation flaw in signature verification missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 3, MEDIUM: 2.

> **Key Finding**: The `redeem` function in `Escrow.sol` allows Indexers to receive query rewards by submitting a signed Receipt Aggregate Voucher (RAV) and `allocationIDProof`. However, anyone with knowledge of a valid `signedRAV` and `allocationIDProof` can call `redeem` and receive the rewards, regardless of whethe



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | signature_logic | signature_replay_vulnerabilities`
- Interaction scope: `multi_contract`
- Primary affected component(s): `signature_logic`
- High-signal code keywords: `AnteHandle`, `Indexers`, `_verifySignatures`, `block.number`, `cross_chain_replay`, `deposit`, `depositBufferedEther`, `duplicate`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `has.function -> is.function -> signature.function`
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

Implementation flaw in signature verification missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies signature verification missing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to signature operations

### Vulnerable Pattern Examples

**Example 1: Front-Running redeem Can Prevent Indexers From Receiving Rewards for Allocations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/front-running-redeem-can-prevent-indexers-from-receiving-rewards-for-allocations.md`
```
// Vulnerable pattern from The Graph Timeline Aggregation Audit:
The [`redeem`](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/blob/d8795c747d44da90f7717b3db9a08698e64a9b2f/src/Escrow.sol#L366) function in `Escrow.sol` enables Indexers to receive query rewards by submitting a signed Receipt Aggregate Voucher (RAV) and `allocationIDProof`. However, anyone who knows the contents of a valid `signedRAV` and `allocationIDProof` can call `redeem` regardless of whether the proof and signed RAV belong to them. This is because `redeem` only che
```

**Example 2: [H-03] `SettlementSignatureVerifier` is missing check for duplicate validator si** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-settlementsignatureverifier-is-missing-check-for-duplicate-validator-signat.md`
```solidity
function verifyECDSA(
    bytes32 msgHash,
    bytes calldata signatures
) internal view returns (bool) {
    require(
        signatures.length % 65 == 0,
        "Signature length must be a multiple of 65"
    );

    uint256 len = signatures.length;
    uint256 m = 0;
    for (uint256 i = 0; i < len; i += 65) {
        bytes memory sig = signatures[i:i + 65];
        if (
            validators[msgHash.recover(sig)] && ++m >= required_validators
        ) {
            return true;
        }
    }

    return false;
}
```

**Example 3: Lack Of Signature Verification** [HIGH]
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

**Example 4: [LID-5] Deposit call data not included in guardian signature** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/lid-5-deposit-call-data-not-included-in-guardian-signature.md`
```solidity
function depositBufferedEther(
    uint256 blockNumber,
    bytes32 blockHash,
    bytes32 depositRoot,
    uint256 stakingModuleId,
    uint256 nonce,
    bytes calldata depositCalldata,
    Signature[] calldata sortedGuardianSignatures
) external validStakingModuleId(stakingModuleId) {
    if (quorum == 0 || sortedGuardianSignatures.length < quorum) revert DepositNoQuorum();

    bytes32 onchainDepositRoot = IDepositContract(DEPOSIT_CONTRACT).get_deposit_root();
    if (depositRoot != onchainDepositRoot) revert DepositRootChanged();

    if (!STAKING_ROUTER.getStakingModuleIsActive(stakingModuleId)) revert DepositInactiveModule();

    uint256 lastDepositBlock = STAKING_ROUTER.getStakingModuleLastDepositBlock(stakingModuleId);
    if (block.number - lastDepositBlock < minDepositBlockDistance) revert DepositTooFrequent();
    if (blockHash == bytes32(0) || blockhash(blockNumber) != blockHash) revert DepositUnexpectedBlockHash();

    uint256 onchainNonce = STAKING_ROUTER.getStakingModuleNonce(stakingModuleId);
    if (nonce != onchainNonce) revert DepositNonceChanged();

    _verifySignatures(depositRoot, blockNumber, blockHash, stakingModuleId, nonce, sortedGuardianSignatures);

    LIDO.deposit(maxDepositsPerBlock, stakingModuleId, depositCalldata);
}

function _verifySignatures(
    bytes32 depositRoot,
    uint256 blockNumber,
    bytes32 blockHash,
    uint256 stakingModuleId,
    uint256 nonce,
    Signature[] memory sigs
// ... (truncated)
```

**Example 5: Unbounded size of request in Covenant signer service** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/unbounded-size-of-request-in-covenant-signer-service.md`
```go
#### Then, import the following attacking script in `exploit-dos.py`:
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in signature verification missing logic allows exploitation through missing vali
func secureSignatureVerificationMissing(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 3, MEDIUM: 2
- **Affected Protocols**: Lido, Ethos Cosmos, The Graph Timeline Aggregation Audit, Babylonchain, Chakra
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Signature Replay

### Overview

Implementation flaw in signature replay logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: This bug report states that there is a problem with the signature verification in the `NFTStaking._stakeNFTs()` function. This means that an attacker can use the same signature on different contracts and exploit the system by staking low-rarity NFTs and receiving rewards as if they were high-rarity.

### Vulnerability Description

#### Root Cause

Implementation flaw in signature replay logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies signature replay in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to signature operations

### Vulnerable Pattern Examples

**Example 1: [H-01] Cross-contract signature replay allows users to inflate rewards** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-cross-contract-signature-replay-allows-users-to-inflate-rewards.md`
```go
bytes32 hash = keccak256(abi.encode(_sender, _tokenIds, _rarityWeightIndexes));
```

**Example 2: Signature Replay Attack Possible Between Stake, Unstake and Reward Functions Ena** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/signature-replay-attack-possible-between-stake-unstake-and-reward-functions-enab.md`
```go
bytes32 messageHash = keccak256(abi.encodePacked(userWallet, rewardAmount, orderId));
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in signature replay logic allows exploitation through missing validation, incorr
func secureSignatureReplay(ctx sdk.Context) error {
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
- **Affected Protocols**: HYBUX_2025-11-11, Sapien
- **Validation Strength**: Moderate (2 auditors)

---

## 3. Signature Cross Chain Replay

### Overview

Implementation flaw in signature cross chain replay logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: The bug report discusses a potential issue with the NttManager.sol code, specifically in the function "completeInboundQueuedTransfer". During a hard fork, if there are still pending transactions in the InboundQueued, they can be replayed on another chain. This is due to the lack of a checkFork(evmCh

### Vulnerability Description

#### Root Cause

Implementation flaw in signature cross chain replay logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies signature cross chain replay in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to signature operations

### Vulnerable Pattern Examples

**Example 1: Cross-chain transactions can be replayed when the chain undergoes a hard fork** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/cross-chain-transactions-can-be-replayed-when-the-chain-undergoes-a-hard-fork.md`
```
// Vulnerable pattern from Wormhole:
## Vulnerability Report
```

**Example 2: [M-04] Retry Payload Channel Collision** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-retry-payload-channel-collision.md`
```go
mapping(uint256 => mapping(uint64 => bytes)) revertReceive; // [chainId][sequence] = payload
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in signature cross chain replay logic allows exploitation through missing valida
func secureSignatureCrossChainReplay(ctx sdk.Context) error {
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
- **Affected Protocols**: Wormhole, Toki Bridge
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Signature Forgery

### Overview

Implementation flaw in signature forgery logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: The bug report is about a lack of verification for signatures on vote extensions. This means that there is a possibility for incorrect calculations of voting power and for a malicious proposer to influence the outcome. The function responsible for validating vote extensions does not raise an error i

### Vulnerability Description

#### Root Cause

Implementation flaw in signature forgery logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies signature forgery in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to signature operations

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

**Example 2: shred tile overflow** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/shred-tile-overflow.md`
```go
static void
during_frag( void * _ctx,
             ulong  in_idx,
             ulong  seq,
             ulong  sig,
             ulong  chunk,
             ulong  sz,
             int *  opt_filter ) {
  (void)seq;

  fd_shred_ctx_t * ctx = (fd_shred_ctx_t *)_ctx;
  ...
   } else { /* the common case, from the netmux tile */
    /* The FEC resolver API does not present a prepare/commit model. If we
       get overrun between when the FEC resolver verifies the signature
       and when it stores the local copy, we could end up storing and
       retransmitting garbage.  Instead we copy it locally, sadly, and
       only give it to the FEC resolver when we know it won't be overrun
       anymore. */
1.    if( FD_UNLIKELY( chunk<ctx->net_in_chunk0 || chunk>ctx->net_in_wmark || sz>FD_NET_MTU ) )
      FD_LOG_ERR(( "chunk %lu %lu corrupt, not in range [%lu,%lu]", chunk, sz, ctx->net_in_chunk0, ctx->net_in_wmark ));
    uchar const * dcache_entry = fd_chunk_to_laddr_const( ctx->net_in_mem, chunk );
    ulong hdr_sz = fd_disco_netmux_sig_hdr_sz( sig );
    FD_TEST( hdr_sz <= sz ); /* Should be ensured by the net tile */
    fd_shred_t const * shred = fd_shred_parse( dcache_entry+hdr_sz, sz-hdr_sz );
    if( FD_UNLIKELY( !shred ) ) {
      *opt_filter = 1;
      return;
    };
    ...
    fd_memcpy( ctx->shred_buffer, dcache_entry+hdr_sz, sz-hdr_sz );
    ctx->shred_buffer_sz = sz-hdr_sz;
  }
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in signature forgery logic allows exploitation through missing validation, incor
func secureSignatureForgery(ctx sdk.Context) error {
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
- **Affected Protocols**: Firedancer v0.1, Ethos Cosmos
- **Validation Strength**: Moderate (2 auditors)

---

## 5. Signature Duplicate

### Overview

Implementation flaw in signature duplicate logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: The bug report identifies a problem with two functions, SettlementSignatureVerifier::verifyECDSA and settlement::check_chakra_signatures, in the Chakra protocol. These functions lack checks for duplicate validators, meaning that a single valid signature can pass the threshold and potentially harm th

### Vulnerability Description

#### Root Cause

Implementation flaw in signature duplicate logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies signature duplicate in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to signature operations

### Vulnerable Pattern Examples

**Example 1: [H-03] `SettlementSignatureVerifier` is missing check for duplicate validator si** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-settlementsignatureverifier-is-missing-check-for-duplicate-validator-signat.md`
```solidity
function verifyECDSA(
    bytes32 msgHash,
    bytes calldata signatures
) internal view returns (bool) {
    require(
        signatures.length % 65 == 0,
        "Signature length must be a multiple of 65"
    );

    uint256 len = signatures.length;
    uint256 m = 0;
    for (uint256 i = 0; i < len; i += 65) {
        bytes memory sig = signatures[i:i + 65];
        if (
            validators[msgHash.recover(sig)] && ++m >= required_validators
        ) {
            return true;
        }
    }

    return false;
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in signature duplicate logic allows exploitation through missing validation, inc
func secureSignatureDuplicate(ctx sdk.Context) error {
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
- **Affected Protocols**: Chakra
- **Validation Strength**: Single auditor

---

## 6. Signature Eip155 Missing

### Overview

Implementation flaw in signature eip155 missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 1, MEDIUM: 3.

> **Key Finding**: The `AvalancheL1Middleware` contract has a vulnerability where if a new operator (Operator B) re-registers a node using the same `nodeId` as a former operator (Operator A), Operator A's stake can be artificially increased. This can lead to a misallocation of rewards. The issue is caused by a functio

### Vulnerability Description

#### Root Cause

Implementation flaw in signature eip155 missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies signature eip155 missing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to signature operations

### Vulnerable Pattern Examples

**Example 1: Historical reward loss due to `NodeId` reuse in `AvalancheL1Middleware`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md`
```
// Vulnerable pattern from Suzaku Core:
**Description:** The `AvalancheL1Middleware` contract is vulnerable to misattributing stake to a former operator (Operator A) if a new, colluding or coordinated operator (Operator B) intentionally re-registers a node using the *exact same `bytes32 nodeId`* that Operator A previously used. This scenario assumes Operator B is aware of Operator A's historical `nodeId` and that the underlying P-Chain NodeID (`P_X`, derived from the shared `bytes32 nodeId`) has become available for re-registration on
```

**Example 2: Lack of Liquid Staking Accounting** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-liquid-staking-accounting.md`
```
// Vulnerable pattern from Cosmos LSM:
## Validator Issues in Liquid Staking

CreateValidator lacks the liquid staking-related bookkeeping present in Delegate. In Delegate, specific checks and updates are performed when the delegation is initiated by a liquid staking provider, converting the staked tokens into an equivalent number of shares in the validator and safely updating the global liquid stake and validator liquid shares. However, no such checks or updates are performed for liquid staking when self-delegating the initial stake
```

**Example 3: [M-12] `ValidatorWithdrawalVault.settleFunds` doesn't check amount that user has** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-12-validatorwithdrawalvaultsettlefunds-doesnt-check-amount-that-user-has-insid.md`
```
// Vulnerable pattern from Stader Labs:
`ValidatorWithdrawalVault.settleFunds` doesn't check amount that user has inside `NodeELRewardVault` to pay for penalty. That value can increase operator's earned amount, which can avoid slashing.

### Proof of Concept

When a validator withdraws from beacon chain the `ValidatorWithdrawalVault.settleFunds` function is called. This function calculates amount that a validator [has earned](https://github.com/code-423n4/2023-06-stader/blob/main/contracts/ValidatorWithdrawalVault.sol#L62) for attesta
```

**Example 4: static_validate_system_transaction missing EIP-155 chain ID validation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/static_validate_system_transaction-missing-eip-155-chain-id-validation.md`
```rust
fn static_validate_system_transaction(
    txn: &Recovered<TxEnvelope>,
) -> Result<(), SystemTransactionError> {
    if !Self::is_system_sender(txn.signer()) {
        return Err(SystemTransactionError::UnexpectedSenderAddress);
    }
    if !txn.tx().is_legacy() {
        return Err(SystemTransactionError::InvalidTxType);
    }
    if txn.tx().gas_price() != Some(0) {
        return Err(SystemTransactionError::NonZeroGasPrice);
    }
    if txn.tx().gas_limit() != 0 {
        return Err(SystemTransactionError::NonZeroGasLimit);
    }
    if !matches!(txn.tx().kind(), TxKind::Call(_)) {
        return Err(SystemTransactionError::InvalidTxKind);
    }
    Ok(())
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in signature eip155 missing logic allows exploitation through missing validation
func secureSignatureEip155Missing(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 3
- **Affected Protocols**: Stader Labs, Cosmos LSM, Monad, Suzaku Core
- **Validation Strength**: Strong (3+ auditors)

---

## 7. Signature Key Management

### Overview

Implementation flaw in signature key management logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: A bug has been identified in the price-feeder, a data validation target, which has a high difficulty level. The bug is that the price-feeder stores keyring passwords in plaintext and does not provide a warning if the configuration file has overly broad permissions. Furthermore, neither the README no

### Vulnerability Description

#### Root Cause

Implementation flaw in signature key management logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies signature key management in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to signature operations

### Vulnerable Pattern Examples

**Example 1: Insecure storage of price-feeder keyring passwords** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/insecure-storage-of-price-feeder-keyring-passwords.md`
```go
**Figure 25.1:** The `price-feeder` does not warn the user if the configuration file used to store the keyring password in plaintext has overly broad permissions.

### Trail of Bits

#### UMEE Security Assessment
**PUBLIC**
```

**Example 2: Peggo takes an Ethereum private key as a command-line argument** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/peggo-takes-an-ethereum-private-key-as-a-command-line-argument.md`
```
// Vulnerable pattern from Umee:
## Diﬃculty: High
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in signature key management logic allows exploitation through missing validation
func secureSignatureKeyManagement(ctx sdk.Context) error {
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
- **Affected Protocols**: Umee
- **Validation Strength**: Single auditor

---

## 8. Signature Malleability

### Overview

Implementation flaw in signature malleability logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 72 audit reports with severity distribution: HIGH: 34, MEDIUM: 38.

> **Key Finding**: The Cosmos AnteHandlers are used to check the validity of transactions and prevent malicious transactions from being executed. However, some of the validators are skipped when not in CheckTx mode, allowing attackers to insert malformed transactions into block proposals. This can lead to incorrect ex

### Vulnerability Description

#### Root Cause

Implementation flaw in signature malleability logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies signature malleability in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to signature operations

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

**Example 2: Bypassing of NFT Collection Integrity Checks** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/bypassing-of-nft-collection-integrity-checks.md`
```rust
/// Stakes an NFT by delegating it to the global authority PDA.
pub fn stake(ctx: Context<StakingAction>) -> Result<()> {
    [...]
    // Deserialize Metadata to verify collection
    let nft_metadata = Metadata::safe_deserialize(&mut ctx.accounts.nft_metadata.to_account_info().data.borrow_mut()).unwrap();
    if let Some(collection) = nft_metadata.collection {
        if collection.key.to_string() != CLAYNO_COLLECTION_ADDRESS {
            return Err(error!(StakingError::WrongCollection));
        }
    } else {
        return Err(error!(StakingError::InvalidMetadata));
    };
    [...]
}
```

**Example 3: [C-01] User Can Deny Opponent NFT Rewards By Marking Safe Post-Battle** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-01-user-can-deny-opponent-nft-rewards-by-marking-safe-post-battle.md`
```solidity
function markBeetleSafe(uint256 _tokenId) public {
  if (isStaked[_tokenId] != msg.sender) revert InvalidTokenOwner();
  safeBeetle[msg.sender] = _tokenId;

  emit SafeBeetleUpdated(msg.sender, _tokenId);
}
```

**Example 4: CASE SENSITIVE CHECK ALLOWS ADDING THE SAME NEAR FUNGIBLE TOKEN MORE THAN ONCE** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/case-sensitive-check-allows-adding-the-same-near-fungible-token-more-than-once.md`
```rust
fn register_near_fungible_token(
    &mut self,
    symbol: String,
    name: String,
    decimals: u8,
    contract_account: AccountId,
    price: U128,
) {
    self.assert_owner();
    let mut near_fungible_tokens = self.near_fungible_tokens.get().unwrap();
    assert!(
        !near_fungible_tokens.contains(&symbol),
        "Token '{}' is already registered.",
        &symbol
    );
    near_fungible_tokens.insert(&NearFungibleToken {
        metadata: FungibleTokenMetadata {
            spec: "ft-1.0.0".to_string(),
            symbol,
            name,
            decimals,
            icon: None,
            reference: None,
            reference_hash: None,
        },
        contract_account,
        price_in_usd: price,
        locked_balance: U128::from(0),
        bridging_state: BridgingState::Active,
    });
    self.near_fungible_tokens.set(&near_fungible_tokens);
}
```

**Example 5: CVGT Staking Pool State Manipulation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/cvgt-staking-pool-state-manipulation.md`
```rust
pub struct Initialize<'info> {
    #[account()]
    pub cvgt: Box<Account<'info, Mint>>,
}
```

**Variant: Signature Malleability - MEDIUM Severity Cases** [MEDIUM]
> Found in 38 reports:
> - `reports/cosmos_cometbft_findings/case-sensitive-check-allows-adding-the-same-near-fungible-token-more-than-once.md`
> - `reports/cosmos_cometbft_findings/eigen2-4-missing-constraint-check-for-modification-of-lookahead-time-of-slashabl.md`
> - `reports/cosmos_cometbft_findings/exchange-rate-not-updated-properly.md`

**Variant: Signature Malleability in Octopus Network Anchor** [MEDIUM]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/case-sensitive-check-allows-adding-the-same-near-fungible-token-more-than-once.md`
> - `reports/cosmos_cometbft_findings/lack-of-upper-limit-checks-allows-blocking-withdrawals.md`
> - `reports/cosmos_cometbft_findings/lack-of-validation-allows-setting-percentages-higher-than-a-hundred.md`

**Variant: Signature Malleability in Suzaku Core** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md`
> - `reports/cosmos_cometbft_findings/potential-underflow-in-slashing-logic.md`

**Variant: Signature Malleability in Sapien** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/getting-max-staking-rewards-possible-while-bypassing-the-lockup-periods.md`
> - `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in signature malleability logic allows exploitation through missing validation, 
func secureSignatureMalleability(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 72 audit reports
- **Severity Distribution**: HIGH: 34, MEDIUM: 38
- **Affected Protocols**: Munchables, Kilnfi Staking (Consensys), ZetaChain Cross-Chain, Persistence, Ethos EVM
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Signature Verification Missing
grep -rn 'signature|verification|missing' --include='*.go' --include='*.sol'
# Signature Replay
grep -rn 'signature|replay' --include='*.go' --include='*.sol'
# Signature Cross Chain Replay
grep -rn 'signature|cross|chain|replay' --include='*.go' --include='*.sol'
# Signature Forgery
grep -rn 'signature|forgery' --include='*.go' --include='*.sol'
# Signature Duplicate
grep -rn 'signature|duplicate' --include='*.go' --include='*.sol'
# Signature Eip155 Missing
grep -rn 'signature|eip155|missing' --include='*.go' --include='*.sol'
# Signature Key Management
grep -rn 'signature|key|management' --include='*.go' --include='*.sol'
# Signature Malleability
grep -rn 'signature|malleability' --include='*.go' --include='*.sol'
```

## Keywords

`accounting`, `allocations`, `allows`, `amount`, `antehandler`, `appchain`, `argument`, `attack`, `between`, `bypassing`, `chain`, `channel`, `check`, `checks`, `claims`, `collection`, `collision`, `cosmos`, `cross`, `deny`, `duplicate`, `eip155`, `enabling`, `ethereum`, `forgery`, `fork`, `from`, `functions`, `hard`, `historical`

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

`AnteHandle`, `Indexers`, `_verifySignatures`, `appchain`, `block.number`, `cosmos`, `cross_chain_replay`, `defi`, `deposit`, `depositBufferedEther`, `duplicate`, `eip155_missing`, `forgery`, `key_management`, `malicious`, `malleability`, `markBeetleSafe`, `mint`, `msg.sender`, `nonce_manipulation`, `receive`, `replay`, `signature`, `signature_replay_vulnerabilities`, `staking`, `verification_missing`
