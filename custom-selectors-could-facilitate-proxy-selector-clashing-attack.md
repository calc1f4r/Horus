---
# Core Classification
protocol: Security Review ink! & cargo-contract
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33101
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/security-review-ink-cargo-contract
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
  - OpenZeppelin
---

## Vulnerability Title

Custom Selectors could facilitate proxy selector clashing attack

### Overview


The ink! feature that allows developers to hardcode the selector for a function can lead to proxy selector clashing. This means that when a user calls a function, it may accidentally execute code within the proxy instead of the intended function. This can make it easier for scam projects to create malicious backdoors that are hard to detect. Using custom selectors can also confuse third-party monitoring services and may cause errors. The report suggests rethinking this feature and finding an alternative solution for language-agnostic contract standards. The issue has been acknowledged and the progress can be tracked on the "ink" repository's issue 1643.

### Original Finding Content

ink! has a feature that allows developers to hardcode the selector for a given function. This capability enables function name-changing while maintaining the same selector and also facilitates the creation of language-agnostic contract standards.


However, allowing custom selectors in contracts can lead to proxy selector clashing. When a user calls a specific function on an implementation, a matching selector in the proxy can cause unintended execution of code within the proxy. This issue makes it easier for scam projects to create malicious backdoors that are difficult to detect. In contrast to ink!, Solidity requires finding function signatures with matching selectors before taking advantage of this vulnerability, which is not trivial. If such function signatures are found and added, they are likely to raise red flags because the name usually does not make sense to the codebase.


Custom selectors can also confuse third-party monitoring or indexing services that use function selectors to identify specific functions. These services may rely on standard selectors, which are part of standards or belong to community databases such as the 4byte directory. If contracts use custom selectors, these services may fail to recognize and monitor transactions, leading to errors.


Given the potential dangers outlined, it is worth rethinking this feature and looking for an alternative to handle language-agnostic contract standards. Alternatively, requiring the metadata of the implementation contract to build the proxy and preventing the code from being compiled if selector clashing occurs with the implementation may be a viable solution. If the benefits of using custom selectors are not greater than the potential risks, consider removing them.


***Update:** Acknowledged, will resolve. The progress can be tracked on [issue 1643](https://github.com/paritytech/ink/issues/1643) of the “ink” repository.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Security Review ink! & cargo-contract |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/security-review-ink-cargo-contract
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

