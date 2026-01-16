---
# Core Classification
protocol: Ufarm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62441
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-06-10-Ufarm.md
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
  - Hexens
---

## Vulnerability Title

[UFARM1-3] Ques Callback Iterates Over Deposit and Withdraw Queues Backwards

### Overview


The bug report describes a medium severity issue in a program called `UFarmPool:quexCallback`. The problem is that the queues for deposits and withdrawals are being processed in reverse order, which means that requests are not being handled in the order they were received. This can lead to unfairness in the system. The report suggests implementing a rate limiter to fix the issue, but even with this solution, the requests will still be processed out of order. The recommended remediation is to process the queues in chronological order. The bug has been fixed.

### Original Finding Content

**Severity:** Medium

**Description:** In `UFarmPool:quexCallback`, the queues for deposits and withdrawals are processed, however they are handled in reverse order, from the most recent to the oldest. This means the original order in which users made their requests is not respected.
```
requestsLength = depositQueue.length;
while (requestsLength > 0) {
    // Validate each deposit request
    depositItem = depositQueue[requestsLength - 1];
```
If the remediation for `UFARM1-2: Quex callback can be permanently DoSed by congesting queues`
 such as introducing a rate limiter, is implemented, there would still be an unfair order of processing if requests continue to be handled in reverse. To ensure fairness, the system should process requests in the order they were received.

**Remediation:**  Handle the depositQueue and withdrawQueue in chronological order.

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Ufarm |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-06-10-Ufarm.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

