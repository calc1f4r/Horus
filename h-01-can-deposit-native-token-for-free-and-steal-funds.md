---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: erc20

# Attack Vector Details
attack_type: erc20
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1624
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/55

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.27
financial_impact: high

# Scoring
quality_score: 1.3333333333333333
rarity_score: 1.3333333333333333

# Context Tags
tags:
  - erc20

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel
  - CertoraInc
---

## Vulnerability Title

[H-01] Can deposit native token for free and steal funds

### Overview


This bug report is about a vulnerability in the LiquidityPool.sol contract. The vulnerability allows an attacker to deposit infinite native tokens without paying anything. This is possible because the "depositErc20" function allows setting "tokenAddress = NATIVE" and does not throw an error. The contract will then emit the same "Deposit" event as a real "depositNative" call and the attacker receives the native funds on the other chain. The recommended mitigation step is to check "tokenAddress != NATIVE" in "depositErc20".

### Original Finding Content

_Submitted by cmichel, also found by CertoraInc_

[LiquidityPool.sol#L151](https://github.com/code-423n4/2022-03-biconomy/blob/db8a1fdddd02e8cc209a4c73ffbb3de210e4a81a/contracts/hyphen/LiquidityPool.sol#L151)<br>

The `depositErc20` function allows setting `tokenAddress = NATIVE` and does not throw an error.<br>
No matter the `amount` chosen, the `SafeERC20Upgradeable.safeTransferFrom(IERC20Upgradeable(tokenAddress), sender, address(this), amount);` call will not revert because it performs a low-level call to `NATIVE = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`, which is an EOA, and the low-level calls to EOAs always succeed.<br>
Because the `safe*` version is used, the EOA not returning any data does not revert either.<br>

This allows an attacker to deposit infinite native tokens by not paying anything.<br>
The contract will emit the same `Deposit` event as a real `depositNative` call and the attacker receives the native funds on the other chain.

### Recommended Mitigation Steps

Check `tokenAddress != NATIVE` in `depositErc20`.

**[ankurdubey521 (Biconomy) confirmed and commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/55):**
 > [HP-25: C4 Audit Fixes, Dynamic Fee Changes bcnmy/hyphen-contract#42](https://github.com/bcnmy/hyphen-contract/pull/42)

**[pauliax (judge) commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/55#issuecomment-1094973634):**
 > Great find, definitely deserves a severity of high.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 1.3333333333333333/5 |
| Rarity Score | 1.3333333333333333/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | cmichel, CertoraInc |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/55
- **Contest**: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest

### Keywords for Search

`ERC20`

