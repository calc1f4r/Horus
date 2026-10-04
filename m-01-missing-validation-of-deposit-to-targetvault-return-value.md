---
# Core Classification
protocol: Gluon-security-review_2025-09-20
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62713
audit_firm: Kann
contest_link: none
source_link: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/Gluon-security-review_2025-09-20.md
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
  - Kann
---

## Vulnerability Title

[M-01] Missing Validation of deposit to targetvault Return Value

### Overview


This bug report is about the _deployFunds function in a smart contract. The function is supposed to forward funds to a specific targetVault, but there is a problem with the assumption that the targetVault will always give the strategy a non-zero amount of vault shares. This assumption can fail in certain cases, such as when a newly launched vault has been pre-funded or other edge cases. This can result in 0 shares being minted for the depositor, effectively locking the strategy's assets in the vault. The recommendation is to always validate that shares were actually received before proceeding. The team has responded that the issue has been fixed.

### Original Finding Content


## Severity

Medium

## Description

The _deployFunds function forwards funds to targetVault by calling:

targetVault.deposit(deployAmount, address(this));

The _deployFunds function assumes targetVault.deposit(...) will always give the strategy a non-zero amount of vault shares. In normal, well-behaved vaults that’s true, but there are cases where this assumption can fail. For example, if a freshly launched/integrated vault has been pre-funded (someone transfers assets directly to the vault contract without calling transfer the vault’s share-calculation can be skewed and a subsequent deposit call can result in 0 shares minted for the depositor. Other edge cases could also lead to the same outcome, leaving the strategy’s assets effectively locked in the vault with no credited shares.

Recommendation
Always validate that shares were actually received:

```solidity
uint256 sharesReceived = targetVault.deposit(deployAmount, address(this));
require(sharesReceived > 0, "Deposit did not mint shares");
```

## Team Response

Fixed.




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Kann |
| Protocol | Gluon-security-review_2025-09-20 |
| Report Date | N/A |
| Finders | Kann |

### Source Links

- **Source**: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/Gluon-security-review_2025-09-20.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

