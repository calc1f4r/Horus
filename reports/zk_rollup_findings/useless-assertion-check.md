---
# Core Classification
protocol: zkSync Bootloader Audit Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10365
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/zksync-bootloader-audit-report/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Useless Assertion Check

### Overview


This bug report is about an issue with the `assertEq` function in the bootloader. This function compares two values and throws an error if they are not equal. There are two issues with this implementation: the function compares the `value1` parameter to itself which makes the comparison redundant, and the function header includes the `value1` parameter twice which causes a compile-time error when using a Solidity compiler.

To resolve the issue, the comparison should be corrected by checking two distinct variables. Additionally, the custom zkEVM compiler should throw an error when declaring two variables with the same name in the same scope. The bug was resolved in pull request #133 at commit 6e3c054a9c8cf6da52b5721a0dd1ef48bec7d6c1.

### Original Finding Content

The [`assertEq` function](https://github.com/matter-labs/system-contracts/blob/4ad1f26ae205d5a973216d141833e0ac37d72ec8/bootloader/bootloader.yul#L1644-L1653) in the bootloader compares two values. If they are not equal, it throws an error. There are two issues with this implementation:


* The function compares the value of the `value1` parameter to itself, which means the comparison will always be true and the function serves no purpose.
* The function header includes the `value1` parameter twice, which causes a compile-time error when using a Solidity compiler such as `solc`.


Consider correcting the comparison by checking two distinct variables. Additionally, ensure that the custom zkEVM compiler throws an error when declaring two variables with the same name in the same scope.


***Update:** Resolved in [pull request #133](https://github.com/matter-labs/system-contracts/pull/133/) at commit [6e3c054](https://github.com/matter-labs/system-contracts/pull/133/commits/6e3c054a9c8cf6da52b5721a0dd1ef48bec7d6c1).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | zkSync Bootloader Audit Report |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/zksync-bootloader-audit-report/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

