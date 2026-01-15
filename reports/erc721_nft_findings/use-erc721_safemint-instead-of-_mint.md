---
# Core Classification
protocol: Dexe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27306
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-10-cyfrin-dexe.md
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

protocol_categories:
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dacian
  - 0kage
---

## Vulnerability Title

Use `ERC721::_safeMint()` instead of `_mint()`

### Overview


This bug report is about the use of `ERC721::_safeMint()` instead of `ERC721::_mint()` in `AbstractERC721Multiplier::_mint()` and `ERC721Expert::mint()`. `ERC721::_mint()` can mint ERC721 tokens to addresses which don't support ERC721 tokens, while `ERC721::_safeMint()` ensures that ERC721 tokens are only minted to addresses which support them. OpenZeppelin discourages the use of `_mint()`. The recommended mitigation is to use `_safeMint()` instead of `_mint()` for ERC721.

However, the Dexe team won't use `_safeMint()` because it opens up potential re-entrancy vulnerabilities and they don't want to limit the decision over mints to be decided by DAOs in terms of who to send tokens to. If the project team believes the usage of `_mint()` is correct in this case, they should document a reason why in the code where it occurs.

### Original Finding Content

**Description:** Use `ERC721::_safeMint()` instead of `ERC721::_mint()` in `AbstractERC721Multiplier::_mint()` [L89](https://github.com/dexe-network/DeXe-Protocol/tree/f2fe12eeac0c4c63ac39670912640dc91d94bda5/contracts/gov/ERC721/multipliers/AbstractERC721Multiplier.sol#L89) & `ERC721Expert::mint()` [L30](https://github.com/dexe-network/DeXe-Protocol/tree/f2fe12eeac0c4c63ac39670912640dc91d94bda5/contracts/gov/ERC721/ERC721Expert.sol#L30).

**Impact:** Using `ERC721::_mint()` can mint ERC721 tokens to addresses which don't support ERC721 tokens, while `ERC721::_safeMint()` ensures that ERC721 tokens are only minted to addresses which support them. OpenZeppelin [discourages](https://github.com/dexe-network/DeXe-Protocol/tree/f2fe12eeac0c4c63ac39670912640dc91d94bda5/contracts/token/ERC721/ERC721.sol#L275) the use of `_mint()`.

If the project team believes the usage of `_mint()` is correct in this case, a reason why should be documented in the code where it occurs.

**Recommended Mitigation:** Use `_safeMint()` instead of `_mint()` for ERC721.

**Dexe:**
We won’t use `_safeMint()` because:

1. It opens up potential re-entrancy vulnerabilities,
2. The decision over mints is decided by DAOs. We won’t limit them in terms of who to send tokens to.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Dexe |
| Report Date | N/A |
| Finders | Dacian, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-10-cyfrin-dexe.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

