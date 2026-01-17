---
# Core Classification
protocol: MetaMask Delegation Framework
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43640
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2024/10/metamask-delegation-framework/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

Improper Calldata Length Check in ERC721TransferEnforcer and OwnershipTransferEnforcer Contracts ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



[Fixed](https://github.com/MetaMask/delegatable-paymaster/commit/6cce0278f3dfccf35c4c82efee563a5c0dcec639).
 

#### Description


In both the `beforeHook` function of the `ERC721TransferEnforcer` contract and the `_validateAndEnforce` function of the `OwnershipTransferEnforcer` contract, the length of the `calldata` is improperly validated. The length check is performed after an operation is executed on the `calldata`, which poses a security risk.
In the `beforeHook` function of the `ERC721TransferEnforcer` contract, the following line extracts the first 4 bytes of the `calldata` to determine the function selector:
`bytes4 selector_ = bytes4(callData_[0:4]);`
However, this operation is performed before validating that the `calldata` is at least 4 bytes long. If the `calldata` is less than 4 bytes, the contract will attempt to access out\-of\-bounds data, causing the transaction to revert unexpectedly.
A similar issue exists in the `_validateAndEnforce` function of the `OwnershipTransferEnforcer` contract. In both cases, the `calldata` length should be checked before any operations are performed on the `calldata` to avoid unexpected reverts and ensure proper handling of `calldata` input.


#### Examples


**src/enforcers/ERC721TransferEnforcer.sol:L36\-L42**



```
bytes4 selector_ = bytes4(callData_[0:4]);

// Decode the remaining callData into NFT transfer parameters
// The calldata should be at least 100 bytes (4 bytes for the selector + 96 bytes for the parameters)
if (callData_.length < 100) {
    revert("ERC721TransferEnforcer:invalid-calldata-length");
}

```
**src/enforcers/OwnershipTransferEnforcer.sol:L75\-L78**



```
bytes4 selector = bytes4(callData_[0:4]);
require(selector == IERC173.transferOwnership.selector, "OwnershipTransferEnforcer:invalid-method");

require(callData_.length == 36, "OwnershipTransferEnforcer:invalid-execution-length");

```
#### Recommendation


Move the length check of `calldata` to the beginning of the function to ensure the `calldata` has sufficient length before any slicing or access operations are performed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | MetaMask Delegation Framework |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2024/10/metamask-delegation-framework/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

