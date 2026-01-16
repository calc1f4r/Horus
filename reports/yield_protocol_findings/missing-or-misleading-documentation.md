---
# Core Classification
protocol: Origin Balancer MetaPool Strategy Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32990
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/origin-balancer-metapool-audit
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

Missing or Misleading Documentation

### Overview


The codebase for this project has multiple sections that are difficult to understand and would benefit from more documentation. Specifically, there are issues with understanding how reward tokens are actually rewarded to the strategy, as well as the math behind certain functions related to Balancer. It is suggested to add more details and practical examples to make these processes clearer. Additionally, the documentation for adding strategies using Balancer is not specific to the `BalancerMetaPoolStrategy` and may differ from the audited implementation. It is recommended to create specific and concise documentation for this strategy to explain the design decisions behind each important piece. These issues have been resolved in two pull requests.

### Original Finding Content

Throughout the codebase, there are multiple sections which are difficult to understand, and would benefit from additional or clearer documentation:


* It was difficult to assert that reward tokens are [actually rewarded to the strategy.](https://github.com/OriginProtocol/origin-dollar/blob/eb11498c376b65696c90981757221b076d6226aa/contracts/contracts/strategies/balancer/BaseAuraStrategy.sol#L84) Consider adding more details around how this happens, especially for the AURA tokens where the process is more complex and not intuitive to follow.
* Given the intricacies of how Balancer works, as well as the need to wrap rebasing tokens, it was difficult to follow [the math](https://github.com/OriginProtocol/origin-dollar/blob/eb11498c376b65696c90981757221b076d6226aa/contracts/contracts/strategies/balancer/BaseBalancerStrategy.sol#L228C5-L251C8) behind the `getBPTExpected` functions.
* Consider adding a practical example, as well as explanations regarding what each variable means and what each price is measured in. Consider documenting why the Balancer read-only reentrancy check is not needed on deposit and withdrawal functions.


Additionally, while there was documentation around the addition of strategies using Balancer, it was at times misleading as it was not specifically targeted towards the `BalancerMetaPoolStrategy`, and hence would differ from the implementation that was audited. Consider creating documentation specific to the strategy at hand, explicitly and concisely explaining the design decisions behind each important piece.


***Update:****Resolved in [pull request #1781](https://github.com/OriginProtocol/origin-dollar/pull/1781) and [pull request #1795.](https://github.com/OriginProtocol/origin-dollar/pull/1795)*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Origin Balancer MetaPool Strategy Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/origin-balancer-metapool-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

