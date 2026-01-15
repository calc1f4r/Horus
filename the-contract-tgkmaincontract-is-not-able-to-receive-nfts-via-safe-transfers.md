---
# Core Classification
protocol: Tengoku Senso
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60523
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/tengoku-senso/5361cc88-760a-4571-8284-7951b4dbbff4/index.html
source_link: https://certificate.quantstamp.com/full/tengoku-senso/5361cc88-760a-4571-8284-7951b4dbbff4/index.html
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
  - Shih-Hung Wang
  - Valerian Callens
  - Cameron Biniamow
---

## Vulnerability Title

The Contract `TGKMainContract` Is Not Able to Receive NFTs via Safe Transfers

### Overview


This report is an update on a previous bug that has been fixed by the client. The bug was related to the contract `TGKMainContract` not being able to receive ERC721 NFT tokens through certain functions. This was due to the contract not implementing the function `IERC721Receiver.onERC721Received()`. The recommendation is for the client to consider implementing this function in the contract to ensure safe transfer of NFT tokens.

### Original Finding Content

**Update**
The client implemented the recommended actions.

![Image 20: Alert icon](https://certificate.quantstamp.com/full/tengoku-senso/5361cc88-760a-4571-8284-7951b4dbbff4/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the client. Addressed in: `c47765595a3fc73626a0792b2460542e00935913`.

**File(s) affected:**`TGKMainContract.sol`

**Description:** The contract `TGKMainContract` is expected to receive ERC721 NFT tokens. These tokens can usually be received via different functions. Some of them, like `safeMint()` or `safeTransferFrom()` first check that the receiver address, if it is a contract, implements the function `IERC721Receiver.onERC721Received()`[described here](https://docs.openzeppelin.com/contracts/3.x/api/token/erc721#IERC721Receiver). If not, the NFT can remain stuck in the receiver contract. As the contract `TGKMainContract` does not implement the function `IERC721Receiver.onERC721Received()`, it will not be able to receive NFT tokens via any kind of safe transfer.

**Recommendation:** Consider implementing the function `IERC721Receiver.onERC721Received()` in the contract `TGKMainContract`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Tengoku Senso |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Valerian Callens, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/tengoku-senso/5361cc88-760a-4571-8284-7951b4dbbff4/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/tengoku-senso/5361cc88-760a-4571-8284-7951b4dbbff4/index.html

### Keywords for Search

`vulnerability`

