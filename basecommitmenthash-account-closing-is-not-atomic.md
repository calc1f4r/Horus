---
# Core Classification
protocol: Elusiv
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48625
audit_firm: OtterSec
contest_link: https://elusiv.io/
source_link: https://elusiv.io/
github_link: github.com/elusiv-privacy/elusiv.

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Harrison Green
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

BaseCommitmentHash Account Closing is not Atomic

### Overview


This report describes a bug in a system where a user can exploit a feature to repeatedly request the same action, leading to farming rewards from the system. The bug occurs when a user deposits funds and the system computes a BaseCommitmentHash, which is added to a global merkle tree. The instruction used to enqueue this hash can be called multiple times on the same account, allowing an attacker to farm rewards. The bug has been fixed by deactivating the account before closing it, preventing multiple calls to the instruction.

### Original Finding Content

## Handling Deposits in the System

When a user deposits new funds into the system, the protocol must first compute the `BaseCommitmentHash`, which represents a base commitment, the amount deposited, and the token type. This stage can be performed in parallel – each user using a separate `BaseCommitmentHashingAccount` to track the state of the computation.

Next, this base commitment is added to the global Merkle tree, which requires computing all of the pairwise hashes from the updated leaf to the root. This step must happen synchronously since the protocol uses a single, global Merkle tree.

## Instruction: FinalizeBaseCommitmentHash

The instruction used to enqueue the base commitment hash is `FinalizeBaseCommitmentHash`:

```rust
pub fn finalize_base_commitment_hash<'a>(
    original_fee_payer: &AccountInfo<'a>,
    commitment_hash_queue: &mut CommitmentQueueAccount,
    hashing_account_info: &AccountInfo<'a>,
    _hash_account_index: u64,
) -> ProgramResult {
    let data = &mut hashing_account_info.data.borrow_mut()[..];
    let hashing_account = BaseCommitmentHashingAccount::new(data)?;
    guard!(hashing_account.get_is_active(), ComputationIsNotYetFinished);
    guard!(hashing_account.get_fee_payer() == original_fee_payer.key.to_bytes(), InvalidAccount);
    guard!(
        (hashing_account.get_instruction() as usize) == BaseCommitmentHashComputation::INSTRUCTIONS.len(),
        ComputationIsNotYetFinished
    );
    let commitment = hashing_account.get_state().result();
    let mut commitment_queue = CommitmentQueue::new(commitment_hash_queue);
    commitment_queue.enqueue(
        CommitmentHashRequest {
            commitment: fr_to_u256_le(&commitment),
            fee_version: u64_as_u32_safe(hashing_account.get_fee_version()),
            min_batching_rate: hashing_account.get_min_batching_rate(),
        }
    )?;
    // Close hashing account
    close_account(original_fee_payer, hashing_account_info)
}
```

This instruction takes the temporary `hashing_account` (containing the base commitment hash) and enqueues it in the singleton `commitment_hash_queue`. Once the request has been enqueued, it closes the temporary hashing account by transferring all the rent lamports back to the original fee payer.

However, since rent is not enforced immediately after each instruction in Solana, this hashing account may stay alive across multiple instructions if the instructions are included in a single transaction. With this mechanism, an attacker can invoke `FinalizeBaseCommitmentHash` multiple times in a row on the same hashing account in order to enqueue many duplicate requests. Following this, the attacker can invoke the subsequent crank instructions to farm rewards from the pool.

## Patch

This vulnerability has been fixed in commit `33a542` by explicitly deactivating the hashing account before closing it. While the account may stay alive for several more instructions, subsequent calls to `FinalizeBaseCommitmentHash` will fail. 

© 2022 OtterSec LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Elusiv |
| Report Date | N/A |
| Finders | Harrison Green, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://elusiv.io/
- **GitHub**: github.com/elusiv-privacy/elusiv.
- **Contest**: https://elusiv.io/

### Keywords for Search

`vulnerability`

