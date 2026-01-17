---
# Core Classification
protocol: Archi Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60941
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
source_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
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
finders_count: 4
finders:
  - Mustafa Hasan
  - Zeeshan Meghji
  - Ibrahim Abouzied
  - Hytham Farah
---

## Vulnerability Title

(Re-Audit) Blocked Credit Managers Cannot Be Unblocked

### Overview


This bug report discusses an issue with the functions `forbidCreditManagerToBorrow()` and `forbidCreditManagerToRepay()` in the file `AbstractVault.sol`. These functions allow the contract owner to block certain credit managers from borrowing or repaying. However, once a credit manager is blocked, their `Sharelocker` cannot be used for the respective action. This makes it impossible for them to repay any open positions they may have. The recommendation is to update the functions so that the owner can block and unblock credit managers as needed.

### Original Finding Content

**Update**
The functions have been modified so they enable and disable borrowing and repayment from specific credit managers.

**File(s) affected:**`AbstractVault.sol`

**Description:** The functions `forbidCreditManagerToBorrow()` and `forbidCreditManagerToRepay()` allow the contract owner to block certain credit managers to borrow or repay. However, the effect of such functions is irreversible and so once a credit manager is "forbidden" their `Sharelocker` will no longer be usable for the respective action. For example, when `forbidCreditManagerToRepay()` is called with the address of a credit manager that is handling a bunch of open positions, repayment for these open positions will be ultimately impossible.

**Recommendation:** Update the logic of the `forbidCreditManagerToBorrow()` and `forbidCreditManagerToRepay()` functions so that boolean is passed and set for the respective mappings, or the setting is toggled per call. This would allow the owner to block and unblock credit managers.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Archi Finance |
| Report Date | N/A |
| Finders | Mustafa Hasan, Zeeshan Meghji, Ibrahim Abouzied, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html

### Keywords for Search

`vulnerability`

