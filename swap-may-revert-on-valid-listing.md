---
# Core Classification
protocol: Block
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60645
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html
source_link: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Danny Aksenov
  - Adrian Koegl
  - Hytham Farah
  - Guillermo Escobero
---

## Vulnerability Title

`swap()` May Revert on Valid Listing

### Overview


This bug report is about a problem in the `Marketplace.sol` file where the `fullShare` variable is not properly calculated in the `Marketplace.swap()` function. This can lead to an underflow of the variable, causing transactions to be reverted when using `solidity 0.8.18`. The recommendation is to adjust the calculation to consider the share of each collector based on the token's share in the listing. The report suggests two approaches to fix this issue, with the second one being the more precise solution. 

### Original Finding Content

**Update**
Addressed in: `72c5a25e2d7eb40a1ec3b972db878fe61019f585`. The client removed share derivation, no risk of underflowing the `fullShare`.

**File(s) affected:**`Marketplace.sol`

**Description:** In `Marketplace.swap()L#129`, the `fullShare` variable is adjusted and later emitted in `L#138`. It is calculated by subtracting all collector shares of all tokens in the listing by the `FEE_DENOMINATOR`.

 Nevertheless, it does not consider the share of each collector conditioned on the token's share in the listing. Therefore, a valid listing might underflow the `fullShare` variable when the share of all royalties on all tokens adds up to more than `FEE_DENOMINATOR`. When using `solidity 0.8.18`, a transaction is reverted if a variable underflows.

**Recommendation:** Adjust the calculation such that the share is conditioned on the tokens share in the listing. With a naive approach, this can be achieved by replacing L129 with the following:

```
fullShare -= share / listing.tokenIds.length
```

However, to avoid loss of precision, we recommend the following approach which first adds the shares, and finally divides and subtracts from `FEE_DENOMINATOR`:

```
uint256 fullShare = 0;
```

```
fullShare += share;
```

```
fullShare = FEE_DENOMINATOR - (share / listing.tokenIds.length);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Block |
| Report Date | N/A |
| Finders | Danny Aksenov, Adrian Koegl, Hytham Farah, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html

### Keywords for Search

`vulnerability`

