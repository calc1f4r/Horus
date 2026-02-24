---
# Core Classification
protocol: Swappee
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55532
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Swappee-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-01] Fee-on-Transfer Tokens Can Cause Accounting Errors in Swappee Contract

### Overview


This bug report is about a vulnerability found in the `Swappee` contract, which could potentially affect the handling of Fee-on-Transfer (FOT) tokens. The issue occurs in the `swappee` function, where the contract assumes that the received amount of tokens will be the same as the transferred amount, without taking into account any transfer fees. This can cause problems when processing token transfers using `IERC20(inputToken).transferFrom()`, as the contract uses the pre-transfer amount for all subsequent calculations and approvals, instead of checking the actual received balance. This can lead to incorrect fee calculations, excessive token approvals, and potential reverts when attempting to swap the full pre-fee amount.

The affected code can be found in the `Swappee.sol` file, specifically in line 121. The impact of this bug is that users who try to swap FOT tokens may experience incorrect fee calculations, excessive token approvals, and potential reverts.

To fix this issue, the contract should properly handle FOT tokens by measuring the actual received balances before and after transfers, and using the difference as the effective amount for swaps. The team has acknowledged this bug and is working on a solution.

### Original Finding Content

## Severity

Medium Risk

## Description

The `Swappee` contract contains a vulnerability in its handling of Fee-on-Transfer (FOT) tokens. The issue manifests in the swappee function, where the contract assumes the actual received amount of tokens will equal the transferred amount, without accounting for potential transfer fees. Specifically, when processing token transfers via `IERC20(inputToken).transferFrom()`, the contract uses the pre-transfer amount (`amountsClaimedPerWallet[inputToken][msg.sender]`) for all subsequent calculations and approvals, rather than checking the actual received balance. This assumption breaks for FOT tokens, where the received amount may be less than the transferred amount due to built-in transfer fees.

## Location of Affected Code

File: [src/Swappee.sol#L121](https://github.com/smilee-finance/swappee-smart-contracts/blob/16315aa674ffce54e36fadca66da3cf6785150de/src/Swappee.sol#L121)

```solidity
function swappee(
    IBGTIncentiveDistributor.Claim[] calldata claims,
    RouterParams[] memory routerParams,
    address tokenOut
)
    public
    invariantCheck
{

    // code

    IERC20(inputToken).transferFrom(msg.sender, address(this), amount);

    unchecked {
        amountsClaimedPerWallet[inputToken][msg.sender] -= amount;
    }

    if (routerParam.swapTokenInfo.inputAmount != amount) {
        revert InvalidAmount();
    }

    IERC20(inputToken).approve(aggregator, routerParam.swapTokenInfo.inputAmount);

    // Override router params to avoid tempered inputs
    routerParam.swapTokenInfo.outputReceiver = address(this);
    routerParam.swapTokenInfo.outputToken = tokenOut;

    uint256 amountOut = _swapToken(
        routerParam.swapTokenInfo,
        routerParam.pathDefinition,
        routerParam.executor,
        routerParam.referralCode,
        tokenOut
    );

    // code
}
```

## Impact

When users attempt to swap FOT tokens, the contract will: incorrectly calculate fees based on the pre-fee amount, potentially approve more tokens than necessary to the aggregator, and may trigger reverts when attempting to swap the full pre-fee amount that isn't actually available.

## Recommendation

The contract should implement proper FOT token handling by: measuring actual received balances before and after transfers, using the delta as the effective amount for swaps.

## Team Response

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Swappee |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Swappee-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

