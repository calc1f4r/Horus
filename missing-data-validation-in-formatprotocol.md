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
solodit_id: 17999
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

Missing data validation in ​formatProtocol()

### Overview

See description below for full details.

### Original Finding Content

## Data Validation Report

**Type:** Data Validation  
**Target:** app/src/crypto.c  

**Difficulty:** Medium  

## Description

The `formatProtocol()` function has incomplete data validation logic. Before `decompressLEB128(addressBytes + 1)` is called, there is no check to ensure that the input buffer argument is large enough, which could lead to a read overrun.

```c
uint16_t formatProtocol(
    uint8_t *addressBytes,
    const uint16_t addressSize,
    uint8_t *formattedAddress,
    const uint16_t formattedAddressSize
) {
    if (formattedAddress == NULL) {
        return 0;
    }
    
    MEMZERO(formattedAddress, formattedAddressSize);
    const uint8_t protocol = addressBytes[0];
    
    formattedAddress[0] = (isTestnet() ? (protocol + 't') : (protocol + '0'));
    
    uint16_t payloadSize = 0;
    
    switch (protocol) {
        case ADDRESS_PROTOCOL_ID: {
            uint64_t val = 0;
            if (!decompressLEB128(addressBytes + 1, &val)) {
                return 0;
            }
            if (uint64_to_str((char *) formattedAddress + 2, (formattedAddressSize - 2), val) != NULL) {
                return 0;
            }
            return strlen((const char *) formattedAddress);
        }
    }
}
```

**Figure 2.1:** Missing data validation on lines 251–280 of `crypto.c`.

**Note:** Presently, this is not an exploitable issue due to the exact details of the code, and because the input buffer is sufficiently large along every execution path that could call `formatProtocol`.

## Exploit Scenario

A vulnerable execution path to this function could be introduced in future codebase modifications. An attacker may craft a malicious transaction that calls `decompressLEB128` with a buffer that is too small, potentially causing a Ledger device to crash or leading to data exfiltration.

## Recommendation

Short term, to enhance defense-in-depth and prevent this from becoming a real issue with future code changes, add a check to `formatProtocol` to ensure the input buffer is large enough before calling `decompressLEB128`. This will require a single conditional and should align with the existing data validation patterns in the surrounding code.

Long term, regularly test the codebase and perform fuzz testing with Address Sanitizer to detect similar issues.

## Remediation

- Input size was added as an argument to `decompressLEB128` in commit `9d6036e4`.
- Output buffer size was increased to ensure ample padding in commit `dd29f1db`.
- Fuzzing target was added for the `decompressLEB128` function.

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

