---
# Core Classification
protocol: NiftyApes - Seller Financing
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60497
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nifty-apes-seller-financing/edbc671f-08c9-44ab-b24c-c3807c9ef43d/index.html
source_link: https://certificate.quantstamp.com/full/nifty-apes-seller-financing/edbc671f-08c9-44ab-b24c-c3807c9ef43d/index.html
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
  - Michael Boyle
  - Ibrahim Abouzied
  - Hytham Farah
  - Jonathan Mevs
---

## Vulnerability Title

Funds May Be Sent to Sanctioned Address

### Overview


The client has reported a bug in the `SellerFinancing.sol` file. The current code allows payments to be made to a sanctioned seller, which can lead to the seller seizing the NFT without the buyer receiving their funds. The recommendation is to update the code to refund the buyer if the seller is sanctioned, which will help prevent this issue. Resolving a previous issue, NFTY-3, can also help mitigate this bug. The client has marked this bug as "Fixed" and it has been addressed in a specific code update.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `9594cb328b26a37c15582d737e3e06ef452b6eec`. The client provided the following explanation: Add return of funds to buyer if seller is sanctioned.

**File(s) affected:**`SellerFinancing.sol`

**Description:**`_makePayment()` currently allows payments to a sanctioned seller. If a buyer refuses (or is under legal obligation not) to send funds to the sanctioned seller, once enough time has passed, the sanctioned seller can transfer the ticket to a non-sanctioned address and seize the NFT. If a sanctioned seller does this near the end of the payment plan, then they will have effectively stolen all the funds from the buyer.

**Recommendation:** Update `_conditionalSendValue()` to refund the buyer when the `to` address is sanctioned. This will allow them to close out their loan without paying any more funds (aside from potential royalties). Resolving [NFTY-3](https://certificate.quantstamp.com/full/nifty-apes-seller-financing/edbc671f-08c9-44ab-b24c-c3807c9ef43d/index.html#findings-qs3) can help mitigate this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | NiftyApes - Seller Financing |
| Report Date | N/A |
| Finders | Michael Boyle, Ibrahim Abouzied, Hytham Farah, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nifty-apes-seller-financing/edbc671f-08c9-44ab-b24c-c3807c9ef43d/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nifty-apes-seller-financing/edbc671f-08c9-44ab-b24c-c3807c9ef43d/index.html

### Keywords for Search

`vulnerability`

