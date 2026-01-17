---
# Core Classification
protocol: Reth
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36035
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/reth/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/reth/review.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

ECIES Protocol Bugs

### Overview

See description below for full details.

### Original Finding Content

## Description
There are bugs within the ECIES protocol that are not specific to the Reth implementation. While these are security considerations, the security impact is not significant enough to warrant immediate patching.

## Forgeable signatures
The function `recover_ecdsa()` allows recovering a public key from a message hash and signature. It is trivial to forge a valid signature if the message hash is selected by the attacker. In ECIES, the attacker is able to set the message hash to `x ^ nonce` where `x` is the ECDH x-coordinate and `nonce` is arbitrarily chosen by the attacker.

An attacker is able to select an arbitrary message hash. To set an arbitrary message hash, first calculate `ECDH x` then select the desired final message hash. Finally, set `nonce = x ^ messageHash`, such that `messageHash = x ^ nonce`.

The impact here is that the attacker can choose any `remote_ephemeral_public_key` without knowing the secret key. The impact is not severe, as this ephemeral key is only used to calculate the shared secret. If the attacker does not know the shared secret, they cannot encrypt or decrypt messages with this peer. The connection will not be able to share Hello messages and will error or be dropped after a timeout.

## Authentication without knowledge of public key secret
It is possible to pass the ECIES Auth / Ack handshake without knowledge of a public key secret. This also occurs due to `recover_ecdsa()`, as if we provide a random message and signature, there is around a 50% chance it will succeed and return a valid public key, for which no one knows the secret.

Again, this style of attack will result in an encrypted connection to which the attacker does not know the shared secret. This will allow them to open a connection but be unable to encrypt and share the Hello message, resulting in an error or timeout.

## Auth / Ack packets are replayable
There is no expiry on Auth or Ack packets. Therefore, an attacker is able to re-use an existing handshake by replaying an Auth packet. This would result in a handshake without knowledge of the shared secret, and as such, no more messages can be encrypted or decrypted by the attacker.

## Recommendations

## Forgeable signatures
The `x` and `nonce` values should be concatenated then hashed rather than using XOR. This would prevent the attacker from selecting a specific message hash.

## Authentication without knowledge of public key secret
To resolve this issue, include the public key in the message hash. That is hash `ephemeral_public_key`, `x`, and `nonce`. To facilitate the message hashing, the ephemeral public key would need to be passed as a field in the message.

## Auth / Ack packets are replayable
Auth and Ack messages should have an expiry timestamp or nonce. A timestamp is the quickest and easiest way to prevent replay, though it allows replay before the timestamp expires. A nonce is more secure but requires long-term storage, which will have resource consumption considerations.

## RETH-45 Large base_fee Overflows Block Base Fee Calculations
**Asset**: crates/reth/primitives/src/basefee.rs  
**Status**: Closed: See Resolution  
**Rating**: Informational

## Description
A large `base_fee` may cause an overflow when adding change. This would require the previous base fee plus the increase to overflow a `u64`, which is unlikely.

```rust
pub fn calculate_next_block_base_fee(
    gas_used: u64,
    gas_limit: u64,
    base_fee: u64,
    base_fee_params: crate::BaseFeeParams,
) -> u64 {
    // Calculate the target gas by dividing the gas limit by the elasticity multiplier.
    let gas_target = gas_limit / base_fee_params.elasticity_multiplier;
    
    match gas_used.cmp(&gas_target) {
        // If the gas used in the current block is equal to the gas target, the base fee remains the same (no increase).
        std::cmp::Ordering::Equal => base_fee,
        
        // If the gas used in the current block is greater than the gas target, calculate a new increased base fee.
        std::cmp::Ordering::Greater => {
            // Calculate the increase in base fee based on the formula defined by EIP-1559.
            base_fee + // @audit can overflow if base_fee is large
            (std::cmp::max(
                // Ensure a minimum increase of 1.
                1,
                base_fee as u128 * (gas_used - gas_target) as u128 /
                (gas_target as u128 * base_fee_params.max_change_denominator as u128),
            ) as u64)
        }
    }
}
```

