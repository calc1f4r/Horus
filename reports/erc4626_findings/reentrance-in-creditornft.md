---
# Core Classification
protocol: Creditswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37102
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
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
  - Zokyo
---

## Vulnerability Title

Reentrance in `CreditorNFT`

### Overview


Bug report: 
The Checks Effects interactions (CEI) pattern is not being followed in the _deposit() function of the CreditorNFT contract. This could potentially result in a reentrancy attack if the debt token being used has hooks that transfer calls to untrusted contracts. It is recommended to use the CEI pattern or a Reentrancy Guard from Openzeppelin to prevent this type of exploit. The bug has been resolved.

### Original Finding Content

**Severity**: Medium

**Status**:  Resolved

**Description**

The Checks Effects interactions (CEI) is not being followed in _deposit() of the CreditorNFT contract. This is because the safeTransferFrom is called on line: 182 on the debt token. If the debt token is an ERC20 token that implements hooks like beforeTransferFrom() or afterTransferFrom() which transfer calls to untrusted contracts, then this could result in reentrancy. Again this is would be a griefing attack for the attacker as he would be losing more than gaining.

**Recommendation**: 

It is still advised to use checks effects interactions pattern or use Reentrancy Guard from Openzeppelin to avoid cross function or cross-contract reentrancy exploits.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Creditswap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

