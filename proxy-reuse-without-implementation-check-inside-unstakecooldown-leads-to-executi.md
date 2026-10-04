---
# Core Classification
protocol: Strata Tranches
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63228
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
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
finders_count: 3
finders:
  - InAllHonesty
  - Arno
  - Stalin
---

## Vulnerability Title

Proxy reuse without implementation check inside `UnstakeCooldown` leads to execution on outdated/vulnerable logic

### Overview


The bug report describes an issue where the contract is reusing old proxies without checking if they were created from the current implementation. This can cause inconsistent behavior, security risks, and mismatches in accounting or logic. A proof of concept is provided, along with a recommended mitigation to verify the proxy's implementation before reusing it. The bug has been fixed in the latest commit by implementing a validation to check for differences in the implementation and creating a new proxy if necessary. The report has been verified by Cyfrin.

### Original Finding Content

**Description:** The contract reuses old proxies from the user’s `UnstakeCooldown::proxiesPool` without verifying whether those proxies were created from the current implementation. Since a clone’s target implementation is permanently embedded in its bytecode, if the owner updates `implementations[token]` using the available `UnstakeCooldown::setImplementations`, any proxies already in a user’s pool will still delegate to the old implementation.

**Impact:** Users may continue operating through outdated or vulnerable implementations even after the owner updates `implementations`. This can cause:
- Inconsistent behavior across requests (some proxies use the new implementation, others use the old one).
- Security risks if the previous implementation contains a bug or vulnerability.
- Accounting or logic mismatches if old and new implementations are not compatible.

**Proof of Concept:**
1. Owner sets `implementations[token] = ImplV1`.
2. Alice makes two transfers, creating two proxies that point to `ImplV1`.
3. Owner later calls `setImplementations(token, ImplV2)`.
4. Some time passes, the two proxies pointing to `ImplV1` are available.
5. Alice makes another transfer. The contract pops a proxy from her pool and reuses it.
6. That proxy still delegates to `ImplV1`, even though `implementations[token]` is now `ImplV2`.

**Recommended Mitigation:** When reusing proxies, verify that the proxy’s implementation matches the current `implementations[token]`. If not, discard the old proxy and create a new one.

**Strata:**
Fixed in commit [ffbedf48d](https://github.com/Strata-Money/contracts-tranches/commit/ffbedf48d268f2617e189cddc1daa167220082b3) by implementing a validation to check if the current implementation for a token is different than the implementation that was used to create a proxy being reused. If so, then a new proxy is made with the new implementation, and the old proxy is discarded.

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Strata Tranches |
| Report Date | N/A |
| Finders | InAllHonesty, Arno, Stalin |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

