---
# Core Classification
protocol: Umami
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57483
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-13-Umami.md
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
  - Zokyo
---

## Vulnerability Title

Uniswap V3 swap in `commitAndClose` susceptible to sandwich attack

### Overview


The report describes a bug in the TracerGMXVault.sol code where a transaction can be exposed to a sandwich attack due to a snippet of code in the swapToStable function. This bug can be exploited by setting the amountOutMinimum to zero, which can result in significant loss. The recommendation is to use an external price source to prevent front-running and to refer to Uniswap's official documentation for further guidance. The bug has been resolved.

### Original Finding Content

**Description**

TracerGMXVault.sol - In body of swapToStable(...), call stack starts from external function commitAndClose(). This transaction can be spotted in pool and exposed to sandwich attack because of this snippet:

ISwapRouter.ExactInputParams memory params = ISwapRouter.ExactInputParams({
 path: route,

});

recipient: address(this),

deadline: block.timestamp,

amountIn: wethBalance,

amountOutMinimum: 0

return router.exactInput(params)

setting amountOutMinimum to zero give a chance to the attacker to exploit that. Severity of this explained by uniswap's official docs

https://docs.uniswap.org/protocol/guides/swaps/single-swaps

amountOutMinimum: we are setting to zero, but this is a significant risk in production. For a real deployment, this value should be calculated using our SDK or an onchain price oracle this helps protect against getting an unusually bad price for a trade due to a front running sandwich or another type of price manipulation

**Recommendation**

When trading from a smart contract, the most important thing to keep in mind is that access to an external price source is required. Without this, trades can be frontrun for considerable loss.

uniswap's official docs

**Re-audit comment**

Resolved

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Umami |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-13-Umami.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

