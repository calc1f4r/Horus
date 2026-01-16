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
solodit_id: 2095
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-backd-contest
source_link: https://code4rena.com/reports/2022-04-backd
github_link: https://github.com/code-423n4/2022-04-backd-findings/issues/47

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
finders_count: 2
finders:
  - shenwilly
  - wuwe1
---

## Vulnerability Title

[M-06] ERC777 tokens can bypass `depositCap` guard

### Overview


This bug report is about a vulnerability in the LiquidityPool contract of the code-423n4/2022-04-backd repository. If an ERC777 token is used as the underlying token for a LiquidityPool, a depositor can reenter depositFor and bypass the depositCap requirement check, resulting in a higher total deposit than intended by governance. This is demonstrated in the Proof of Concept section of the report, which shows that a depositor can deposit more tokens than the deposit cap allows. The recommended mitigation step to fix this vulnerability is to add reentrancy guards to depositFor.

### Original Finding Content

_Submitted by shenwilly, also found by wuwe1_

[LiquidityPool.sol#L523](https://github.com/code-423n4/2022-04-backd/blob/c856714a50437cb33240a5964b63687c9876275b/backd/contracts/pool/LiquidityPool.sol#L523)<br>

When ERC777 token is used as the underlying token for a `LiquidityPool`, a depositor can reenter `depositFor` and bypass the `depositCap` requirement check, resulting in higher total deposit than intended by governance.

### Proof of Concept

*   An empty ERC777 liquidity pool is capped at 1.000 token.
*   Alice deposits 1.000 token. Before the token is actually sent to the contract, `tokensToSend` ERC777 hook is called and Alice reenters `depositFor`.
*   As the previous deposit hasn't been taken into account, the reentrancy passes the `depositCap` check.
*   Pool has 2.000 token now, despite the 1.000 deposit cap.

### Recommended Mitigation Steps

Add reentrancy guards to `depositFor`.

**[chase-manning (Backd) confirmed and resolved](https://github.com/code-423n4/2022-04-backd-findings/issues/47)**



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
| Finders | shenwilly, wuwe1 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-backd
- **GitHub**: https://github.com/code-423n4/2022-04-backd-findings/issues/47
- **Contest**: https://code4rena.com/contests/2022-04-backd-contest

### Keywords for Search

`vulnerability`