## Recommendations
Consider using `saturating_add()`.

## Resolution
The issue is marked as won’t fix by the development team. The variable `base_fee` has been increased from a `u64` to `u128` and is therefore unlikely to overflow.

## RETH-46 Missing Documentation for Untrusted NippyJar and Compact Formatted Data
**Asset**: crates/storage/codecs & crates/storage/nippy-jar  
**Status**: Resolved: See Resolution  
**Rating**: Informational

## Description
The NippyJar and Compact encoding formats and their implementations are designed for storing and retrieving data internally. They are not hardened to safely read potentially malicious data. Documentation should clearly and visibly warn against misuse.

For example, the Compact encoding does not allow limiting the length values to protect against allocating extremely large vectors. The implementation can trivially panic after reading a length value that is larger than the size of the buffer being read from (out of bounds with a range slicing operation). Similarly, the `decode_varuint()` function will panic with "could not decode varuint" when passed malformed data.

The NippyJar implementation can similarly panic after reading offset values that exceed the bounds of the data file. The testing team notes that these formats are used safely in Reth for internal storage purposes. However, because these modular components are also intended to be used as libraries in other projects, it is important that documentation warns against their misuse.

## Recommendations
Ensure crate documentation and README files clearly warn against using the Compact and NippyJar formats to read untrusted data.

## Resolution
Documentation has been added in PR #8345.

## RETH-47 Missing Panic Comments in from_compact()
**Asset**: crates/reth/primitives/src/transaction/mod.rs  
**Status**: Resolved: See Resolution  
**Rating**: Informational

## Description
Numerous implementations of the trait Compact, specifically the function `from_compact()`, may panic. There are `unreachable!()` statements that would cause a panic if reached. These panics could be triggered on certain input. However, the calling function is the compact codec in storage, and so these will only be reached if bad data is added to the storage database. As these panics are not reachable unless there is an invalid database entry, this is not likely to occur. However, there should be doc comments stating how and why these panics could occur.

For example, `Transaction::from_compact()` has multiple `unreachable!()` statements that could be reached with an identifier larger than 3.

```rust
fn from_compact(mut buf: &[u8], identifier: usize) -> (Self, &[u8]) {
    match identifier {
        0 => {
            let (tx, buf) = TxLegacy::from_compact(buf, buf.len());
            (Transaction::Legacy(tx), buf)
        }
        1 => {
            let (tx, buf) = TxEip2930::from_compact(buf, buf.len());
            (Transaction::Eip2930(tx), buf)
        }
        2 => {
            let (tx, buf) = TxEip1559::from_compact(buf, buf.len());
            (Transaction::Eip1559(tx), buf)
        }
        3 => {
            // An identifier of 3 indicates that the transaction type did not fit into
            // the backwards compatible 2 bit identifier, their transaction types are
            // larger than 2 bits (eg. 4844 and Deposit Transactions). In this case,
            // we need to read the concrete transaction type from the buffer by
            // reading the full 8 bits (single byte) and match on this transaction type.
            let identifier = buf.get_u8() as usize;
            match identifier {
                3 => {
                    let (tx, buf) = TxEip4844::from_compact(buf, buf.len());
                    (Transaction::Eip4844(tx), buf)
                }
                #[cfg(feature = "optimism")]
                126 => {
                    let (tx, buf) = TxDeposit::from_compact(buf, buf.len());
                    (Transaction::Deposit(tx), buf)
                }
                _ => unreachable!("Junk data in database: unknown Transaction variant"), // @audit should have a panic comment for this case
            }
        }
        _ => unreachable!("Junk data in database: unknown Transaction variant"), // @audit should have a panic comment for this case
    }
}
```

