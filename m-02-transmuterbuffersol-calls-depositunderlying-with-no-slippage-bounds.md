---
# Core Classification
protocol: Alchemix
chain: everychain
category: uncategorized
vulnerability_type: slippage

# Attack Vector Details
attack_type: slippage
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2367
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-alchemix-contest
source_link: https://code4rena.com/reports/2022-05-alchemix
github_link: https://github.com/code-423n4/2022-05-alchemix-findings/issues/222

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
  - slippage

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

[M-02] TransmuterBuffer.sol calls depositUnderlying with no slippage bounds

### Overview


This bug report concerns a vulnerability in a contract code called TransmuterBuffer. This vulnerability could result in a loss of funds in TransmuterBuffer. The vulnerability occurs when the buffer is called during an unfavorable time, which could cause a large portion of deposited funds to be lost due to slippage. To mitigate this issue, a slippage calculation similar to _alchemistWithdraw should be implemented to protect against it.

### Original Finding Content

_Submitted by 0x52_

Loss of funds in TransmuterBuffer

### Proof of Concept

If the buffer is called during and unfavorable time then a large portion of deposited funds may be lost due to slippage because deposit is called with 0 as the minimum out allowing any level of slippage

### Recommended Mitigation Steps

Implement a slippage calculation similar to `\_alchemistWithdraw` to protect against it


**[0xfoobar (Alchemix) acknowledged, disagreed with severity and commented](https://github.com/code-423n4/2022-05-alchemix-findings/issues/222#issuecomment-1133985891):**

> This function is only called by keeper bots harvesting yields, which should not be subject to large slippage and could be sent through a private mempool if necessary. However, we acknowledge that a configurable parameter could enable greater protection, even if in practice the issue does not occur.

**[0xleastwood (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-05-alchemix-findings/issues/222#issuecomment-1146180192):**
 > Because this requires the keeper role to sandwich attack the protocol when yield is harvested, this better fits the criteria of a `medium` severity issue.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Alchemix |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-alchemix
- **GitHub**: https://github.com/code-423n4/2022-05-alchemix-findings/issues/222
- **Contest**: https://code4rena.com/contests/2022-05-alchemix-contest

### Keywords for Search

`Slippage`

