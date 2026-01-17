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
solodit_id: 18000
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

A malicious transaction can cause a read overrun

### Overview

See description below for full details.

### Original Finding Content

## Type: Configuration
**Target:** deps/ledger-zxlib/dockerized_build.mk

## Difficulty: High

## Description

The `base32_encode` function is not guaranteed to null-terminate its output. If an encoded `formattedAddress` value is just the right length, `strlen` will read past its end and will not be null-terminated.

```c
// Now prepare the address output
if ((formattedAddress + formattedAddressSize - (payload_crc, int 2), 2) < 0) {
    return 0;
}
return strlen((char *) formattedAddress);
```

**Figure 3.1:** Formatted address encoding on lines 312–320 of `crypto.c`.

The `formattedAddress` function is called from `parser_getItem`, which is called upon the transaction receipt to parse the CBOR payload. The following base64-encoded CBOR payload triggers this read overrun:

```
iQBYMQMKAAD//////////wAAAAAAAAAAAEIAiQAAQAAAQMD5RAD///////8AAAAAAAAAAABCAIkAQEAAAEA=
```

And the read overrun corresponds to this valid CBOR input structure:

```
[0, 
 b'\x03\n\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00
 \x00B\x00\x89\x00\x00@\x00\x00@\xc0\xf9D\x00\xff\xff\xff\xff\xff\xff\x00\x00\x00
 \x00\x00\x00\x00\x00\x00', 
 b'\x00\x89', 
 0, 
 b'', 
 b'', 
 0, 
 0, 
 b'']
```

This finding has low severity because although it can cause the app to crash, there seems to be no other way to exploit the bug.

## Exploit Scenario

A maliciously crafted transaction causes the app to crash.

## Recommendation

- **Short term:** Fix this data validation issue. This may simply require an additional check after the call to `base32_encode` to see if the output buffer's full length was used instead of `strlen`.

- **Long term:** Prefer safer alternatives to C-string functions, e.g., `strnlen`, particularly when dealing with user-controllable binary data such as Filecoin transaction data. Also, regularly run fuzz testing against APIs that deal with user-controllable data. As part of this assessment, we have provided several fuzz testing targets, which are discussed in more detail in **Appendix C**.

## Remediation

- Length-bounded string comparison was added in commit `9d6036e4`.

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

