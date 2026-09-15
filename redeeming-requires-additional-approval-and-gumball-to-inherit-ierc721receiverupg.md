---
# Core Classification
protocol: Gumball
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57491
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-27-Gumball.md
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
  - Zokyo
---

## Vulnerability Title

Redeeming requires additional approval and Gumball to inherit IERC721ReceiverUpgradeable.

### Overview


The report discusses a bug in the Gumball.sol file where additional approval is required for redeeming Gumball NFTs. This is due to the use of an external call to the safe TransferFrom function. The bug can be fixed by either using the internal_transfer function or implementing the onERC721Received function. The post-audit comment states that the issue has been resolved, but it is recommended to verify if the approval for Gumball is still necessary for redeeming NFTs.

### Original Finding Content

**Description**

Gumball.sol

Due to external call of safe TransferFrom on address(this), Redeeming required additional approval of Gumball NFTs by the user. It also requires Gumball to inherit IERC721Receiver Upgradeable and implement onERC721Received() function. Although issue is marked as critical, since currently redeem() reverts due to absence of onERC721Received() implemented, it should be verified, in case another version of ERC721 is used, where this check is missed.

**Recommendation**

Either use internal_transfer() function instead of external safe TransferFrom() or implement onERC721Received(). Verify the necessity of additional approval tokens for Gumball in order to perform redeeming.

**Re-audit comment**

Resolved.

Post-audit:

transferFrom() is used, which doesn't call onERC721Received(). Approval to Gumball for redeeming NFTs remained.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Gumball |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-27-Gumball.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

