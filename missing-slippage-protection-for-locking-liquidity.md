---
# Core Classification
protocol: UNCX UniswapV3 Liquidity Locker Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32618
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uncx-uniswapv3-liquidity-locker-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Missing Slippage Protection for Locking Liquidity

### Overview


The bug report describes an issue with the UniswapV3 liquidity locking function, specifically when a position is locked that is not full-range. This causes the liquidity distribution in the pool to change, which can be exploited by an attacker to make a profit. The report suggests adding slippage parameters to the locking function to prevent this issue. The bug has since been resolved in a recent update.

### Original Finding Content

When a UniswapV3 position is locked that is not full-range, the liquidity position is removed and redeposited in the [`_convertPositionToFullRange`](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/blob/342c621cc93a13882601b30e547907877f3e3f86/contracts/UNCX_ProofOfReservesV2_UniV3.sol#L229) function. In this situation, the liquidity between the `tickUpper` and `tickLower` decreases while the liquidity in any tick outside of that range increases. These changes in the liquidity distribution of the UniswapV3 pool can be sandwiched for a profit by manipulating the AMM with a large buy order of one token and then selling that token back into the new liquidity distribution.


The sandwiching attack requires manipulating the pool tick such that it is outside the victim's tick range (`tickLower` to `tickUpper`) when they lock their liquidity. However, when the liquidity is removed, the liquidity position is comprised entirely of one token and none of the other token. When this liquidity gets redeposited in the `mint` call, since there is an amount of `0` for one of the tokens, the contract will attempt to mint `0` liquidity and revert.


The attacker can still make the victim deposit the full amount of liquidity by transferring a small amount of the missing token directly to the contract before the `lock` call. At this point, since the AMM is already manipulated to an extreme tick, only a small transfer is required to complete the liquidity deposit. The cost of the direct transfer ends up being negligible compared to the attacker's profit.


Consider adding slippage parameters to the `lock` function. These slippage parameters can either be determined by input parameters or hard coded to require the pool's price tick to be within a locker's position's tick range.


***Update**: Resolved in [pull request #1](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/pull/1) at commit [56a8037](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/pull/1/commits/56a80378854790dac3ced20ed576fa117289890b).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UNCX UniswapV3 Liquidity Locker Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uncx-uniswapv3-liquidity-locker-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

