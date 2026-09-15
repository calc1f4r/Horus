---
# Core Classification
protocol: Backd
chain: everychain
category: uncategorized
vulnerability_type: min/max_cap_validation

# Attack Vector Details
attack_type: min/max_cap_validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2100
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-backd-contest
source_link: https://code4rena.com/reports/2022-04-backd
github_link: https://github.com/code-423n4/2022-04-backd-findings/issues/87

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - min/max_cap_validation

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

[M-11] Position owner should set allowed slippage

### Overview


This bug report is about a vulnerability in the code for the TopUpAction.sol contract, which is part of the 2022-04-backd project. The vulnerability allows malicious keepers and owners to sandwich attack topup, meaning they can bundle swaps before and after the topup to take advantage of it. The default swap slippage of 5% allows malicious keepers to do this, and up to 40% slippage allows malicious owners to sandwich huge amounts from the topup. To mitigate this vulnerability, it is recommended to allow users to specify a maximum swap slippage when creating the topup, similar to how it is done on Uniswap or Sushiswap, to block attacks from both keepers and owners.

### Original Finding Content

_Submitted by 0x52_

[TopUpAction.sol#L154](https://github.com/code-423n4/2022-04-backd/blob/c856714a50437cb33240a5964b63687c9876275b/backd/contracts/actions/topup/TopUpAction.sol#L154)<br>
[TopUpAction.sol#L187](https://github.com/code-423n4/2022-04-backd/blob/c856714a50437cb33240a5964b63687c9876275b/backd/contracts/actions/topup/TopUpAction.sol#L187)<br>

The default swap slippage of 5% allows malicious keepers to sandwich attack topup. Additionally, up to 40% (\_MIN_SWAPPER_SLIPPAGE) slippage allows malicious owner to sandwich huge amounts from topup

### Proof of Concept

Keeper can bundle swaps before and after topup to sandwich topup action, in fact it's actually in their best interest to do so.

### Recommended Mitigation Steps

Allow user to specify max swap slippage when creating topup similar to how it's specified on uniswap or sushiswap to block attacks from both keepers and owners.

**[chase-manning (Backd) confirmed and resolved](https://github.com/code-423n4/2022-04-backd-findings/issues/87)**

**[gzeon (judge) commented](https://github.com/code-423n4/2022-04-backd-findings/issues/87#issuecomment-1121225398):**
 > According to [C4 Judging criteria](https://docs.code4rena.com/roles/judges/how-to-judge-a-contest#notes-on-judging)
> > Unless there is something uniquely novel created by combining vectors, most submissions regarding vulnerabilities that are inherent to a particular system or the Ethereum network as a whole should be considered QA. Examples of such vulnerabilities include front running, sandwich attacks, and MEV. 
> 
> However since Backd use keeper to run topup transactions, which presumably are bots and smart contracts that can fetch onchain price directly. A large (5% default, up to 40%) seems excessive and can lead to user losing fund. Judging this as Medium Risk.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Backd |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-backd
- **GitHub**: https://github.com/code-423n4/2022-04-backd-findings/issues/87
- **Contest**: https://code4rena.com/contests/2022-04-backd-contest

### Keywords for Search

`Min/Max Cap Validation`

