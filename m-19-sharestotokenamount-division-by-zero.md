---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42515
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-biconomy
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/53

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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-19] `sharesToTokenAmount`: Division by zero

### Overview


The bug report is about a function called `sharesToTokenAmount` in the `LiquidityProviders.sol` file. The function does not check for a specific condition, causing it to revert and potentially cause errors. The suggested solution is to return 0 in case the condition is not met. The bug has been confirmed by a team member and a judge has commented on it.

### Original Finding Content

_Submitted by cmichel, also found by cccz and CertoraInc_

[LiquidityProviders.sol#L192](https://github.com/code-423n4/2022-03-biconomy/blob/db8a1fdddd02e8cc209a4c73ffbb3de210e4a81a/contracts/hyphen/LiquidityProviders.sol#L192)<br>

The public `sharesToTokenAmount` function does not check if the denominator `totalSharesMinted[_tokenAddress]` is zero.<br>
Neither do the callers of this function. The function will revert.<br>
Calling functions like `getFeeAccumulatedOnNft` and `sharesToTokenAmount` from another contract should never revert.<br>

### Recommended Mitigation Steps

Return 0 in case `totalSharesMinted[_tokenAddress]` is zero.

**[ankurdubey521 (Biconomy) confirmed](https://github.com/code-423n4/2022-03-biconomy-findings/issues/53)**

**[pauliax (judge) commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/53#issuecomment-1120953089):**
 > A valid concern of runtime error.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/53
- **Contest**: https://code4rena.com/reports/2022-03-biconomy

### Keywords for Search

`vulnerability`

