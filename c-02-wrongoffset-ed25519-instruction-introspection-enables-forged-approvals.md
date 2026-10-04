---
# Core Classification
protocol: Enclave_2025-10-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63519
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Enclave-security-review_2025-10-25.md
github_link: none

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

protocol_categories:
  - algo-stables
  - bridge
  - cross_chain
  - decentralized_stablecoin
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[C-02] Wrong‑Offset Ed25519 instruction introspection enables forged approvals

### Overview


The report discusses a bug found in a program that accepts off-chain approvals by verifying an Ed25519 signature. The current verifier does not perform essential validations, allowing attackers to craft preceding instructions that cause the program to accept invalid signatures. This can result in unauthorized borrows from the pool and block legitimate users from redeeming their approvals. The recommendation is to harden the verification process by checking the previous instruction's program ID, only allowing one signature and no auxiliary accounts, using inline mode, and checking for matching public key, message, and signature.

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** High

## Description

The program accepts off‑chain approvals by “verifying” an Ed25519 signature via the instruction sysvar: `borrow` expects the previous instruction in the same transaction to be a native Ed25519 verification and then inspects that instruction’s raw data to decide whether the signature is valid.

However, the current verifier does not perform the essential validations that make this pattern sound:

* It does not assert that the previous instruction’s `program_id` is the native Ed25519 program.
* It does not enforce “inline mode” by requiring the three `*_instruction_index` fields in `Ed25519SignatureOffsets` to be `0xFFFF` (meaning use data from this very Ed25519 instruction).
* It relies on reading specific byte ranges inside the Ed25519 instruction data, but does not validate that the supplied offsets and sizes actually point to those ranges.

On Solana, the Ed25519 verifier is flexible: the instruction can specify offsets and instruction indexes for where to read the signature, public key, and message. If a contract does not validate those fields, an attacker can craft a preceding instruction that causes the Ed25519 program to verify a signature over attacker‑controlled data, while placing benign‑looking bytes (the expected signer pubkey, message hash, signature) at the locations your program later checks. Your verifier will then return success even though no signature from an authorized signer was actually validated.

As a result, any caller can submit a transaction that includes a maliciously constructed “verification” instruction immediately before `borrow` and have the program accept it as valid. That enables unauthorized borrows from the pool and increments the user’s nonce, potentially blocking the legitimate user from later redeeming a genuine approval.

## Recommendations

Harden the Ed25519 verification to treat the previous instruction as valid evidence only if all of the following are true:

* The previous instruction’s `program_id` is the native Ed25519 program.
* The instruction encodes exactly one signature and carries no auxiliary accounts.
* All three `*_instruction_index` fields in `Ed25519SignatureOffsets` are `0xFFFF` (inline mode), so the signature, public key, and message are taken from the same Ed25519 instruction.
* All offsets and sizes are bounds‑checked against the instruction data length before slicing.
* The inline public key, message, and signature bytes exactly match the expected authorized signer and message.
* If `borrow` is the first instruction, reject (there is no “previous” verification to inspect).





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Enclave_2025-10-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Enclave-security-review_2025-10-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

