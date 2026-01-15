---
# Core Classification
protocol: Pyth Oracle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48817
audit_firm: OtterSec
contest_link: https://pyth.network/
source_link: https://pyth.network/
github_link: https://github.com/pyth-network/pyth-client.

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
finders_count: 3
finders:
  - Robert Chen
  - OtterSec
  - William Wang
---

## Vulnerability Title

Incorrect rent exemption checks

### Overview

See description below for full details.

### Original Finding Content

## Program Requirements

The program requires that all writable accounts be rent-exempt; this is enforced within the `valid_signable_account` and `valid_writable` functions.

## Code Snippet

```c
oracle.c:L38-L57

static bool valid_signable_account( SolParameters *prm,
                                    SolAccountInfo *ka,
                                    uint64_t dlen ) {
    return ka->is_signer &&
           ka->is_writable &&
           SolPubkey_same( ka->owner, prm->program_id ) &&
           ka->data_len >= dlen &&
           is_rent_exempt( *ka->lamports, dlen );
}

static bool valid_writable_account( SolParameters *prm,
                                     SolAccountInfo *ka,
                                     uint64_t dlen ) {
    return ka->is_writable &&
           SolPubkey_same( ka->owner, prm->program_id ) &&
           ka->data_len >= dlen &&
           is_rent_exempt( *ka->lamports, dlen );
}
```

However, the `is_rent_exempt` calculation is performed with the minimum required length `dlen`, rather than the account’s actual length `ka->data_len`. This allows an attacker to create a larger-than-required account which is not rent-exempt.

## Proof of Concept

Consider the following scenario:

- An attacker attempts to initialize a product account with a 1024-char buffer and 4,454,400 lamports. Note that `PC_PROD_ACC_SIZE` is 512.
- The program does not reject the instruction, since the lamport balance is sufficient for a 512-char buffer.

To conclude, the attacker was able to use a larger-than-required account to bypass the rent exemption check.

## Remediation

The rent exemption checks in `valid_signable_account` and `valid_writable_account` should be replaced with the following:

```c
is_rent_exempt( *ka->lamports, ka->data_len );
```

## Patch

Pyth Data Association acknowledges the finding and developed a patch for this issue: `#168`.

## General Findings

Here we present a discussion of general findings during our audit. While these findings do not present an immediate security impact, they do represent anti-patterns and could introduce a vulnerability in the future.

| ID              | Description                                  |
|-----------------|----------------------------------------------|
| OS-PYO-SUG-00   | Unused quote-set data                        |
| OS-PYO-SUG-01   | Test instructions remain in production       |
| OS-PYO-SUG-02   | Test instructions do not check exponent      |
| OS-PYO-SUG-03   | Potential out-of-bounds read in PD arithmetic|
| OS-PYO-SUG-04   | Potential integer overflows in PD arithmetic  |

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pyth Oracle |
| Report Date | N/A |
| Finders | Robert Chen, OtterSec, William Wang |

### Source Links

- **Source**: https://pyth.network/
- **GitHub**: https://github.com/pyth-network/pyth-client.
- **Contest**: https://pyth.network/

### Keywords for Search

`vulnerability`

