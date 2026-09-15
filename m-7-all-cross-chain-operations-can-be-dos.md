---
# Core Classification
protocol: LEND
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58404
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/908
source_link: none
github_link: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/745

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
finders_count: 10
finders:
  - newspacexyz
  - molaratai
  - moray5554
  - Kvar
  - yoooo
---

## Vulnerability Title

M-7: All Cross-Chain operations can be DOS

### Overview


This bug report is about a vulnerability found in the CrossChainRouter contract of the LayerZero protocol. The protocol team transfers ETH to the router to be used as gas for cross-chain messaging. However, the design allows a malicious user to drain all the ETH on the router by making unnecessary cross-chain operations, potentially causing the protocol to fail and resulting in the loss of assets for users. This bug could also lead to delays in liquidation and repayment, causing users to unfairly lose their assets. There is currently no response or mitigation for this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/745 

## Found by 
Hueber, Kirkeelee, Kvar, Phaethon, molaratai, moray5554, newspacexyz, xiaoming90, yoooo, zxriptor

### Summary

-

### Root Cause

-

### Internal Pre-conditions

-

### External Pre-conditions

-

### Attack Path

The protocol team will transfer ETH to the router to be used as gas for LayerZero's cross-chain messaging. All cross-chain operations (e.g., `borrowCrossChain`, `liquidateCrossChain`, `repayCrossChainBorrow`) in the `CrossCahinRouter` contract require ETH residing in the contract in order for the LayerZero's `_lzSend` cross-chain messaging to work because any cross-chain message send requires a fee.

However, the problem with this design is that a malicious user can drain all the ETH residing on the `CrossChainRouter` contract intended for LayerZero fee by making many unnecessary cross-chain operations, likely with a very small amount (e.g., opening a dust cross-chain borrow position or dust repayment)

When no ETH is residing in the router, all Cross-Chain operations on the router will be fail/revert and be DOSed.

https://github.com/sherlock-audit/2025-05-lend-audit-contest/blob/main/Lend-V2/src/LayerZero/CrossChainRouter.sol#L804

```solidity
File: CrossChainRouter.sol
801:     /**
802:      * @notice Sends LayerZero message
803:      */
804:     function _send(
805:         uint32 _dstEid,
806:         uint256 _amount,
807:         uint256 _borrowIndex,
808:         uint256 _collateral,
809:         address _sender,
810:         address _destlToken,
811:         address _liquidator,
812:         address _srcToken,
813:         ContractType ctype
814:     ) internal {
815:         bytes memory payload =
816:             abi.encode(_amount, _borrowIndex, _collateral, _sender, _destlToken, _liquidator, _srcToken, ctype);
817: 
818:         bytes memory options = OptionsBuilder.newOptions().addExecutorLzReceiveOption(1_000_000, 0);
819: 
820:         _lzSend(_dstEid, payload, options, MessagingFee(address(this).balance, 0), payable(address(this)));
821:     }
```

### Impact

Loss of assets and core feature broken. It can lead to the loss of assets because if liquidation can be blocked or delayed, it will result in a loss for the protocol. If repayment cannot be performed or delayed by malicious user, users cannot repay or cannoty repay their debt in a timely manner, causing their debt to accumulate and their account eventually get liquidated unfairly.

### PoC

_No response_

### Mitigation

_No response_

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | LEND |
| Report Date | N/A |
| Finders | newspacexyz, molaratai, moray5554, Kvar, yoooo, Phaethon, xiaoming90, Hueber, zxriptor, Kirkeelee |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/745
- **Contest**: https://app.sherlock.xyz/audits/contests/908

### Keywords for Search

`vulnerability`

