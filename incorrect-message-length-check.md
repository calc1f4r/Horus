---
# Core Classification
protocol: USDV
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47771
audit_firm: OtterSec
contest_link: https://layerzero.network/
source_link: https://layerzero.network/
github_link: https://github.com/LayerZero-Labs/usdv

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - James Wang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Incorrect Message Length Check

### Overview


The bug report discusses an issue with the MsgCodec component, which is responsible for data serialization and deserialization in a messaging system. Specifically, the decodeSendAndCallMsg function is incorrectly checking the length of deserialized data, causing the API to become unusable. The bug is located in the MsgCodec.sol file and can be fixed by changing the condition in the code to _message.length < 53. This bug has been resolved in the latest patch.

### Original Finding Content

## MsgCodec Vulnerability Report

## Overview
MsgCodec is responsible for data serialization and deserialization before pushing messages to LayerZero. 

## Issue
The `decodeSendAndCallMsg` function attempts to perform a sanity check on the length of deserialized data but performs the opposite of the required comparison. Since all messages for `SendAndCallMsg` will have at least 53 bytes, this incorrect check renders the entire API unusable.

### Affected Code
The relevant code can be found in the following file:
```
usdv2/packages/usdv/evm/contracts/contracts/messaging/libs/MsgCodec.sol
```

### Vulnerable Function
```solidity
function decodeSendAndCallMsg(bytes calldata _message) internal pure returns (SendAndCallMsg memory) {
    if (_message.length >= 53) revert InvalidSize();
    [...]
}
```

## Remediation
Assert against the correct condition: `_message.length < 53`.

## Patch
This issue has been resolved in commit `e216fb0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | USDV |
| Report Date | N/A |
| Finders | James Wang, Robert Chen, OtterSec |

### Source Links

- **Source**: https://layerzero.network/
- **GitHub**: https://github.com/LayerZero-Labs/usdv
- **Contest**: https://layerzero.network/

### Keywords for Search

`vulnerability`

