---
# Core Classification
protocol: Nemeos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59589
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
source_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
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
finders_count: 3
finders:
  - Sebastian Banescu
  - Faycal Lalidji
  - Guillermo Escobero
---

## Vulnerability Title

NFT Is Always Transferred to the Original Borrower

### Overview


The bug report describes an issue with the NFTWrapper tokens, which are used for loans. When a borrower repays their loan, the NFTWrapper token is supposed to be burned and the underlying NFT is sent back to the borrower. However, the tokens can currently be transferred to other addresses, which can be confusing for users as they will not receive the underlying NFT. The recommendation is to either make the tokens untransferrable or transfer the NFT to the actual owner of the token.

### Original Finding Content

**Update**
Fixed in `29cba2f8b59263c4e010bb0d61d1b5a1b0f9e0c2`. `NFTWrapper` tokens were made non-transferrable.

**Description:** When a borrower repays the full loan amount, the NFTWrapper token associated with that loan is burned, and the underlying NFT is sent to the original borrower that created the loan.

However, this behavior can be unexpected, as the NFTWrapper mints ERC-721 tokens that can be transferred to other addresses. Other users can exchange tokens by NFTWrapper tokens, but in the end, they will not get the underlying NFT.

**Recommendation:** Revise this use case. If the NFTWrapper tokens are not expected to be traded or transferred, consider making the tokens untransferrable. If they are expected to be transferred, consider transferring the NFT to the actual owner of the NFTWrapper token.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Nemeos |
| Report Date | N/A |
| Finders | Sebastian Banescu, Faycal Lalidji, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html

### Keywords for Search

`vulnerability`

