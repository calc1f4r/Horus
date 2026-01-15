---
# Core Classification
protocol: Arcana
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20337
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-12-01-Arcana.md
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

[M-01] If address is a smart contract that can't handle ERC721 tokens they will be stuck after a whitelisted mint

### Overview


This bug report focuses on the `mintPublic` method of the `ArcanaPrime` smart contract. The method has a check that only allows external owned accounts (EOAs) to call it, but this check is missing in the whitelisted mint methods (`mintArcanaList`, `mintAspirantList`, `mintAllianceList`). This means that if the address that is whitelisted is a contract and it calls those functions, but it can't handle ERC721 tokens correctly, they will be stuck.

The impact of this bug is that a user can potentially lose their newly minted tokens forever, resulting in a loss of value. As it requires the user to be using a smart contract that does not handle ERC721 properly, it is considered to be of Medium severity.

The recommendation to fix this bug is to change the `_mint` call in `mintArcanaList`, `mintAspirantList` and `mintAllianceList` to `_safeMint`. It is advised to also add a `nonReentrant` modifier as this adds a reentrancy possibility.

### Original Finding Content

**Proof of Concept**

The `mintPublic` method has a check that allows only EOAs to call it

```solidity
if (tx.origin != msg.sender) revert ContractsNotAllowed();
```

but it is missing in the whitelisted mint methods (`mintArcanaList`, `mintAspirantList`, `mintAllianceList`). This means that if the address that is whitelisted is a contract and it calls those functions but it can't handle ERC721 tokens correctly, they will be stuck. This problem is usually handled by using `_safeMint` instead of `_mint` but all `mint` functionality in `ArcanaPrime` uses `_mint`.

**Impact**

This can result in a user losing his newly minted tokens forever, which is a potential values loss. It requires the user to be using a smart contract that does not handle ERC721 properly, so it is Medium severity.

**Recommendation**

In `mintArcanaList`, `mintAspirantList` and `mintAllianceList` change the `_mint` call to `_safeMint`. Keep in mind this adds a reentrancy possibility, so it is best to add a `nonReentrant` modifier as well.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Arcana |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-12-01-Arcana.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

