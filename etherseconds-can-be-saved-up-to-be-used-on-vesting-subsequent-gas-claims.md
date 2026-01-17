---
# Core Classification
protocol: DRAFT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29887
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-contracts-review-draft.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-contracts-review-draft.pdf
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
  - Milo Truck
  - Christoph Michel
  - Csanuragjain
  - Desmond Ho
---

## Vulnerability Title

etherSeconds can be saved up to be used on vesting subsequent gas claims

### Overview

See description below for full details.

### Original Finding Content

## Security Analysis Report

## Severity: Low Risk
### Context: Gas.sol#L216
**Description:**  
etherSeconds is the integral of unclaimed ether over time (ether * seconds vested). There is no limit to its accumulation, so etherSeconds continues to grow while gas remains unclaimed. This allows the accumulated gas to be "saved up" and be used for subsequent gas claims to be claimed at the maximum ceiling rate immediately.

**Recommendation:**  
Consider imposing an upper bound to the accumulation of etherSeconds at `etherBalance * ceilGasSeconds`.

---

## Severity: Low Risk
### Context: USDConversions.sol#L76, PSM
**Description:**  
The USD yield manager converts between stablecoins. For the USDC to DAI path, it always uses the PSM USDC contract's `sellGem` function. The PSM takes on debt to mint DAI through the `vat.frob(ilk, ..., int256(gemAmt18), int256(gemAmt18))` call. This call can fail if the ilk (the PSM's USDC collateral) hits its line (its debt limit), or the Line (total overall debt limit) is exceeded.

```solidity
require(either( /*...*/ , both(_mul(ilk.Art, ilk.rate) <= ilk.line, debt <= Line)),
"Vat/ceiling-exceeded");
```

Direct USDC deposits could be disabled in this case. The current debt limit (as of writing) is set to 789,651,294 USD and 242,649,337 debt is used.

**Recommendation:**  
Consider checking if enough USDC can be sold into the PSM (`inputWad <= vat.ilks(psm.ilk()).line / RAY - vat.ilks(psm.ilk()).Art`), otherwise, use a different conversion path. Alternatively, add an option for the user to define what conversion path should be used. Furthermore, consider keeping the conversion system upgradeable in case the current USDC PSM is deprecated.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | DRAFT |
| Report Date | N/A |
| Finders | Milo Truck, Christoph Michel, Csanuragjain, Desmond Ho |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-contracts-review-draft.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-contracts-review-draft.pdf

### Keywords for Search

`vulnerability`

