---
# Core Classification
protocol: Mode Earnm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29267
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
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
finders_count: 2
finders:
  - Dacian
  - 0kage
---

## Vulnerability Title

Transferring mystery boxes bricks token redemption

### Overview


The MysteryBox contract is an ERC1155 contract which allows users to transfer tokens to other addresses via in-built transfer functions. However, when users try to redeem their tokens using the MysteryBox::claimMysteryBoxes() function, it reverts unless the caller is the same address who minted the box. This is because the internal mappings that track mystery box ownership are never updated when transfers occur.

This issue has an impact on token redemption, as users may not be able to transfer their mystery box from one address to another, or to sell their mystery box on platforms like OpenSea which support ERC1155 sales.

The recommended mitigation for this issue is to override the ERC1155 transfer hooks to either prevent transferring of mystery boxes, or to update the internal mappings so that when mystery boxes are transferred, the new owner address can redeem their tokens. The second option is more attractive for the protocol, as it allows mystery box holders to access liquidity without putting sell pressure on the token, creating a "secondary market" for mystery boxes.

The issue has been fixed in commit a65a50c by overriding ERC1155::_beforeTokenTransfer() to prevent mystery boxes from being transferred. The fix has been verified.

### Original Finding Content

**Description:** `MysteryBox` is an `ERC1155` contract which users expect to be able to transfer to other addresses via the in-built transfer functions. But `MysteryBox::claimMysteryBoxes()` [reverts](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L296) unless the caller is the same address who minted the box since the internal mappings that track mystery box ownership are never updated when transfers occur.

**Impact:** Token redemption is bricked if users transfer their mystery box. Users reasonably expect to be able to transfer their mystery box from one address they control to another address (if for example their first address is compromised), or they may wish to sell their mystery box on platforms like OpenSea which support `ERC1155` sales.

**Recommended Mitigation:** Override `ERC1155` transfer hooks to either prevent transferring of mystery boxes, or to update the internal mappings such that when mystery boxes are transferred the new owner address can redeem their tokens. The second option may be more attractive for the protocol as it allows mystery box holders to access liquidity without putting sell pressure on the token, creating a "secondary market" for mystery boxes.

**Mode:**
Fixed in commit [a65a50c](https://github.com/Earnft/smart-contracts/commit/a65a50ca8af4d6abc58d3c429785bcd82182c04e) by overriding `ERC1155::_beforeTokenTransfer()` to prevent mystery boxes from being transferred.

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Mode Earnm |
| Report Date | N/A |
| Finders | Dacian, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

