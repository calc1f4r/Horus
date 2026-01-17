---
# Core Classification
protocol: Rwa
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48929
audit_firm: Kann
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Kann Audits/2025-01-19-RWA.md
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
finders_count: 1
finders:
  - Kann Audits
---

## Vulnerability Title

[H-01] Cross-chain Replay in borrowAsset() & swapToBorrow()

### Overview


The bug being reported is related to a feature called "Cross-chain Replay". This feature allows users to borrow assets on one chain and then use the same signature on another chain. However, there is a problem where the same signature can be reused on multiple chains, which is not intended. 

To fix this issue, the recommendation is to include the chain ID in the hash used for generating the signature. This will make each signature unique to its respective chain and prevent cross-chain replay. 

### Original Finding Content

**Description**

Cross-chain Replay: If an User borrows assets on Chain A, they could reuse the same signature (generated from the same data) on Chain B, assuming the signature is valid for the same borrow hash structure on both chains.

**Recommendations**

```solidity
bytes32 _borrowHash = keccak256(
    abi.encode(
        collaterals,
        borrows,
        collateralAmounts,
        borrowsAmounts,
        msg.sender,
        nonceOf[msg.sender],
        block.chainid // Include the chainId in the hash to make it unique per chain
    )
);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Kann |
| Protocol | Rwa |
| Report Date | N/A |
| Finders | Kann Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Kann Audits/2025-01-19-RWA.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

