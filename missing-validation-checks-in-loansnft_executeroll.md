---
# Core Classification
protocol: Collar Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45139
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Collar-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Collar-Spearbit-Security-Review-December-2024.pdf
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
finders_count: 4
finders:
  - R0bert
  - Om Parikh
  - 0xDjango
  - MiloTruck
---

## Vulnerability Title

Missing validation checks in LoansNFT._executeRoll()

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
LoansNFT.sol#L736-L740

## Description
In `LoansNFT._executeRoll()`, only `canOpenPair()` is checked for the rolls contract, as shown below:

```solidity
(Rolls rolls, uint rollId) = (rollOffer.rolls, rollOffer.id);
// check this rolls contract is allowed
require(configHub.canOpenPair(underlying, cashAsset, address(rolls)), "loans: unsupported rolls");
// taker matching roll's taker is not checked because if doesn't match, roll should check / fail
// offer status (active) is not checked, also since rolls should check / fail
```

The function currently does not explicitly check the following conditions, and instead relies on `rolls.executeRoll()` to revert:

- `takerNFT` in both contracts match (i.e. `rolls.takerNFT() == takerNFT`).
- `cashAsset` in both contracts match (i.e. `rolls.cashAsset() == cashAsset`).
- The `takerId` stored in `rollId` matches `loanId` (i.e. `rolls.getRollOffer(rollId).takerId == _takerId(loanId)`).

If `takerNFT`, `cashAsset`, or `takerId` do not match, `executeRoll()` reverts as there is no approval from `LoansNFT` to `Rolls` for `rolls.takerNFT`. However, this is not a strong guarantee.

## Recommendation
Explicitly check the conditions listed above:

```solidity
// check this rolls contract is allowed
require(configHub.canOpenPair(underlying, cashAsset, address(rolls)), "loans: unsupported rolls");
// taker matching roll's taker is not checked because if doesn't match, roll should check / fail
// offer status (active) is not checked, also since rolls should check / fail
require(rolls.takerNFT() == takerNFT, "loans: takerNFT mismatch");
require(rolls.cashAsset() == cashAsset, "loans: cashAsset mismatch");
require(rolls.getRollOffer(rollId).takerId == _takerId(loanId), "loans: takerId mismatch");
```

## Collar
Fixed in commit `897a702d` by adding some of the suggested checks (and some additional ones).

## Spearbit
Verified, the `takerNFT` check has been added, which implicitly guarantees `cashAsset` in both contracts also match. Note that the roll offer's `takerId` is still not checked to match `loanId`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Collar Protocol |
| Report Date | N/A |
| Finders | R0bert, Om Parikh, 0xDjango, MiloTruck |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Collar-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Collar-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

