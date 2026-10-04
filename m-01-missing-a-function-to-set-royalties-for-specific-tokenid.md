---
# Core Classification
protocol: BeamNodes_2025-01-28
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55378
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/BeamNodes-security-review_2025-01-28.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Missing a function to set royalties for specific tokenId

### Overview


This bug report is about a missing function in a code that is used to set royalty information for a specific token. The current code has a function called `resetDefaultRoyalty` that clears the royalty information, but there is no function to set it. The report suggests adding a new function called `setRoyaltyForId` that can set the royalty information for a specific token. This will help fix the issue and make the code more complete.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `resetDefaultRoyalty` function is used to clear the royalty information set for specific tokenId.

```solidity
    function resetDefaultRoyalty(uint256 _tokenId) external onlyRole(ADMIN_ROLE) {
        _resetTokenRoyalty(_tokenId);
        emit ResetDefaultRoyalty(_tokenId);
    }
```

However, there is a lack of a function to set royalty information for specific tokenId.

## Recommendations

Add a function to set royalty information for specific tokenId.

```diff
+   function setRoyaltyForId(uint256 _tokenId, address _receiver, uint96 _feeNumerator) external onlyRole(ADMIN_ROLE) {
+       _setTokenRoyalty(_tokenId, _receiver, _feeNumerator);
+       emit ResetDefaultRoyalty(_tokenId);
+   }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | BeamNodes_2025-01-28 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/BeamNodes-security-review_2025-01-28.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

