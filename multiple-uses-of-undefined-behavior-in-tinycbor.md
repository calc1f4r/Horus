---
# Core Classification
protocol: Ledger Filecoin App
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18002
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/LedgerFilecoin.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/LedgerFilecoin.pdf
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
  - Brad Larsen | ​Trail of Bits Evan Sultanik | ​Trail of Bits
---

## Vulnerability Title

Multiple uses of undefined behavior in ​tinycbor

### Overview

See description below for full details.

### Original Finding Content

## Undefined Behavior in the Filecoin App

## Description

The `tinycbor` library, which is a dependency of the Ledger Filecoin app, invokes undefined behavior in several places when it processes user-controllable transaction data. These appear to be previously undiscovered bugs in the third-party `tinycbor` library and are not due to flaws inherent in the Ledger Filecoin code itself. These issues were discovered toward the end of the engagement, and there was insufficient time to determine whether they are exploitable.

A standards-conforming C compiler is under no obligations when a program invokes undefined behavior, and the resulting behavior cannot be safely reasoned about. Changes to anything, including compiler toolchain version, build flags, target hardware, operating system, system header files, application source code, etc., could result in different observable behavior. This includes applying a non-zero offset to a null pointer, as well as numeric over- and underflows.

The former behavior is due to pointer arithmetic that, in certain code paths, allows a null pointer to be offset by `SIZE_MAX`. The `iterate_string_chunks` function is called with the erroneous arguments in several instances, including `string copying` and `string length calculation`. Despite invoking undefined behavior, these functions currently appear to compile to semantically correct code for the Ledger devices. However, compiler optimization changes are not guaranteed to preserve this behavior. The behavior can be reproduced with virtually any valid CBOR input that contains strings.

Note that the "offsetting a NULL pointer" undefined behavior does not pose an immediate risk to the Ledger Filecoin app, but it could become a problem in the future. Starting with LLVM 10, the optimizer in Clang takes advantage of this and could unexpectedly eliminate code. It is undetermined whether newer versions of GCC take advantage of this.

The latter undefined behavior related to numeric over- and underflow is of more concern on Ledger devices. It appears this behavior can be triggered by passing a large value as the version parameter in the Filecoin transaction’s CBOR payload, and may occur because there’s no check for the `CborIteratorFlag_IntegerValueTooLarge` flag in the `tinycbor` function `cbor_value_get_int64`.

## Undefined Behaviors Identified

When built with Clang 10 and Undefined Behavior Sanitizer, the `fuzz-parser_parse` target reveals the following undefined behaviors:

1. **Applying Zero Offset to Null Pointer**  
   ```plaintext
   deps/tinycbor/src/cborparser.c:1126:37: runtime error: applying zero offset to null pointer
   #0 0x57f801 in iterate_string_chunks deps/tinycbor/src/cborparser.c:1126:37
   ```

2. **Applying Non-Zero Offset to Null Pointer**  
   ```plaintext
   deps/tinycbor/src/cborparser.c:1136:33: runtime error: applying non-zero offset 2 to null pointer
   #0 0x57fe63 in iterate_string_chunks deps/tinycbor/src/cborparser.c:1136:33
   ```

3. **Negation of Out-of-Bounds Integer**  
   ```plaintext
   deps/tinycbor/src/cbor.h:375:19: runtime error: negation of -9223372036854775808 cannot be represented in type 'int64_t' (aka 'long'); cast to an unsigned type to negate this value to itself
   #0 0x5668d1 in cbor_value_get_int64 deps/tinycbor/src/cbor.h:375:19
   ```

4. **Signed Integer Overflow**  
   ```plaintext
   deps/tinycbor/src/cbor.h:375:28: runtime error: signed integer overflow: -9223372036854775808 - 1 cannot be represented in type 'long'
   #0 0x56693a in cbor_value_get_int64 deps/tinycbor/src/cbor.h:375:28
   ```

![Figure 5.1: Fuzz Testing to Reveal the Undefined Behavior](path_to_image)

## Exploit Scenario

An attacker could craft a malicious Filecoin transaction that makes the `tinycbor` code invoke undefined behavior, which could cause the Ledger device to crash or the transaction to be mishandled.

## Recommendations

**Short Term**  
1. Run your test suites with Address Sanitizer and Undefined Behavior Sanitizers enabled. 
2. Run the fuzz testing targets added during this assessment. Seek clarification on these issues from the TinyCBOR developers, potentially by opening GitHub issues on their project.

**Long Term**  
Consider a focused security assessment and/or security hardening engagement for the `tinycbor` dependency.

## References

- [Ledger Security Guidelines](https://ledger.readthedocs.io/en/latest/additional/security_guidelines.html?highlight=overflow#integer-overflows-underflows)
- [LLVM Review D67122](https://reviews.llvm.org/D67122)
- [LLVM Revision rL369789](https://reviews.llvm.org/rL369789)

## Remediation

The `tinycbor` library was locally patched to remove the undefined behavior caused by offsetting a null pointer in commit `860b25af`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Ledger Filecoin App |
| Report Date | N/A |
| Finders | Brad Larsen | ​Trail of Bits Evan Sultanik | ​Trail of Bits |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/LedgerFilecoin.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/LedgerFilecoin.pdf

### Keywords for Search

`vulnerability`

