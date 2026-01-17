---
# Core Classification
protocol: Ondo Finance: Ondo Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17498
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf
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
finders_count: 3
finders:
  - Damilola Edwards
  - Anish Naik
  - Justin Jacob
---

## Vulnerability Title

Problematic use of safeApprove

### Overview

See description below for full details.

### Original Finding Content

## Difficulty: High

## Type: Data Validation

## Description
In order for users to earn yield on the collateral tokens they deposit, the Treasury contract sends the collateral tokens to a yield-bearing strategy contract that inherits from the BaseStablecoinStrategy contract. When a privileged actor calls the `redeem` function, the function approves the Treasury contract to pull the necessary funds from the strategy.

However, the function approves the Treasury contract by calling the `safeApprove` function.

```solidity
...
_redeem(amount);
stablecoin.safeApprove(getCurrentTreasury(), amount);
emit Redeem(address(stablecoin), amount, currentPosition, profit, loss);
}
```
*Figure 7.1: A snippet of the redeem function in BaseStablecoinStrategy.sol:#L106–L110*

As explained in the OpenZeppelin documentation, `safeApprove` should be called only if the currently approved amount is zero—when setting an initial allowance or when resetting the allowance to zero. Therefore, if the entire approved amount is not pulled by calling `Treasury.withdraw`, subsequent redemption operations will revert.

Additionally, OpenZeppelin’s documentation indicates that the `safeApprove` function is officially deprecated.

```solidity
/**
 * @dev Deprecated. This function has issues similar to the ones found in
 * {IERC20-approve}, and its usage is discouraged.
 *
 * Whenever possible, use {safeIncreaseAllowance} and
 * {safeDecreaseAllowance} instead.
 */
function safeApprove(
    IERC20 token,
    address spender,
    uint256 value
) internal {
    // safeApprove should only be called when setting an initial allowance,
    // or when resetting it to zero. To increase and decrease it, use
    // 'safeIncreaseAllowance' and 'safeDecreaseAllowance'
    require(
        (value == 0) || (token.allowance(address(this), spender) == 0),
        "SafeERC20: approve from non-zero to non-zero allowance"
    );
    _callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector,
    spender, value));
}
```
*Figure 7.2: The safeApprove function in SafeERC20.sol#L39–L59*

## Exploit Scenario
Bob, the fund manager of the Ondo protocol, deposits 200 tokens into the CompoundStrategy contract and calls `redeem` to redeem 100 of them. However, he calls `Treasury.withdraw` for only 50 tokens. Because the allowance allocated for `safeApprove` has not been completely used, he is blocked from performing subsequent redemption operations for the remaining 100 tokens.

## Recommendations
- **Short term:** Use `safeIncreaseAllowance` and `safeDecreaseAllowance` instead of `safeApprove`. Alternatively, document the fact that the Treasury should use up the entire approval amount before the privileged actor can call a strategy’s redeem function.
- **Long term:** Expand the dynamic fuzz testing suite to identify edge cases like this.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Ondo Finance: Ondo Protocol |
| Report Date | N/A |
| Finders | Damilola Edwards, Anish Naik, Justin Jacob |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf

### Keywords for Search

`vulnerability`

