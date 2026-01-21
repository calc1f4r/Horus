---
# Core Classification
protocol: Woosh Deposit Vault
chain: everychain
category: uncategorized
vulnerability_type: call_vs_transfer

# Attack Vector Details
attack_type: call_vs_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21962
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh Deposit Vault.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.68
financial_impact: medium

# Scoring
quality_score: 3.4248537686513085
rarity_score: 1

# Context Tags
tags:
  - call_vs_transfer
  - documentation

protocol_categories:
  - services

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Hans
  - 0kage
---

## Vulnerability Title

Use call instead of transfer

### Overview


This bug report is about an issue that arises when using the transfer() function for native ETH withdrawal in two withdraw functions. This function forwards a fixed amount of 2300 gas, which may not be enough for some smart contracts. This could lead to the transaction failing when the claimer smart contract does not implement a payable function, the claimer smart contract does implement a payable fallback which uses more than 2300 gas units, or the claimer smart contract implements a payable fallback function that needs less than 2300 gas units but is called through proxy, raising the call's gas usage above 2300. Additionally, using higher than 2300 gas might be mandatory for some multisig wallets. The recommended mitigation for this issue is to use call() instead of transfer(). This has been verified in commit 7726ae7 on the HyperGood/woosh-contracts Github repository.

### Original Finding Content

**Severity:** Medium

**Description:** In both of the withdraw functions, `transfer()` is used for native ETH withdrawal.
The transfer() and send() functions forward a fixed amount of 2300 gas. Historically, it has often been recommended to use these functions for value transfers to guard against reentrancy attacks. However, the gas cost of EVM instructions may change significantly during hard forks which may break already deployed contract systems that make fixed assumptions about gas costs. For example. EIP 1884 broke several existing smart contracts due to a cost increase of the SLOAD instruction.

**Impact:** The use of the deprecated transfer() function for an address will inevitably make the transaction fail when:
- The claimer smart contract does not implement a payable function.
- The claimer smart contract does implement a payable fallback which uses more than 2300 gas unit.
- The claimer smart contract implements a payable fallback function that needs less than 2300 gas units but is called through proxy, raising the call's gas usage above 2300.

Additionally, using higher than 2300 gas might be mandatory for some multisig wallets.

**Recommended Mitigation:** Use call() instead of transfer().

**Protocol:**
Agree, transfer was causing issues with smart contract wallets.

**Cyfrin:** Verified in commit [7726ae7](https://github.com/HyperGood/woosh-contracts/commit/7726ae72118cfdf91ceb9129e36662f69f4d42de).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3.4248537686513085/5 |
| Rarity Score | 1/5 |
| Audit Firm | Cyfrin |
| Protocol | Woosh Deposit Vault |
| Report Date | N/A |
| Finders | Hans, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh Deposit Vault.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`call vs transfer, Documentation`

