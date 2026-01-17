---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25297
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-illuminate
source_link: https://code4rena.com/reports/2022-06-illuminate
github_link: https://github.com/code-423n4/2022-06-illuminate-findings/issues/289

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-13] Leak of Value in `yield` function, slippage check is not effective

### Overview


This bug report was submitted by Alex the Entreprenerd. It is regarding the function `yield` in the code <https://github.com/code-423n4/2022-06-illuminate/blob/912be2a90ded4a557f121fe565d12ec48d0c4684/lender/Lender.sol#L641-L654>. The function `yield` is using the input from `sellBasePreview` and is not performing any validation on the value. This means that the check is equivalent to setting `returned = 0`. As a result, it is recommended to add checks or have a trusted keeper bulk `sellBase` with an additional slippage check as the function parameter. This bug report was confirmed by sourabhmarathe (Illuminate).

### Original Finding Content

_Submitted by Alex the Entreprenerd_

The function `yield` is using the input from `sellBasePreview` and then using it.

<https://github.com/code-423n4/2022-06-illuminate/blob/912be2a90ded4a557f121fe565d12ec48d0c4684/lender/Lender.sol#L641-L654>

```solidity
    function yield(
        address u,
        address y,
        uint256 a,
        address r
    ) internal returns (uint256) {
        // preview exact swap slippage on yield
        uint128 returned = IYield(y).sellBasePreview(Cast.u128(a));

        // send the remaing amount to the given yield pool
        Safe.transfer(IERC20(u), y, a);

        // lend out the remaining tokens in the yield pool
        IYield(y).sellBase(r, returned);
```

The output of `sellBasePreview` is meant to be used off-chain to avoid front-running and price changes, additionally no validation is performed on this value (is it zero, is it less than 95% of amount) meaning the check is equivalent to setting `returned = 0`

I'd recommend to add checks, or ideally have a trusted keeper bulk `sellBase` with an additional slippage check as the function parameter

**[sourabhmarathe (Illuminate) confirmed](https://github.com/code-423n4/2022-06-illuminate-findings/issues/289)** 



***





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-illuminate
- **GitHub**: https://github.com/code-423n4/2022-06-illuminate-findings/issues/289
- **Contest**: https://code4rena.com/reports/2022-06-illuminate

### Keywords for Search

`vulnerability`

