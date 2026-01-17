---
# Core Classification
protocol: Arkis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59955
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/arkis/07924f14-1727-4e72-8e7a-2bc71aa735dd/index.html
source_link: https://certificate.quantstamp.com/full/arkis/07924f14-1727-4e72-8e7a-2bc71aa735dd/index.html
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
finders_count: 3
finders:
  - Julio Aguilar
  - Ibrahim Abouzied
  - Hytham Farah
---

## Vulnerability Title

Debt Entries Can Be Overwritten

### Overview


A bug was reported by the client and has been marked as "Fixed". The bug affects the files `DebtLibrary.col`, `Fund.sol`, and `MoneyAccountant.sol`. The issue occurs when the function `Fund.forward()` is executed and calls `MoneyAccount.spendMoney()`. If this function is called multiple times in the same block with the same parameters, it can cause previous debt entries to be overwritten and not all debt will be accounted for. This is because the `block.timestamp` acts as a salt instead of a true nonce. The recommendation is to use a different source for the nonce if `Fund.forward()` can be called with the same parameters in a single block.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `f12aeacb9b0f6015270cfdf3ca1602217739bd6a`.

**File(s) affected:**`DebtLibrary.col`, `Fund.sol`, `MoneyAccountant.sol`

**Description:** Part of the execution flow of `Fund.forward()` involves calling `MoneyAccount.spendMoney(amount, reward, block.timestamp)`, where `block.timestamp` serves as a nonce. If `spendMoney()` is called more than once in the same block with identical parameters, any child calls to `createDebtIfNecessary()` will overwrite previous debt entries, and not all debt will be accounted for. This is in part because the `block.timestamp` acts as a salt rather than a true nonce.

**Recommendation:** If it is possible for `Fund.forward()` to be called with the same parameters in a single block, consider using a different source for the nonce.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Arkis |
| Report Date | N/A |
| Finders | Julio Aguilar, Ibrahim Abouzied, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/arkis/07924f14-1727-4e72-8e7a-2bc71aa735dd/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/arkis/07924f14-1727-4e72-8e7a-2bc71aa735dd/index.html

### Keywords for Search

`vulnerability`

