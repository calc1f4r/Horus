---
# Core Classification
protocol: Gluex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44370
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/GlueX-Security-Review.md
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

[L-02] Missing Deadline Check in the `GluexRouter.swap()` Function

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

The `swap()` function in the `GluexRouter.sol` contract executes a route, delegating all calls encoded interactions to the `executor`.

However, this function does not include a **deadline check** to ensure that the swap is executed within a specific time frame.

This omission could expose the contract to certain risks, such as stale transactions that are executed later than intended.

Although the slippage check helps mitigate the impact of price changes, swaps executed without a time limit could still be exposed to high market volatility over a longer period. If market conditions change drastically, the user’s transaction could be negatively impacted.

## Impact

Users who send more ETH than required will not receive a refund for the excess amount.

## Location of Affected Code

File: [contracts/GluexRouter.sol#L88](https://github.com/gluexprotocol/gluex_router/blob/1df4eaef9c3063a3171961e1f8bba3eb83c6b7e1/contracts/GluexRouter.sol#L88)

## Recommendation

We recommend adding a **deadline parameter** to the `swap()` function to ensure that transactions are executed within a specified time frame. This will give users additional protection against market volatility and stale transactions.

```diff
function swap(
        IExecutor executor,
        RouteDescription calldata desc,
        Interaction[] calldata interactions
+       uint256 deadline
)
    external
    payable
    returns (
        uint256 finalOutputAmount
) {
+   if (deadline < block.timestamp) revert DeadlineExpired();
}
```

## Team Response

Fixed.

## [I-01] Nothing Happens in the `uniTransfer()` Function When the Amount Parameter Is Equal to Zero

## Severity

Info

## Description

In the uniTransfer function, if the amount parameter is equal to zero, nothing happens and the transaction is executed successfully.

## Location of Affected Code

File: [contracts/GluexRouter.sol#L191](https://github.com/gluexprotocol/gluex_router/blob/1df4eaef9c3063a3171961e1f8bba3eb83c6b7e1/contracts/GluexRouter.sol#L191)

```solidity
function uniTransfer(
    IERC20 token,
    address payable to,
    uint256 amount
) internal {
@>  if (amount > 0) {
        if (address(token) == _nativeToken) {
            if (address(this).balance < amount)
                revert InsufficientBalance();

            // solhint-disable-next-line avoid-low-level-calls
            (bool success, ) = to.call{
                value: amount,
                gas: _RAW_CALL_GAS_LIMIT
            }("");

            if (!success) revert NativeTransferFailed();
        } else {
            token.safeTransfer(to, amount);
        }
@>  }
}
```

## Recommendation

We recommend reverting the transaction when the amount is zero.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Gluex |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/GlueX-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

