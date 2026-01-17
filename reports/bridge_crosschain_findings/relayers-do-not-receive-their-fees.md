---
# Core Classification
protocol: Hinkal Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60152
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/hinkal-protocol/66b9b783-8b42-4a4e-89ed-3ef2a2df5958/index.html
source_link: https://certificate.quantstamp.com/full/hinkal-protocol/66b9b783-8b42-4a4e-89ed-3ef2a2df5958/index.html
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
finders_count: 7
finders:
  - Shih-Hung Wang
  - Ibrahim Abouzied
  - Jan Gorzny
  - Martin Derka
  - Ruben Koch
---

## Vulnerability Title

Relayers Do Not Receive Their Fees

### Overview


The client has reported a bug in the Hinkal.sol file where the formula used to calculate fees for token withdrawals is incorrect. This is due to the incorrect usage of parentheses in the code, resulting in the fee always being calculated as 0. The client has suggested removing the parentheses and applying the multiplication before division to fix the issue. The bug has been marked as fixed by the client.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `9afae61f817046de299b40a1248797b2d01b34c2`. The client provided the following explanation:

> The braces error has been taken care of

**File(s) affected:**`Hinkal.sol`

**Description:** When a token withdrawal is submitted to Hinkal through a relayer, relayers can receive a fee depending on the token transferred and the amount transferred. However, the formula to calculate these fees in `_internalTransact()` is incorrect due to the usage of parenthesis:

```
relayFee = uint256(-circomData.amountChanges[i]) * (relayPercentage / 10000);
```

Since the allowed range of values for the variable `relayPercentage` is `[0:500]`, the amount will always be multiplied by `0`, resulting in the `relayFee` taking the value `0`.

**Recommendation:** Apply the multiplication before division by removing the parenthesis.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Hinkal Protocol |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Ibrahim Abouzied, Jan Gorzny, Martin Derka, Ruben Koch, Valerian Callens, Fatemeh Heidari |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/hinkal-protocol/66b9b783-8b42-4a4e-89ed-3ef2a2df5958/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/hinkal-protocol/66b9b783-8b42-4a4e-89ed-3ef2a2df5958/index.html

### Keywords for Search

`vulnerability`

