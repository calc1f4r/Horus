---
# Core Classification
protocol: Lido Csm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44094
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Lido-CSM-Security-Review.md
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
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[L-01] Fee-on-Transfer Tokens Can Cause Accounting Discrepancies in Asset Recovery Functions

### Overview

See description below for full details.

### Original Finding Content

## Submitted By

[bloqarl](https://x.com/TheBlockChainer)

## Severity

Low Risk

## Description

The `AssetRecovererLib` library, which is used by `CSAccounting`, `CSFeeDistributor`, and potentially other contracts inheriting from `AssetRecoverer`, contains a `recoverERC20()` function that is vulnerable to fee-on-transfer token accounting issues. This function assumes that the full amount specified will be transferred, which may not be the case for tokens that implement a fee-on-transfer mechanism.

## Impact

If a fee-on-transfer token is recovered using this function, the actual amount transferred will be less than the amount specified. This discrepancy could lead to:

- Incorrect accounting of recovered assets
- Potential loss of funds if the contract's balance is used for future calculations or operations
- Inconsistencies between on-chain state and off-chain records
- Misleading event emissions, as the emitted amount may not reflect the actual transferred amount

While the impact is generally low due to the restricted access of these functions (only callable by a recoverer role), it still presents a risk, especially if these contracts interact with or recover a wide range of tokens in the future.

## Proof of Concept

1. Assume a fee-on-transfer token that takes a 1% fee on each transfer.
2. The contract has a balance of 1000 of these tokens.
3. A recoverer calls recoverERC20 with an amount of 1000.
4. Only 990 tokens are actually transferred due to the fee.
5. The ERC20Recovered event is emitted with an amount of 1000, which is incorrect.

## Location of Affected Code

File: [AssetRecovererLib.sol](https://github.com/lidofinance/community-staking-module/blob/8ce9441dce1001c93d75d065f051013ad5908976/src/lib/AssetRecovererLib.sol)

```solidity
function recoverERC20(address token, uint256 amount) external {
    IERC20(token).safeTransfer(msg.sender, amount);
    emit IAssetRecovererLib.ERC20Recovered(token, msg.sender, amount);
}
```

## Recommendation

To mitigate this issue, implement a balance check before and after the transfer to determine the actual amount transferred:

```solidity
function recoverERC20(address token, uint256 amount) external {
    uint256 balanceBefore = IERC20(token).balanceOf(address(this));
    IERC20(token).safeTransfer(msg.sender, amount);
    uint256 balanceAfter = IERC20(token).balanceOf(address(this));
    uint256 actualAmountTransferred = balanceBefore - balanceAfter;
    emit IAssetRecovererLib.ERC20Recovered(token, msg.sender, actualAmountTransferred);
}
```

## Team Response

Acknowledged, the amount in the event properly reflects the amount of tokens transferred from the contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Lido Csm |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Lido-CSM-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

