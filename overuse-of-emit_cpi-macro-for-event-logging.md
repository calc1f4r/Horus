---
# Core Classification
protocol: SVM Spoke Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56774
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/svm-spoke-audit
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

Overuse of emit_cpi! Macro for Event Logging

### Overview

The `emit_cpi!` macro is being overused in the codebase, causing unnecessary computational overhead. This can lead to Solana's transaction compute budget limits being exceeded, potentially impacting the program's functionality. To mitigate this issue, it is recommended to limit the use of `emit_cpi!` to critical events that may exceed the log size limit or be subject to truncation. For non-sensitive events, the `emit!` macro should be used to efficiently utilize compute resources. The team has decided not to replace `emit_cpi!` with `emit!` due to potential risks, and will continue to use `emit_cpi!` for consistency. 

### Original Finding Content

The `emit_cpi!` macro is extensively utilized across the codebase for logging events, even in scenarios where the standard `emit!` macro would suffice. While `emit_cpi!` provides benefits such as preventing log truncation by leveraging Solana’s instruction data storage, its overuse introduces unnecessary computational overhead.

The `emit_cpi!` macro works by executing a self-invocation with the event data, ensuring logs remain intact regardless of size. However, this approach has trade-offs, as creating and invoking new instructions consumes additional compute budget within transactions. Solana’s transactions have strict compute budget limits, and excessive use of `emit_cpi!` can result in these limits being exceeded, potentially impacting the program's functionality.

To mitigate these issues, consider limiting the use of `emit_cpi!` to the following cases:

* Events that are likely to exceed the log size limit (10 KB) and are critical to preserve.
* Events that might be subject to truncation in malicious scenarios.
* Events emitted alongside other logs where truncation is likely.

For non-sensitive events or those occurring behind admin actions in which goodwill is assumed, the `emit!` macro is more appropriate. Doing this ensures that compute resources are utilized efficiently without compromising the reliability of critical logs.

***Update:** Acknowledged, not resolved. The team stated:*

> *We have decided not to replace some of the emit\_cpi! events with native emit! events. This decision stems from the potential risk of an attacker prepending instructions that fill the logs before invoking the svm-spoke functions, which could cause the logs to be dropped. To mitigate this risk, we opted to continue using emit\_cpi!. While certain cases, might be safe to use native emit! events, we chose to maintain emit\_cpi! for consistency across all events. Additionally, it is preferable to always query events using the same technique in all contexts, not requiring some code to use emit\_cpi! and others to use emit! logic.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | SVM Spoke Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/svm-spoke-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

