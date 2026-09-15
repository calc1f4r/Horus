---
# Core Classification
protocol: Orderly Solana Vault Contract
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43630
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/524
source_link: none
github_link: https://github.com/sherlock-audit/2024-09-orderly-network-solana-contract-judging/issues/146

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
finders_count: 4
finders:
  - g
  - krikolkk
  - 0xNirix
  - LZ\_security
---

## Vulnerability Title

M-1: Missing LayerZero Ordered Execution Option For Orderly Chain Messages

### Overview


This bug report discusses a missing feature in the protocol that can lead to a vulnerability for users. The bug was found by a group of individuals and has been acknowledged by the protocol. The root cause of the bug is a missing option for ordered execution in the withdraw implementation, which can cause message rejection and lead to inconsistent balance states for users. This can happen when multiple withdrawals are processed quickly and the messages arrive out of order at the Solana vault. This can result in funds being locked in the vault while the user's balance is reduced on the Orderly Chain. The impact of this bug can be significant and may require manual intervention by an administrator to resolve. There is currently no proof of concept or suggested mitigation for this bug. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-09-orderly-network-solana-contract-judging/issues/146 

The protocol has acknowledged this issue.

## Found by 
0xNirix, LZ\_security, g, krikolkk
### Summary

Missing ordered execution enforcement will cause message rejection vulnerability for users as unordered messages will update balances on Orderly Chain's ledger but fail on Solana vault due to message ordering mismatch.

### Root Cause

In https://github.com/sherlock-audit/2024-09-orderly-network-solana-contract/blob/main/sol-cc/contracts/SolConnector.sol#L92 the withdraw implementation only applies basic gas/value options without ordered execution option:
solidityCopybytes memory withdrawOptions = OptionsBuilder.newOptions().addExecutorLzReceiveOption(
    msgOptions[uint8(MsgCodec.MsgType.Withdraw)].gas,
    msgOptions[uint8(MsgCodec.MsgType.Withdraw)].value
);
LayerZero will not guarantee ordered message delivery in absence of this option.

### Internal pre-conditions

1. Ordered delivery is enabled on Solana vault side and Orderly chain
2. Multiple withdrawals are processed in quick succession

### External pre-conditions

_No response_

### Attack Path

1. User A and User B submit withdrawals close together
2. SolConnector sends messages with only gas/value options configured
3. LayerZero messages arrive out of order at Solana vault due to missing ordered execution option
4. Solana vault rejects out-of-order messages with InvalidInboundNonce error
5. Ledger contract has already updated balances on Orderly Chain
6. Balance state becomes inconsistent between chains

### Impact

Users suffer from state inconsistency where their balances are reduced on Orderly Chain's ledger but funds remain locked in Solana vault due to message rejection. User may effectively lose funds and to resolve this  extensive manual intervention may be required by admin.

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
| Protocol | Orderly Solana Vault Contract |
| Report Date | N/A |
| Finders | g, krikolkk, 0xNirix, LZ\_security |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-09-orderly-network-solana-contract-judging/issues/146
- **Contest**: https://app.sherlock.xyz/audits/contests/524

### Keywords for Search

`vulnerability`

