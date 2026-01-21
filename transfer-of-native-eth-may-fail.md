---
# Core Classification
protocol: Zap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35727
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-26-zap.md
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

Transfer of native ETH may fail.

### Overview


A bug has been found in the `RetrieveAsset.sol` contract, where the `retrieveNative()` function uses the `transfer()` function to transfer ETH. However, `transfer()` only provides 2300 gas for its operation, which can cause the transfer to fail in certain cases. This means that users may not be able to receive funds from the contract. To fix this, it is recommended to use the low-level `.call()` function instead of `transfer()` and check the returned value to ensure that the transfer of ether has been completed correctly. This bug has been resolved.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

The `retrieveNative()` function in the `RetrieveAsset.sol` contract uses the native `transfer()` function to transfer ETH. `transfer()` only provides 2300 gas for its operation. This means the following cases can cause the transfer to fail: 

- The contract's callback spends more than 2300 gas (which is only enough to emit something) 

- The contract is called through a proxy which itself uses up the 2300 gas 

- Complex operations or external calls

If a user falls into one of the above categories, they'll be unable to receive funds from the contract.

**Recommendation**: 

Consider using the low-level .call() instead of transfer() and check the returned value to ensure that the transfer of ether has been correctly completed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-26-zap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

