---
# Core Classification
protocol: Lumin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27239
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Lumin.md
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
  - Pashov
---

## Vulnerability Title

[M-05] Protocol does not support fee-on-transfer and rebasing tokens

### Overview


This bug report is about an issue with the `_depositWithdraw` method in the `AssetManager` contract, which does not account for tokens that have a fee-on-transfer or a rebasing mechanism. This can lead to tokens being stuck in the protocol, which has a high impact. The likelihood of this occurring is low, as only a small portion of tokens have such mechanisms. 

The report recommends either explicitly documenting that the protocol does not support tokens with a fee-on-transfer or rebasing mechanism, or implementing a complex solution to update the cached reserves when the value of the token goes down, and to transfer the excess tokens out of the protocol when the value of the token goes up.

### Original Finding Content

**Severity**

**Impact:**
High, as this can leave tokens stuck in the protocol

**Likelihood:**
Low, as a small portion of the commonly used tokens have such mechanisms

**Description**

The `_depositWithdraw` method in `AssetManager` has the following implementation:

```solidity
function _depositWithdraw(address assetAddress, bool deposit, address sender, uint256 amount) private {
    if (deposit) {
        IERC20(assetAddress).safeTransferFrom(sender, address(this), amount);
    } else {
        IERC20(assetAddress).safeTransfer(sender, amount);
    }
}
```

Also before/after it is called we have code like this:

```solidity
assetDeposit.depositAmount -= amount;
userDeposit.depositAmount -= amount;
```

and this

```solidity
assetDeposit.depositAmount += amount;
userDeposit.depositAmount += amount;
```

This code does not account for tokens that have a fee-on-transfer or a rebasing (token balance going up/down without transfers) mechanisms. By caching (or removing) the `amount` given to the `transfer` or `transferFrom` methods of the ERC20 token, this implies that this will be the actual received/sent out amount by the protocol and that it will be static, but that is not guaranteed to be the case. If fee-on-transfer tokens are used, on deposit action the actual received amount will be less, so withdrawing the same balance won't be possible. For rebasing tokens it is also possible that the contract's balance decreases over time, which will lead to the same problem as with the fee-on-transfer tokens, and if the balance increases then the reward will be stuck in the `AssetManager` contract.

**Recommendations**

You can either explicitly document that you do not support tokens with a fee-on-transfer or rebasing mechanism or you can do the following:

For fee-on-transfer tokens, check the balance before and after the transfer and validate it is the same as the `amount` argument provided.
For rebasing tokens, when they go down in value, you should have a method to update the cached reserves accordingly, based on the balance held. This is a complex solution.
For rebasing tokens, when they go up in value, you should add a method to actually transfer the excess tokens out of the protocol (possibly directly to users).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Lumin |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Lumin.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

