---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7284
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation
  - merkle_tree

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

Phony signatures can be used to forge any strategy

### Overview


This bug report is about a critical risk found in the VaultImplementation.sol#L249 of the code. The bug is related to the check performed to validate the signature in the In_validateCommitment() function. The check was miswritten, which allows any borrower to pass in any merkle root they'd like and sign it in a way that causes address(0) to return from ecrecover, and have their commitment validated. This can be done by submitting a phony signature. 

The recommendation to fix the bug is to change the check from recovered != owner() && recovered != s.delegate && recovered != address(0) to (recovered != owner() && recovered != s.delegate) || recovered == address(0). This was fixed in PR 209 and verified by Spearbit.

### Original Finding Content

## Security Report

## Severity
**Critical Risk**

## Context
`VaultImplementation.sol#L249`

## Description
In `in_validateCommitment()`, we check that the merkle root of the strategy has been signed by the strategist or delegate. After the signer is recovered, the following check is performed to validate the signature:

```plaintext
recovered != owner() && recovered != s.delegate && recovered != address(0)
```

This check seems to be miswritten, so that any time `recovered == address(0)`, the check passes. Whenever `ecrecover` is used to check the signed data, it returns `address(0)` in the situation that a phony signature is submitted. 

See this example for how this can be done. The result is that any borrower can pass in any merkle root they'd like, sign it in a way that causes `address(0)` to return from `ecrecover`, and have their commitment validated.

## Recommendation
Modify the check to:

```plaintext
if (
- recovered != owner() && recovered != s.delegate && recovered != address(0)
+ (recovered != owner() && recovered != s.delegate) || recovered == address(0)
) {
    revert IVaultImplementation.InvalidRequest(
        InvalidRequestReason.INVALID_SIGNATURE
    );
}
```

## Acknowledgements
- **Astaria**: Fixed in PR 209.
- **Spearbit**: Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, Merkle Tree`

