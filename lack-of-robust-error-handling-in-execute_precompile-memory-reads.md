---
# Core Classification
protocol: ZKsync Protocol Precompiles Implementation Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55343
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/zksync-protocol-precompiles-implementation-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Lack of Robust Error Handling in execute_precompile Memory Reads

### Overview

See description below for full details.

### Original Finding Content

The `execute_precompile` method does not adequately handle memory read failures, leading to silent failures where invalid inputs are misinterpreted as valid elliptic curve points. Specifically, when memory reads fail without triggering exceptions ([returning zeros instead](https://github.com/matter-labs/zksync-protocol/blob/97162ccf21bb80be6f543307d93588f290720fc0/crates/zk_evm/src/reference_impls/memory.rs#L110-L115)), the code incorrectly treats these as legitimate `(0,0)` points, which represent the point at infinity in elliptic curve cryptography.

If a memory read fails and returns `(0,0)`, the system does not differentiate between a legitimate input and a failure-induced default. This introduces several security risks:

* **Silent Failure:** The system does not raise an error even if the user did not provide a valid elliptic curve point. Instead, it performs an operation that may seem correct but is semantically incorrect due to hidden errors.
* **Ambiguity in Input Handling:** The system assumes that `(0,0)` is always a deliberate input, failing to distinguish it from memory read failures.
* **Attack Vector for Cryptographic Manipulation:** An attacker could exploit this behavior by crafting inputs that force `(0,0)` as an operand (manipulating input offsets or memory pages to areas they know will return zeros rather than fail outright), effectively bypassing part of an elliptic curve operation.
* **Protocol Inconsistencies:** If the precompile is used in a higher-level protocol, operations that should fail may silently produce seemingly valid results, breaking security assumptions.

To prevent these issues, the implementation should:

1. **Explicitly verify memory read success** before using the values in cryptographic computations. If `execute_partial_query` does not provide a failure indicator, additional validation should be implemented.
2. **Differentiate between intentional `(0,0)` inputs and memory failure-induced defaults** by introducing explicit error checks.
3. **Enforce memory access validation** before performing elliptic curve operations to ensure that out-of-bounds or corrupted reads do not lead to incorrect cryptographic behavior.

***Update:** Acknowledged, not resolved. The Matter Labs team stated:*

> *We do believe it is not an issue, and the reason for this is the context in which code is used. Crypto precompiles can be called only via precompile\_call opcode on EraVM. The way VM handles precompile\_call - it checks that address of contract that calls precompile\_call is 0x01 then the ecrecover circuit is executed under the hood if the contract address is 0x02 it will do sha logic, if the contract address is 0x08 then it does ecpairing logic. But also note, that 0x08 has predeployed bytecode of https://github.com/matter-labs/era-contracts/blob/draft-v28/system-contracts/contracts/precompiles/EcPairing.yul#L134. Which means the circuit logic which you reviewed will be only executed with a constraints on which EcPairing contract living (with all of memory invariants and etc).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | ZKsync Protocol Precompiles Implementation Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/zksync-protocol-precompiles-implementation-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

