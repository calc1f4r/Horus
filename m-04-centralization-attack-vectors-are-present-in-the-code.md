---
# Core Classification
protocol: Nft Loots
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20621
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-NFT Loots.md
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
  - Pashov
---

## Vulnerability Title

[M-04] Centralization attack vectors are present in the code

### Overview


This bug report describes the potential for malicious or compromised owner/admin accounts to negatively impact the game, either by executing a rug pull or causing a denial of service (DoS). The bug report outlines five methods which can be used to cause the negative impacts, such as withdrawing all of the reward tokens or changing the randomness provider. The likelihood of this bug being exploited is low, however the impact is high. 

The bug report recommends limiting the usage of the methods by making them callable only under certain conditions or with specific arguments. This will help to reduce the likelihood of malicious or compromised owner/admin accounts exploiting the bug and causing negative impacts to the game.

### Original Finding Content

**Impact:**
High, as some accounts can execute a rug pull or brick the game

**Likelihood:**
Low, as it requires a malicious or compromised owner/admin account

**Description**

The owner accounts of both `NFTLootbox` & `VRFv2Consumer` contracts have the power to break the game while it is running.

- `NFTLootbox::withdrawERC20` can be used by the contract owner to execute a rug pull by withdrawing all of the reward tokens from the contract
- `NFTLootbox::withdrawERC721` can be used to steal the ERC721 tokens if the lootbox has closed but the game winner is still about to claim them
- `VRFv2Consumer::requestRandomWords` should only be callable by `NFTLootbox` - currently it can be forbidden that it is called from `NFTLootbox`, resulting in a DoS in a running game
- `NFTLootbox::changeVrfV2Consumer` can be used maliciously to update the randomness provider to an admin controlled one
- `NFTLootbox::changeBetCoin` shouldn't be callable while a game is running as if it's not a stablecoin then the `priceForPlay` will be very different

**Recommendations**

Limit the usage of those methods by either making them callable only in special conditions or with specific arguments.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nft Loots |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-NFT Loots.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

