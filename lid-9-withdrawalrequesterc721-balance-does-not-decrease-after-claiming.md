---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53477
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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
  - Hexens
---

## Vulnerability Title

[LID-9] WithdrawalRequestERC721 balance does not decrease after claiming

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** WithdrawalRequestERC721.sol:balanceOf#L112-L115

**Description:**

A withdrawal request implements ERC721 and so acts as an NFT. Once a withdrawal request is claimed, it cannot be transferred anymore and NFT should have been burned.

This is also apparent from `WithdrawalQueue.sol:claimWithdrawal` (L214-238) where a `Transfer` event from the owner to `address(0)` for the request ID is emitted, which suggests a burn of the withdrawal request NFT.

However, we found that claimed withdrawals are still counted in the NFT balance of a user when calling `balanceOf`. This is due to the withdrawal request not being removed from the `requestsByOwner` mapping.
```
function balanceOf(address _owner) external view override returns (uint256) {
    if (_owner == address(0)) revert InvalidOwnerAddress(_owner);
    return _getRequestsByOwner()[_owner].length();
}
```

**Remediation:**  Remove the withdrawal request from the `requestsByOwner` mapping upon claiming. The request and its data will still available in the `queue` mapping.

**Status:**  Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

