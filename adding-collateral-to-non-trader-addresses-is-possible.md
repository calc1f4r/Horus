---
# Core Classification
protocol: Native v2 (Security Review)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58961
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/native-v-2-security-review/7c9b3fe3-dbb4-4527-ad0b-f50aa3e15d8c/index.html
source_link: https://certificate.quantstamp.com/full/native-v-2-security-review/7c9b3fe3-dbb4-4527-ad0b-f50aa3e15d8c/index.html
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
  - Valerian Callens
---

## Vulnerability Title

Adding Collateral to Non-Trader Addresses Is Possible

### Overview


A recent update to the `CreditVault.sol` contract has caused a bug where collateral can only be added to specific addresses that are whitelisted. This means that if someone tries to add collateral for an address that is not whitelisted, the tokens may become stuck in the contract. The recommendation is to check that the receiver address is a whitelisted trader before allowing collateral to be added.

### Original Finding Content

**Update**
Collateral can only be added to whitelisted trader address as of commit `5a3b5b2`.

**File(s) affected:**`src/CreditVault.sol`

**Description:** In the `CreditVault.sol` contract, anyone can call the function `addCollateral()` to add collateral for another address. However, there is no check to make sure that the receiver address is a whitelisted trader in the system. If this is not the case, tokens sent as collateral may remain locked in the contract.

**Recommendation:** Consider making sure that the receiver address is a whitelisted `trader`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Native v2 (Security Review) |
| Report Date | N/A |
| Finders | Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/native-v-2-security-review/7c9b3fe3-dbb4-4527-ad0b-f50aa3e15d8c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/native-v-2-security-review/7c9b3fe3-dbb4-4527-ad0b-f50aa3e15d8c/index.html

### Keywords for Search

`vulnerability`

