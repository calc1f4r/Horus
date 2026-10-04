---
# Core Classification
protocol: 1Inch
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34099
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/1inch-security-review.md
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

[M-02] FeeTaker is incompatible with fee-on-transfer tokens

### Overview


The bug report is about a problem with a contract called `FeeTaker.sol` when a certain type of token, called a fee-on-transfer token, is used as a taker asset. This can cause the contract to fail, or "revert," because it expects to have a certain amount of the token available, but only receives a smaller amount. The report recommends adding a validation step to check the balance of the token before transferring it to the recipient, in order to prevent the contract from reverting.

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** Medium

**Description**

When a fee-on-transfer token is used as a taker asset, the `FeeTaker.sol` contract receives `takingAmount - tokenFee`. This can cause the contract to revert because it assumes that the entire `takingAmount` is available on its balance.

```solidity
    function postInteraction(
        IOrderMixin.Order calldata order,
        bytes calldata /* extension */,
        bytes32 /* orderHash */,
        address /* taker */,
        uint256 /* makingAmount */,
        uint256 takingAmount,
        uint256 /* remainingMakingAmount */,
        bytes calldata extraData
    ) external {
        ---SNIP---
        unchecked {
>>          IERC20(order.takerAsset.get()).safeTransfer(receiver, takingAmount - fee);
        }
    }
```

**Recommendations**

Validate the balance before transferring to the recipient

```diff
    function postInteraction(
        IOrderMixin.Order calldata order,
        bytes calldata /* extension */,
        bytes32 /* orderHash */,
        address /* taker */,
        uint256 /* makingAmount */,
        uint256 takingAmount,
        uint256 /* remainingMakingAmount */,
        bytes calldata extraData
    ) external {
+      uint256 balance = IERC20(order.takerAsset.get()).balanceOf(address(this));
+      if (balance < takingAmount) takingAmount = balance;

         ---SNIP---
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | 1Inch |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/1inch-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

