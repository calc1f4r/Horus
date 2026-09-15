---
# Core Classification
protocol: Sense
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6808
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Max Goodman
  - Denis Milicevic
  - Gerard Persoon
---

## Vulnerability Title

Do Not Use abi.encodedPacked With Multiple Dynamically-Sized Types

### Overview


This bug report is about a situation in which the abi.encodePacked method is called with multiple dynamically-sized types, which leads to ambiguity in unpacking. This can be dangerous when the contract becomes permissionless for adding custom zero/claim adapters. The recommendation is to use abi.encode instead and abi.decode to appropriately decode the externally called contract. This issue has been addressed in #156.

### Original Finding Content

## Severity: Medium Risk

## Context
- Fuse.sol#L242-L252
- Fuse.sol#L262-L272

## Situation
The `abi.encodePacked` method is called where there are multiple dynamically-sized types. Trying to pack these dynamically-sized types leads to ambiguity in unpacking. This makes it difficult to impossible to unpack, especially in a safe manner. It is made more difficult, in a case like this, because users have some limited input control over the contents passed via the `name` and `symbol` parameters. This could present a danger when the contract becomes permissionless for adding custom zero/claim adapters.

```solidity
bytes memory constructorDataZero = abi.encodePacked(
    zero,
    comptroller,
    zeroParams.irModel,
    ERC20(zero).name(),
    ERC20(zero).symbol(),
    cERC20Impl,
    "0x00",
    zeroParams.reserveFactor,
    adminFee
);
```

## Recommendation
`abi.encode` should be used here instead, and `abi.decode` to appropriately decode the externally called contract.

## Sense
Addressed in #156.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Sense |
| Report Date | N/A |
| Finders | Max Goodman, Denis Milicevic, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