## Recommendations
It is recommended to update the transaction signature of `from_compact()` to return an error. This error can handle any of the deserialization issues that may occur and exit gracefully.

## Resolution
Additional documentation has been added in PR #8346.

## RETH-48 is_database_empty() False Positive For Paths That Are Not Directories
**Asset**: crates/storage/db/src/utils.rs  
**Status**: Resolved: See Resolution  
**Rating**: Informational

## Description
The utility function `is_database_empty()` takes a path parameter and returns a boolean value indicating whether the path corresponds to an empty database. The function returns true for paths that exist but are not directories, which may be unexpected.

Though unusual, this could be encountered if the Reth data directory contains a file named “db”. No security implications were identified for this issue, hence an informational severity.

### Detail
The following test function constitutes a proof of concept. The test fails if `is_database_empty()` returns true when passed a path to a non-empty file.

```rust
#[test]
fn not_empty_if_db_path_is_a_file() {
    let base_dir = tempdir().unwrap();
    let db_file = base_dir.as_ref().join("db");
    fs::write(&db_file, b"Lorem ipsum").unwrap();
    let result = is_database_empty(&db_file);
    // would expect the function to return false
    assert!(!result);
}
```

When the same path is passed to `init_db()` at `crates/storage/db/src/lib.rs:97`, the path is treated as if it is a valid but empty database directory. Fortunately, an error is safely returned at line [103] when trying to create a directory at that path:

```
Error {
    msg: "Could not create database directory /tmp/.tmp6h66uI/db",
    source: CreateDir {
        source: Os {
            code: 17,
            kind: AlreadyExists,
            message: "File exists",
        },
        path: "/tmp/.tmp6h66uI/db",
    },
},
```

## Recommendations
Consider whether `is_database_empty()` should return false or an error when passed a path to a non-directory.

## Resolution
The recommendation has been implemented in PR #8351.

## RETH-49 BlockchainTreeConfig Concerns Regarding Fixed Finalisation Depth
**Asset**: crates/blockchain-tree/src/config.rs  
**Status**: Open  
**Rating**: Informational

## Description
There are several inaccuracies in the `BlockchainTreeConfig` that appear to indicate misunderstandings surrounding the consensus layer’s fork-choice and finality mechanisms.

Consider the following excerpt that defines the default values for `BlockchainTreeConfig`:

```rust
// Gasper allows reorgs of any length from 1 to 64.
max_reorg_depth: 64,
// This default is just an assumption. Has to be greater than the `max_reorg_depth`.
max_blocks_in_chain: 65,
```

1. The comment at line [28] is inaccurate. When the network is unhealthy and unable to finalize, it is possible to have reorgs of a depth with no fixed bounds (much greater than 64).
2. Relying on a `max_reorg_depth` is potentially dangerous. From the perspective of the Ethereum protocol, there is no “maximum reorg depth” other than the last finalized block. If the implementation’s correctness relies on any fixed depth value, it may fail to agree with other EL implementations during adverse network conditions (when consensus is most important).
3. The `max_blocks_in_chain` field is unused in the codebase under review and has no effect.

This issue is focused on the comments and config definitions, which do not appear to pose a direct security risk, hence an informational severity rating.

## Recommendations
Evaluate whether these findings indicate misunderstood assumptions that need to be rectified elsewhere in the codebase and design. Additionally:

1. Correct or remove the comment at line [28].
2. If making use of a fixed `max_reorg_depth` in the in-memory Blockchain Tree, ensure there is an alternate recovery pathway that allows processing larger reorgs. This could involve rebuilding the state from some on-disk checkpoint. In this case, consider also renaming and documenting the field to indicate that the limit is only for Blockchain Tree, rather than Reth as a whole. Otherwise, consider removing the `max_reorg_depth` field and modifying code that relies on it.
3. Consider whether `max_blocks_in_chain` should remain unused. If so, remove the unnecessary field.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Reth |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/reth/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/reth/review.pdf

### Keywords for Search

`vulnerability`

