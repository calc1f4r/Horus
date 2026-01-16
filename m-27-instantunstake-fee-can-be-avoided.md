---
# Core Classification
protocol: Yieldy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2902
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-yieldy-contest
source_link: https://code4rena.com/reports/2022-06-yieldy
github_link: https://github.com/code-423n4/2022-06-yieldy-findings/issues/9

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
  - liquid_staking
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - skoorch
---

## Vulnerability Title

[M-27] instantUnstake fee can be avoided

### Overview


A bug was recently discovered in the LiquidityReserve.sol contract, which is part of the code-423n4/2022-06-yieldy repository. This bug allows users to utilize the `instantUnstake` function without paying the liquidity provider fee using rounding errors in the fee calculation. This attack is not feasible on mainnet, but it is likely feasible on low-cost L2s and for tokens with a small decimal precision. The bug is caused by the `instantUnstake` fee being handled by sending the user back `amount - fee`, which causes the fee to be rounded down rather than the amount.

The recommended mitigation steps for this bug include avoiding the use of subtraction to calculate the fee. Instead, a muldiv operation over (1 - fee) should be used. This would effectively round up the fee instead of down, so it can never be 0 unless the fee is 0. Uniswapv2 already implements this solution for their LP fee. This solution would look something like this: `uint256 amountMinusFee = amount * (BASIS_POINTS - fee) / BASIS_POINTS`.

### Original Finding Content

_Submitted by skoorch_

Users can utilize the `instantUnstake` function without paying the liquidity provider fee using rounding errors in the fee calculation. This attack only allows for a relatively small amount of tokens to be unstaked in each call, so is likely not feasible on mainnet. However, on low-cost L2s and for tokens with a small decimal precision it is likely a feasible workaround.

### Proof of Concept

The `instantUnstake` fee is handled by sending the user back `amount - fee`. We can work around the fee by unstaking small amounts (`amount < BASIS_POINTS / fee`) in a loop until reaching the desired amount.

### Recommended Mitigation Steps

Avoid using subtraction to calculate the fee as this causes the fee to be rounded down rather than the amount. I'd propose calculating amount less fee using a muldiv operation over (1 - fee). In this case, the fee is effectively rounded up instead of down, so it can never be 0 unless fee is 0. Uniswapv2 uses a similar solution for their LP fee: <https://github.com/Uniswap/v2-core/blob/8b82b04a0b9e696c0e83f8b2f00e5d7be6888c79/contracts/UniswapV2Pair.sol#L180-L182>

It might look like the following:

    uint256 amountMinusFee = amount * (BASIS_POINTS - fee) / BASIS_POINTS

**[toshiSat (Yieldy) confirmed and resolved](https://github.com/code-423n4/2022-06-yieldy-findings/issues/9)**

***





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yieldy |
| Report Date | N/A |
| Finders | skoorch |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-yieldy
- **GitHub**: https://github.com/code-423n4/2022-06-yieldy-findings/issues/9
- **Contest**: https://code4rena.com/contests/2022-06-yieldy-contest

### Keywords for Search

`vulnerability`

