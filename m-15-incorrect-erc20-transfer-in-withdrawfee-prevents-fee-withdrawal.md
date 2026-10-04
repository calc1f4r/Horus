---
# Core Classification
protocol: Hyperhyper_2025-03-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57758
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperhyper-security-review_2025-03-30.md
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

[M-15] Incorrect `ERC20` transfer in `withdrawFee` prevents fee withdrawal

### Overview


This bug report discusses an issue with the `AdminOperationalTreasury.withdrawFee()` function. The function is using `safeTransferFrom()` instead of `safeTransfer()` when withdrawing protocol fees. This is incorrect because it requires the spender to have an allowance from the owner, which the contract does not have. The recommendation is to replace `safeTransferFrom()` with `safeTransfer()` since the contract is transferring tokens it owns. This will prevent the fee transfer from failing due to insufficient allowance. The severity and likelihood of this bug are both considered medium.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `AdminOperationalTreasury.withdrawFee()` function uses `safeTransferFrom()` instead of `safeTransfer()` when withdrawing protocol fees. This is incorrect because:

1. `safeTransferFrom()` requires the spender to have an allowance from the owner.
2. The contract is trying to transfer from itself (`address(this)`) to the recipient.
3. The contract has not approved itself to spend its own tokens.

```solidity
function withdrawFee(address token_, address recipient_) external {
    OperationalTreasuryStorage.Layout storage strg = OperationalTreasuryStorage.layout();

    if (msg.sender != strg.setUp.base.feesReceiver) revert("FeesReceiverOnly");
    uint256 amount = strg.ledger.collectedFees[token_];
    strg.ledger.collectedFees[token_] = 0;

@>  IERC20Metadata(token_).safeTransferFrom(address(this), recipient_, amount);
    emit ProtocolFeeWithdrawn(token_, recipient_, amount);
}
```

For normal `ERC20`, `transferFrom` always checks the allowance of the spender, even when `from` is the same as `msg.sender`. As a result, the fee transfer will fail due to insufficient allowance.

## Recommendation

Replace `safeTransferFrom()` with `safeTransfer()`, since the contract is transferring tokens it owns.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperhyper_2025-03-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperhyper-security-review_2025-03-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

