---
# Core Classification
protocol: NFTonPulse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60463
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nf-ton-pulse/7880ca8f-d4d5-4407-ad57-1c0dabe6b187/index.html
source_link: https://certificate.quantstamp.com/full/nf-ton-pulse/7880ca8f-d4d5-4407-ad57-1c0dabe6b187/index.html
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
  - Michael Boyle
  - Hytham Farah
  - Mostafa Yassin
  - Guillermo Escobero
---

## Vulnerability Title

Multi Claiming ERC1155 Vouchers

### Overview


The bug report addresses an issue with the `NFTVoucher` for `NFT1155` contract. This contract does not include a nonce, which could allow for the voucher to be replayed multiple times, resulting in the minting of more tokens than intended. While the function attempts to mitigate this by adding a check, it may not be sufficient for ERC1155 tokens. The recommendation is to add a nonce value to the `NFTVoucher` struct to prevent this issue.

### Original Finding Content

**Update**
Addressed in: `157b890be9446783e01250e2f8f5907546cb9b00` and `d8212bb720cb022a856a432d640bf32d7252e60d`

Added more controls and checks to ensure that only the correct users have the ability to mint vouchers and write sensitive information on the NFT like URI info and royalty information.

**File(s) affected:**`NFT1155`

**Description:** The `NFTVoucher` for `NFT1155` contract does not include a nonce. In the case of `NFT721`, there is no need for a nonce, since the `tokenId` acts as an implicit nonce. Since you cannot mint more than one token of the same ID.

However, for ERC1155, you can mint multiple tokens with the same `tokenID`.

This means that the voucher can be replayed multiple times to mint more than once.

The function attempts to mitigate that by adding the check:

```
require(
      _tokensMinted[voucher.tokenId] + amount <= voucher.amount,
      'Exceeded mint limit'
    );
```

However, this only allows a max amount of `voucher.amount` for `voucher.tokenId` which might not be the desired behavior with ERC1155 tokens.

**Recommendation:** Add a nonce value to the `NFTVoucher` struct.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | NFTonPulse |
| Report Date | N/A |
| Finders | Michael Boyle, Hytham Farah, Mostafa Yassin, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nf-ton-pulse/7880ca8f-d4d5-4407-ad57-1c0dabe6b187/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nf-ton-pulse/7880ca8f-d4d5-4407-ad57-1c0dabe6b187/index.html

### Keywords for Search

`vulnerability`

