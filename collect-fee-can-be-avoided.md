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
solodit_id: 32624
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uncx-uniswapv3-liquidity-locker-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Collect Fee Can Be Avoided

### Overview


This bug report is about a fee that is being assessed when users withdraw their NFT from the protocol after the time lock has expired. However, users have found a way to bypass this fee by using a different function. The report suggests that the logic for how the fee is collected should be reworked to prevent users from avoiding it. The bug has been resolved in a recent pull request.

### Original Finding Content

When users `withdraw` from the protocol (transfer back their NFT after the time lock has expired), [there is a "collect fee" that is assessed from the user](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/blob/342c621cc93a13882601b30e547907877f3e3f86/contracts/UNCX_ProofOfReservesV2_UniV3.sol#L365-L367). However, users can sidestep this fee by simply calling `decreaseLiquidity` instead [which transfers the full amount to the caller (the lock owner)](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/blob/342c621cc93a13882601b30e547907877f3e3f86/contracts/UNCX_ProofOfReservesV2_UniV3.sol#L335).


Consider reworking the logic for how the collect fee is collected.


***Update**: Resolved in [pull request #3](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/pull/3) at commit [8355982](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/pull/3/commits/8355982ca95cd635d5ba7d77cc8362a51071cfa1).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

