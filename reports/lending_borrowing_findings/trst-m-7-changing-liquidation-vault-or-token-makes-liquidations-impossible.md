---
# Core Classification
protocol: Stella
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19059
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
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
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-7 Changing liquidation vault or token makes liquidations impossible

### Overview


This bug report is about an issue with UniswapV3Strategy. When the contract is initialized, it approves spending of the liquidation token to the liquidation vault. The addresses of the vault and the token are read from the Config contract, which allows the “exec” role to change them. However, after liquidation vault or token is changed, token spending is not re-approved, resulting in liquidations always reverting. 

The team recommended allowing any spender address in the BaseStrategy.approve() function to mitigate this issue. The team then fixed the issue by extending target approval to either liquidation vault or router in `BaseStrategy.approve()`.

### Original Finding Content

**Description:**
When UniswapV3Strategy is initialized, it approves spending of the liquidation token to the 
liquidation vault. The addresses of the vault and the token are read from the Config contract, 
which allows the “exec” role to change them. However, after liquidation vault or token is 
changed, token spending is not re-approved. As a result, liquidations will always revert 
because the new vault won’t be able to take liquidation tokens from the strategy contract (or 
the old vault won’t be able to take the new liquidation token, if the token was changed).

**Recommended Mitigation:**
Strategy contracts need a (restricted) way to approve arbitrary tokens to arbitrary addresses. 
BaseStrategy.approve() allows that, but it only approves to whitelisted routers. Thus, our 
recommendation is to allow any spender address in the BaseStrategy.approve() function.

**Team response:**
Fixed

**Mitigation Review:**
The team addressed this issue by extending target approval to either liquidation vault or 
router in `BaseStrategy.approve()`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Stella |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

