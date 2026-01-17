---
# Core Classification
protocol: Gearbox Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30770
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Gearbox%20Protocol/Gearbox%20Protocol%20v.3%20Bots%20&%20Integrations/README.md#5-lack-of-path-validation-in-the-velodrome-adapter
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
  - MixBytes
---

## Vulnerability Title

Lack of path validation in the `Velodrome` adapter

### Overview


The `swapExactTokensForTokens` and `swapDiffTokensForTokens` functions in `VelodromeV2RouterAdapter` are accepting a `routes` parameter that can cause unexpected behavior. This is because the `Adapter` and `Router` are not properly checking if the `tokenOut` and `tokenIn` parameters of the routes match. This could lead to the loss of tokens from `Velodrome` pools. It is recommended to improve the validation of the `routes` parameter in the `Velodrome` adapter.

### Original Finding Content

##### Description
The swap functions `swapExactTokensForTokens` and `swapDiffTokensForTokens` of `VelodromeV2RouterAdapter` accepts `routes` parameter with arbitrary consequences of routes, consisting of (`tokenIn`, `tokenOut`, `stable`, `factory`) parameters. Neither `Adapter` or `Router` performs a check that the `tokenOut` parameter of the previous route matches the `tokenIn` parameter of the successive route. This may cause unexpected bahaviour, i.e. seizing the tokens by LP of `Velodrome` pools, which is unintended.

##### Recommendation
We recommend improving the validation of the `routes` parameter in the `Velodrome` adapter.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Gearbox Protocol |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Gearbox%20Protocol/Gearbox%20Protocol%20v.3%20Bots%20&%20Integrations/README.md#5-lack-of-path-validation-in-the-velodrome-adapter
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

