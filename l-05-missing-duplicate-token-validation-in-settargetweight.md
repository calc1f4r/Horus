---
# Core Classification
protocol: Hyperhyper_2025-03-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57763
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperhyper-security-review_2025-03-30.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-05] Missing duplicate token validation in `setTargetWeight`

### Overview

See description below for full details.

### Original Finding Content

The `setTargetWeight` function lacks validation for duplicate tokens in the input array, which could lead to inconsistent weight assignments. Here's the problematic code:

```solidity
function setTargetWeight(TokenWeight[] calldata tokens)
    external
    onlyRole(AccessControlStorage.DEFAULT_ADMIN_ROLE)
{
    PoolStorage.AssetsConfig storage assets = PoolStorage.layout().setUp.assets;
    uint256 nTokens = tokens.length;
    if (nTokens != assets.allAssets.length()) revert PoolErrors.RequireAllTokens();

    uint256 total;
    TokenWeight memory item;
    uint256 weight;
    for (uint8 i; i < nTokens;) {
        item = tokens[i];
        assert(assets.allAssets.contains(item.token));
        weight = assets.isListed[item.token] ? item.weight : 0;
        assets.targetWeights[item.token] = weight;
        total += weight;
        // ... increment i
    }
    assets.totalWeight = total;
}
```

The issue arises because:

1. The function only checks if the number of tokens matches assets.allAssets.length().
2. There is no validation to ensure each token appears exactly once in the input array.
3. If a token appears multiple times in the input array:
   - Each occurrence will overwrite the previous weight assignment.
   - Only the last occurrence's weight will be stored.
   - The `totalWeight` calculation will include all occurrences.

To mitigate this issue, it is recommended to add validation to ensure each token appears exactly once(by checking address ordering).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperhyper_2025-03-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperhyper-security-review_2025-03-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

