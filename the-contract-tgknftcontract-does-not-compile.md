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
solodit_id: 60524
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

The Contract `TGKNFTContract` Does Not Compile

### Overview


This bug report is about a contract called `TGKNFTContract` that is not compiling correctly. The report suggests that the contract is missing inheritance declarations and gives two specific errors. The report recommends explicitly inheriting from `ERC721` and making a change to the `override` instruction.

### Original Finding Content

**Update**
It is now possible to compile the contracts (commit `1f8ba861cc5895ca46920a930967a749abae7678`).

![Image 23: Alert icon](https://certificate.quantstamp.com/full/tengoku-senso/5361cc88-760a-4571-8284-7951b4dbbff4/static/media/info-icon-alert.3c9578483b1cf3181c9bfb6fec7dc641.svg)

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> In our Hardhat configuration file, we set the Solidity compiler version to 0.8.18. By including this configuration in the Hardhat file, we ensure that the contracts are compiled using the Solidity version 0.8.18. This version will be used when compiling and deploying the contracts using Hardhat. If we make the changes suggested by you, we get the following error: Invalid contract specified in override list: "ERC721URIStorage".

**File(s) affected:**`TGKNFTContract.sol`

**Description:** The contract `TGKNFTContract` does not compile due to incorrect inheritance declarations and gives two errors:

```
1. Error (4327): Function needs to specify overridden contract "ERC721URIStorage". => needs to override ERC721URIStorage (since it is explicitly inherited)
2. Error (2353): Invalid contract specified in override list: "ERC721". => should not override ERC721 (since it is not explicitly inherited)
```

In detail, the contract `TGKNFTContract` does not inherit `ERC721`, and the function `supportsInterface()` is missing `ERC721URIStorage` from its override list.

**Recommendation:**

Consider:

1.   explicitly inheriting from `ERC721` by adding `ERC721` in `TGKNFTContract is ERC721, ERC721URIStorage, ERC721Enumerable`.
2.   replacing the instruction `override(ERC721, ERC721Enumerable)` with the instruction `override(ERC721, ERC721URIStorage, ERC721Enumerable)`.

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

