---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6452
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest
source_link: https://code4rena.com/reports/2023-01-biconomy
github_link: https://github.com/code-423n4/2023-01-biconomy-findings/issues/288

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - gz627  zapaz
  - Atarpara
---

## Vulnerability Title

[M-06] Doesn't Follow ERC1271 Standard

### Overview


This bug report is about a vulnerability in the smart contract wallet code of the code-423n4/2023-01-biconomy repository. The code does not follow the EIP-1271 standard which requires the `ERC1271_MAGIC_VALUE` to be `0x1626ba7e` and the function name to be `isValidSignature(bytes32,bytes)` instead of `isValidSignature(bytes,bytes)`. This causes the signature verifier contract to go to the fallback function and return an unexpected value, which in turn causes the `execTransaction` function to always revert. 

The proof of concept for this vulnerability can be found in the following lines of code:

https://github.com/code-423n4/2023-01-biconomy/blob/main/scw-contracts/contracts/smart-contract-wallet/interfaces/ISignatureValidator.sol#L6
https://github.com/code-423n4/2023-01-biconomy/blob/main/scw-contracts/contracts/smart-contract-wallet/interfaces/ISignatureValidator.sol#L19
https://github.com/code-423n4/2023-01-biconomy/blob/main/scw-contracts/contracts/smart-contract-wallet/SmartAccount.sol#L342

The recommended mitigation step for this vulnerability is to follow the EIP-1271 standard.

### Original Finding Content


As Per [EIP-1271](https://eips.ethereum.org/EIPS/eip-1271) standard `ERC1271_MAGIC_VAULE` should be `0x1626ba7e` instead of `0x20c13b0b` and function name should be `isValidSignature(bytes32,bytes)` instead of  `isValidSignature(bytes,bytes)`. Due to this, signature verifier contract go fallback function and return unexpected value and never return `ERC1271_MAGIC_VALUE` and always revert `execTransaction` function.

### Proof of Concept

[contracts/smart-contract-wallet/interfaces/ISignatureValidator.sol#L6](https://github.com/code-423n4/2023-01-biconomy/blob/main/scw-contracts/contracts/smart-contract-wallet/interfaces/ISignatureValidator.sol#L6)<br>
[contracts/smart-contract-wallet/interfaces/ISignatureValidator.sol#L19](https://github.com/code-423n4/2023-01-biconomy/blob/main/scw-contracts/contracts/smart-contract-wallet/interfaces/ISignatureValidator.sol#L19)<br>
[contracts/smart-contract-wallet/SmartAccount.sol#L342](https://github.com/code-423n4/2023-01-biconomy/blob/main/scw-contracts/contracts/smart-contract-wallet/SmartAccount.sol#L342)

### Recommended Mitigation Steps

Follow [EIP-1271](https://eips.ethereum.org/EIPS/eip-1271) standard.

**[livingrockrises (Biconomy) confirmed](https://github.com/code-423n4/2023-01-biconomy-findings/issues/288#issuecomment-1404396848)**

**[gzeon (judge) commented](https://github.com/code-423n4/2023-01-biconomy-findings/issues/288#issuecomment-1425683830):**
 > Selected as best as this issue also mentions the wrong function signature.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | gz627  zapaz, Atarpara |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-biconomy
- **GitHub**: https://github.com/code-423n4/2023-01-biconomy-findings/issues/288
- **Contest**: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest

### Keywords for Search

`vulnerability`

