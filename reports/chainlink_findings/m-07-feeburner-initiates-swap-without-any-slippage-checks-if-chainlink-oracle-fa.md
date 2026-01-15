---
# Core Classification
protocol: Backd
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42665
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-05-backd
source_link: https://code4rena.com/reports/2022-05-backd
github_link: https://github.com/code-423n4/2022-05-backd-findings/issues/44

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
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-07] FeeBurner initiates swap without any slippage checks if Chainlink oracle fails

### Overview


The submitted bug report highlights a potential issue in the FeeBurner contract, which is a dependency of the SwapperRouter contract. The SwapperRouter contract uses a chainlink oracle to determine the minimum amount of tokens for a swap, but if the oracle fails, the contract will use a value of 0 instead. This could lead to potential sandwich attacks, where the value of the swap can be manipulated. The report recommends either reverting the transaction or using a default slippage of 99% to mitigate this issue. The sponsor of the contract has disputed this recommendation, stating that they want to offer a service to the end user by allowing any swappable token to be used, even if it presents a potential risk. The judge has acknowledged the sponsor's intent, but still considers this to be a medium severity issue as it could lead to the extraction of value.

### Original Finding Content

_Submitted by Ruhum_

<https://github.com/code-423n4/2022-05-backd/blob/main/protocol/contracts/tokenomics/FeeBurner.sol#L43-L88>

<https://github.com/code-423n4/2022-05-backd/blob/main/protocol/contracts/swappers/SwapperRouter.sol#L414-L425>

<https://github.com/code-423n4/2022-05-backd/blob/main/protocol/contracts/swappers/SwapperRouter.sol#L439>

### Impact

While the SwapperRouter contract isn't explicitly in scope, it's a dependency of the FeeBurner contract which *is* in scope. So I think it's valid to make this submission.

The SwapperRouter contract uses the chainlink oracle to compute the minimum amount of tokens it should expect from the swap. The value is then used for the slippage check. But, if the chainlink oracle fails, for whatever reason, the contract uses `0` for the slippage check instead. Thus there's a scenario where swaps initiated by the FeeBurner contract can be sandwiched.

### Proof of Concept

1.  multiple swaps initiated through [`FeeBurner.burnToTarget()`](https://github.com/code-423n4/2022-05-backd/blob/main/protocol/contracts/tokenomics/FeeBurner.sol#L43-L88)
2.  SwapperRouter calls [`_minTokenAmountOut()`](https://github.com/code-423n4/2022-05-backd/blob/main/protocol/contracts/swappers/SwapperRouter.sol#L220) to determine `min_out` parameter.
3.  [`minTokenAmountOut()`](https://github.com/code-423n4/2022-05-backd/blob/main/protocol/contracts/swappers/SwapperRouter.sol#L414-L425) returns `0` when Chainlink oracle fails

### Recommended Mitigation Steps

Either revert the transaction or initiate the transaction with a default slippage of 99%. In the case of Curve, you can get the expected amount through `get_dy()` and then multiply the value by 0.99. Use that as the `min_out` value and you don't have to worry about chainlink

**[chase-manning (Backd) disputed and commented](https://github.com/code-423n4/2022-05-backd-findings/issues/44#issuecomment-1147362714):**
 > This is intended functionality. If there is no oracle for a token, we still want to swap it, even if this presents a possible sandwich attack. It should be rare for a token to not have an oracle, and when it does we would rather accept slippage as opposed to not being able to swap it at all.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-05-backd-findings/issues/44#issuecomment-1159775547):**
 > I acknowledge the sponsor reply that they want to offer a service to the end user in allowing any swappable token to be used.
> 
> While I believe the intent of the sponsor is respectable, the reality of the code is that it indeed allows for price manipulation and extraction of value, personally I would recommend end users to perform their own swaps to ensure a more reliable outcome.
> 
> That said, because the code can be subject to leak of value, I believe Medium Severity to be appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Backd |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-backd
- **GitHub**: https://github.com/code-423n4/2022-05-backd-findings/issues/44
- **Contest**: https://code4rena.com/reports/2022-05-backd

### Keywords for Search

`vulnerability`

