---
# Core Classification
protocol: Flayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41781
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/468
source_link: none
github_link: https://github.com/sherlock-audit/2024-08-flayer-judging/issues/509

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
  - zzykxx
---

## Vulnerability Title

M-18: If the royalties receiver it's a smart contract it might be impossible to collect L2 royalties

### Overview


This bug report discusses an issue (M-18) found by a user named zzykxx. The issue involves the inability to collect L2 royalties if the receiver is a smart contract. The root cause of this problem is the [InfernalRiftAbove::claimRoyalties()](https://github.com/sherlock-audit/2024-08-flayer/blob/main/moongate/src/InfernalRiftAbove.sol#L251) function, which can only be called by the receiver of the royalties. This is problematic because if the receiver is a smart contract, it may not have a way to call this function and therefore cannot claim the royalties. This bug could potentially lead to the royalties being stuck and unable to be claimed. To mitigate this issue, it is suggested to allow anyone to claim the royalties for the receiver address when it is a smart contract.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-08-flayer-judging/issues/509 

## Found by 
zzykxx
### Summary

_No response_

### Root Cause

The function [InfernalRiftAbove::claimRoyalties()](https://github.com/sherlock-audit/2024-08-flayer/blob/main/moongate/src/InfernalRiftAbove.sol#L251) can only be called by the receiver of the royalties:

```solidity
(address receiver,) = IERC2981(_collectionAddress).royaltyInfo(0, 0);

// Check that the receiver of royalties is making this call
if (receiver != msg.sender) revert CallerIsNotRoyaltiesReceiver(msg.sender, receiver);
```

This is fine for EOAs but is problematic if `receiver` is a contract that doesn't have a way to call [InfernalRiftAbove::claimRoyalties()](https://github.com/sherlock-audit/2024-08-flayer/blob/main/moongate/src/InfernalRiftAbove.sol#L251), as this would result in the `receiver` not being able to claim the royalties collected by NFTs bridged to L2.

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

_No response_

### Impact

If the royalties `receiver` is a smart contract that doesn't have a way to call [InfernalRiftAbove::claimRoyalties()](https://github.com/sherlock-audit/2024-08-flayer/blob/main/moongate/src/InfernalRiftAbove.sol#L251) it's impossible to claim the royalties, which will be stuck.

### PoC

_No response_

### Mitigation

Allow royalties to be claimed to the `receiver` address by anybody when `receiver` is a smart contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Flayer |
| Report Date | N/A |
| Finders | zzykxx |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-08-flayer-judging/issues/509
- **Contest**: https://app.sherlock.xyz/audits/contests/468

### Keywords for Search

`vulnerability`

