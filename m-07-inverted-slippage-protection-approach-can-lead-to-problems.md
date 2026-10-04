---
# Core Classification
protocol: Gmd
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20390
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-12-01-GMD.md
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
  - Pashov
---

## Vulnerability Title

[M-07] Inverted slippage protection approach can lead to problems

### Overview


The bug report discusses a vulnerability in the protocol that can lead to funds being lost from the vault. The vulnerability is caused by an unusual approach to slippage protection, which results in the protocol sending more $GLP than necessary in order to swap. This can be used as a griefing attack vector, where a user deposits and withdraws from a vault multiple times to drain the pool's $GLP balance.

The recommendation is to redesign the `leave` methods so that the user pays the slippage cost instead of the protocol. This will reduce the likelihood of the vulnerability being exploited and limit the potential impact.

### Original Finding Content

**Likelihood:**
Low, because it needs more than one special condition simultaneously

**Impact:**
Medium, because it can lead to limited amount of funds lost from the protocol

**Description**

Both the `leaveETH` and `leave` methods use the `slippage` storage variable to implement slippage protection for the users leaving the vault. The problem is that the slippage protection is done in an unusual approach which can result in problems. Both methods call the `swapGLPto` method which has the `min_receive` parameter that is passed to the `unstakeAndRedeemGlp` method in `GLPRouter`. The usual approach to slippage protection is to calculate how much tokens you expect to receive after a swap, let's say 100 $TKN, and then apply some slippage tolerance percentage to it - if the tolerance is 5% then the minimum expected tokens received is 95 $TKN. The protocol implemented a different approach, instead of providing a smaller expected received value it actually inflates the value to be sent for the swap.

```solidity
uint256 percentage = 100000 - slippage;
uint256 glpPrice = priceFeed.getGLPprice().mul(percentage).div(100000);
uint256 glpOut = amountOut.mul(10**12).mul(tokenPrice).div(glpPrice).div(10**30);
```

As you see, the way it works is "expecting" a lower price of $GLP which means the protocol always sends more $GLP than needed to swap. Now if the slippage protection is bigger than the deposit fee this can be used as a griefing attack vector by depositing and then withdrawing from a vault multiple times to drain the pool's $GLP balance.

**Recommendations**

Think about redesigning the `leave` methods so that you make the user pay the slippage cost instead of the protocol.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Gmd |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-12-01-GMD.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

