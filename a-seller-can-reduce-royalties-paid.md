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
solodit_id: 60648
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html
source_link: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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

A Seller Can Reduce Royalties Paid

### Overview


The client has acknowledged a bug where a malicious seller can reduce the royalties they have to pay when creating a listing. This is because the allocated royalties per token depends on the number of tokens in the listing. The exploit scenario involves the seller creating or using other tokens with low royalties and including them in the listing with the main token. This results in the seller paying lower royalties overall. The recommendation is to rework the design of how royalties are allocated in a listing.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation: "We do not see that as a concern, as we have a standard marketplace fee of 10% (subject to change at the discretion of the company). We do not want to hard code the 10% fee on change, as it may change in the future. Since we control the royalties share setting, we understand the risks associated with varied shares across token. We acknowledge that if we were to adjust the marketplace fee, it would be adjusted across all tokens."

**Description:** When creating a listing, a malicious seller can reduce the royalties they have to pay. This is because the allocated royalties per token depends on the number of tokens in a listing.

**Exploit Scenario:** Let us assume that address A wants to sell their `BlockBarBottle` token id 1. They can reduce the royalties paid for it as follows:

1.   Address A creates / uses other `BlockBarBottle` tokens X with low royalties. In the best case for A, they are a collector for those tokens X.

2.   A includes as many of those X tokens as possible in the listing together with token id 1.

3.   The full amount paid for the listing is evenly spread across all tokens included.

4.   A pays much lower royalties in total as the allocated royalties for token id 1 decreases with every other token X in the listing. A might even take profit if they are a sufficiently high collector on the X tokens.

**Recommendation:** The issue lies in the fact that royalties are evenly spread across all items in the listing. This design needs to be reworked.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

