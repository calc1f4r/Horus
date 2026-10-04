---
# Core Classification
protocol: Nexus_2024-11-29
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44990
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-04] LayerZero fee refunds misdirected to deposit contracts

### Overview


The report discusses a bug in the LayerZero fee system where the fee intended to cover cross-chain messaging costs for deposits and withdrawals is not refunded to the sender. Instead, the fee is directed to the deposit contract, causing an unfair burden on the sender. The report recommends passing the user's address as the refund address to ensure proper reimbursement.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The LayerZero fee, which is intended to cover the cross-chain messaging cost for deposits and withdrawals, is not refunded to the sender who initiates the transaction through the Ethereum mainnet or Berachain.

Instead, this fee is directed to the deposit contract itself (`DepositETH`, `DepositUSD`, `DepositETHBera`, and `DepositUSDBera`), despite the fact that the sender is the one incurring the cost of the cross-chain messaging.

This can result in an unfair burden on the sender, who bears the full cost of initiating the cross-chain transaction without receiving any compensation for the excess fee.

```solidity
@> function sendMessage(bytes memory _data, uint32 _destId, uint256 _lzFee) external override payable onlyDeposit{
    if(!destIdAvailable(_destId)) revert NotWhitelisted(_destId);
    MessagingReceipt memory receipt = _lzSend(
        _destId,
        _data,
        optionsDestId[_destId],
        MessagingFee(_lzFee, 0),
@>        payable(msg.sender)
    );
    emit MessageSent(_destId,_data,receipt);
}
```

Using the `Messaging` contract as an example, the `sendMessage()` can only be called by `DepositETH` or `DepositUSD`. Consequently, the `msg.sender` passed as the refund address is either the `DepositETH` or `DepositUSD` contract, rather than the user who originally initiated the deposit.

To note that the `MessageBera.sendMessage()` that is used in `DepositETHBera` and `DepositUSDBera` contracts shares the same issues.

## Recommendations

Consider passing the user address that initiated the action as the refund address to ensure the fee is properly refunded to the user.

```diff
- function sendMessage(bytes memory _data, uint32 _destId, uint256 _lzFee) external override payable onlyDeposit{
+ function sendMessage(bytes memory _data, uint32 _destId, uint256 _lzFee, address refundAddress) external override payable onlyDeposit{
    if(!destIdAvailable(_destId)) revert NotWhitelisted(_destId);
    MessagingReceipt memory receipt = _lzSend(
        _destId,
        _data,
        optionsDestId[_destId],
        MessagingFee(_lzFee, 0),
-        payable(msg.sender)
+       payable(refundAddress)
    );
    emit MessageSent(_destId,_data,receipt);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nexus_2024-11-29 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

