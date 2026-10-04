---
# Core Classification
protocol: Heurist
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45791
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-04-Heurist.md
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

ExchangeRate manipulation via Donation

### Overview


This bug report mentions a problem with a function called donate() in the StHEU.sol contract. The function allows the owner of the contract to donate HEU tokens, which increases the totalHEU balance and affects the exchange rate. However, it was discovered that the owner could manipulate the exchange rate by donating a large number of tokens and then claiming more tokens than they originally vested. This poses a risk of centralization, where the owner could benefit from this manipulation. The recommendation is to restrict the donate() function to only be used during a specific time period, to prevent this manipulation from happening during normal operations. The comment states that the function has been removed from the contract. 

### Original Finding Content

**Severity** : High 

**Status**: Resolved

**Description**

The StHEU.sol  donate(uint256 amount) function allows the contract owner to donate HEU tokens to the contract. The donated tokens increase the totalHEU balance, which affects the exchange rate.

**Manipulation Scenario**:

The contract owner (or someone with control over the owner account) could donate a large number of HEU tokens to the contract, thereby increasing totalHEU and boosting the exchange rate.
With the exchange rate now inflated, the owner could claim previously vested stHEU tokens, receiving more HEU tokens than the value of the stHEU that was originally vested.
Since the donate() function can only be called by the owner, there is a centralization risk where the owner could manipulate the exchange rate to their benefit.

**Recommendation **

Restrict the donate() function to only allow donations when migrationMode is active, to avoid affecting the exchange rate during normal operations.

**Comment**: 

The donate() function has been removed from the contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Heurist |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-04-Heurist.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

