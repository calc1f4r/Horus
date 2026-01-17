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
solodit_id: 57490
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

XGBT, pegged to Gumball NFTs, can be withdrawn directly for GBT.

### Overview


Gumbar.sol is a platform where users can receive and redeem XGBT tokens by staking GBT or Gumball NFTs. However, there is a bug where if XGBT tokens received for staking Gumball NFTs are transferred to another address using standard ERC20 transfer functions, the locked NFTs are not transferred along with them. This allows for the possibility of XGBT tokens being redeemed for GBT without the required NFTs, causing problems for other users and potentially locking NFTs forever. The recommendation is to transfer the locked NFTs to the other user's locks when XGBT tokens are transferred. This bug has been resolved in the latest commit.

### Original Finding Content

**Description**

Gumbar.sol. Gumbar allows users to receive and redeem XGBT it two ways: by staking GBT and by staking Gumball NFTs. It is checked against an amount of NFTs locked by the user, that XGBT, pegged to Gumballs, cannot be redeemed directly for GBT tokens. However, in case XGBT, received for staking Gumball NFTs, are transferred with standard ERC20 transfer functions to another address, locked NFTs are not transferred to the other address'es locked NFTs as well. Due to this, XGBT, which were minted for Gumball NFTs, can now be redeemed for GBT tokens. This can lead to scenarios, where there won't be enough GBT for other users, preventing them from receiving their funds and scenarios, where Gumball NFTs are locked forever.

**Recommendation**

Transfer locked NFTs to other user's locks in case transferred XGBT are pegged to Gumball NFTS.

**Re-audit comment**

Resolved.

Post-audit:

XGBT can be transferred to limited number of addresses, such as the Gumbar itself, BondingCurve, zero address. The commit with fix is 22d3a460059225a51c8face497afd4a60a36802d.

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

