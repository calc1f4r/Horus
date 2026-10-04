---
# Core Classification
protocol: Ionprotocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36433
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[C-01] Using underlying as the input `amount` instead of normalized balances

### Overview


The report states that there is a bug in the `IonPool` contract which inherits from `RewardToken`. This bug can have a high impact and is likely to occur. The bug occurs during token transfers, where the contract accepts the underlying amount as input and converts it to a normalized amount using a factor. However, this conversion does not take into account the current supply factor, which can result in incorrect amounts being transferred. Additionally, since `RewardToken` is now a non-rebasing token, the `balanceOf` function will return the normalized balances instead of the underlying balances, which can cause issues for users and third-party integrators. To fix this bug, it is recommended to directly transfer the normalized balances instead of converting them from the underlying amount.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** High

**Description**

`IonPool` inherits `RewardToken`, an ERC20-based non-rebasing token, to enable the transferability of supply shares. However, during token transfers, it accepts the underlying amount as the `amount` input. It then converts this amount to `amountNormalized` using the `supplyFactor`, and updates the `_normalizedBalances` of `from` and `to` based on this converted `amountNormalized`.

```solidity
    function _transfer(address from, address to, uint256 amount) private {
        if (from == address(0)) revert ERC20InvalidSender(address(0));
        if (to == address(0)) revert ERC20InvalidReceiver(address(0));
        if (from == to) revert SelfTransfer(from);

        RewardTokenStorage storage $ = _getRewardTokenStorage();

        uint256 _supplyFactor = $.supplyFactor;
>>>     uint256 amountNormalized = amount.rayDivDown(_supplyFactor);

        uint256 oldSenderBalance = $._normalizedBalances[from];
        if (oldSenderBalance < amountNormalized) {
            revert ERC20InsufficientBalance(from, oldSenderBalance, amountNormalized);
        }
        // Underflow impossible
        unchecked {
>>>         $._normalizedBalances[from] = oldSenderBalance - amountNormalized;
        }
>>>     $._normalizedBalances[to] += amountNormalized;

        emit Transfer(from, to, amountNormalized);
    }
```

There are several issues with this implementation :

- When converting from the underlying amount to `amountNormalized` using `supplyFactor`, it doesn't trigger accrue interest first. This could lead to issues since the `supplyFactor` might not be up to date with the current supply factor after accruing interest, resulting in an incorrect amount of `amountNormalized` being transferred.

- `RewardingToken` is now a non-rebasing token. ERC20-based `balanceOf` function now will return the user's `_normalizedBalances` instead of their underlying balances. If users or third-party integrators use the `balanceOf` result for the amount of the transfer, it will result in transferring the wrong amount of tokens, potentially breaking all interactions with this ERC20-based non-rebasing token.

**Recommendations**

Considering that this is now a non-rebasing token, `_transfer` should accept the normalized amount as the `amount` input and directly transfer the `_normalizedBalances` of users.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ionprotocol |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

