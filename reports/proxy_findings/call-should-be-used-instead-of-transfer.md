---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37038
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
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

`call()` Should Be Used Instead Of `transfer()`

### Overview


The report discusses a bug in the VaultkaV2GMXHandler code that uses the outdated transfer() function to transfer ETH back to the user. This can cause the transaction to fail if the receiving smart contract does not have a payable function, has a payable fallback that uses more than 2300 gas units, or is called through a proxy. It is recommended to use the call() function instead of transfer() to avoid these issues. This bug has been resolved.

### Original Finding Content

**Severity** - Medium

**Status** - Resolved

**Description**

VaultkaV2GMXHandler makes use of the transfer function at L520 to transfer ETH back to the user.
The use of the deprecated transfer() function for an address will inevitably make the transaction fail when:
The claimer smart contract does not implement a payable function.
The claimer smart contract does implement a payable fallback which uses more than 2300 gas unit.
The claimer smart contract implements a payable fallback function that needs less than 2300 gas units but is called through proxy, raising the call's gas usage above 2300.
Additionally, using more than 2300 gas might be mandatory for some multisig wallets.

**Recommendation**:

It is recommended to use call() instead of transfer()

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

