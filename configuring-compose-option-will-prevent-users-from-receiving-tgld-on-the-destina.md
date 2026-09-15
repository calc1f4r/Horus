---
# Core Classification
protocol: Templedao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33579
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
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
  - Hans
---

## Vulnerability Title

Configuring compose option will prevent users from receiving TGLD on the destination chain

### Overview


The bug report discusses an issue where users are unable to receive TGLD tokens when using the `send` function of the TempleGold contract. This is because the `_lzReceive` function on the destination chain blocks messages with compose options. This means that users who call `send` with compose option will not receive their tokens, resulting in a loss of funds. The recommended solution is to either revert if the `_sendParam` includes compose option or to only input mandatory fields from users and construct the `SendParam` within the `send` function. The bug has been fixed in PR 1029 by TempleDAO and has been verified by Cyfrin. 

### Original Finding Content

**Description:** Users are able to send their TGLD by calling `send` function of TempleGold contract.
Since `SendParam` struct is passed from users, they can add any field including compose data into the message.
However on the destination chain, in `_lzReceive` function, it blocks messages with compose options in it:
```Solidity
if (_message.isComposed()) { revert CannotCompose(); }
```

This means that users who call `send` with compose option, they will not receive TGLD tokens on the destination chain.

**Impact:** Token transfer does not work based on the parameter and causes loss of funds for users.

**Recommended Mitigation:**
1. In `send` function, if the `_sendParam` includes compose option, it should revert.
2. Even better, `send` function only inputs mandatory fields from users like the amount to send, and it constructs `SendParam` in it rather than receiving it as a whole from the user.

**TempleDAO:** Fixed in [PR 1029](https://github.com/TempleDAO/temple/pull/1029)

**Cyfrin:** Verified

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Templedao |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

