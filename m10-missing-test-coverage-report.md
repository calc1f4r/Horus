---
# Core Classification
protocol: Aave Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11615
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/aave-protocol-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M10] Missing test coverage report

### Overview


This bug report is about the lack of automated test coverage report for the Aave protocol. Without this report, it is impossible to know if there are parts of the code that are not being tested by the automated tests. This is a problem because high test coverage is important for projects like Aave, where large sums of valuable assets are expected to be handled safely and bugs can cause financial losses. The report recommends adding the test coverage report and making it reach at least 95% of the source code.

The bug report has been acknowledged and a fix is in progress. The Aave team was working on setting up coverage on a separate branch during the audit, but some problems arose due to the tools being immature and unstable. The team is aware of the importance of high test coverage and is working to reach at least 95% coverage before launch.

### Original Finding Content

There is no automated test coverage report. Without this report it is impossible to know whether there are parts of the code never executed by the automated tests; so for every change, a full manual test suite has to be executed to make sure that nothing is broken or misbehaving. High test coverage is of utter importance in projects like the Aave protocol, where large sums of valuable assets are expected to be handled safely and bugs can cause important financial losses.


Consider adding the test coverage report, and making it reach at least 95% of the source code.


**Update**: *Acknowledged, and fix in progress. The Aave team was working on setting up coverage on a separate branch during our audit. Given the tools are still immature and unstable, some problems arised in the process which are now being solved by customizing the coverage tools to Aave’s needs. The team is fully aware of the importance of high test coverage, and is striving to reach at least 95% coverage before launch.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Aave Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/aave-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

