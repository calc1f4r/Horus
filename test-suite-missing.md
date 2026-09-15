---
# Core Classification
protocol: Elara Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59160
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/elara-finance/ceaf2e43-2883-4f4f-bd80-20dc354abb46/index.html
source_link: https://certificate.quantstamp.com/full/elara-finance/ceaf2e43-2883-4f4f-bd80-20dc354abb46/index.html
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
  - Gereon Mendler
  - Julio Aguilar
  - Valerian Callens
---

## Vulnerability Title

Test Suite Missing

### Overview


The client has acknowledged an issue with adapting Compound's test suite in their project, Elara. They are currently facing challenges due to the use of different testing environments, with Elara using Hardhat and Compound using a proprietary tool called 'Saddle'. Other projects using Hardhat, such as Orbit Lending, have also not integrated Compound's tests. While Elara's codebase has been reliable in real-world deployments, there is no current test suite, which could lead to small bugs or unexpected behavior. The recommendation is to fork and adapt Compound's test suite and add tests for new features introduced by Elara.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Still working on it. But we have some challenges in Adapting Compound's Test Suite Environment Mismatch: We use Hardhat; Compound uses proprietary 'Saddle'. Direct migration is unfeasible. Industry Norm: Other projects (e.g., Orbit Lending) using Hardhat also haven't integrated Compound's tests. Proven Stability: Elara's codebase has demonstrated reliability through real-world deployments.

**Description:** Even though Elara is initially a Compound Fork that has been battle-tested throughout the years, there are some changes made that require testing to ensure the correct behavior of the system. Currently, there is no test suite, and small bugs or unexpected behavior could still be present in the codebase.

**Recommendation:** We recommend forking and adapting the test suite from Compound and improving on that by including tests that cover the new features introduced by Elara.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Elara Finance |
| Report Date | N/A |
| Finders | Gereon Mendler, Julio Aguilar, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/elara-finance/ceaf2e43-2883-4f4f-bd80-20dc354abb46/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/elara-finance/ceaf2e43-2883-4f4f-bd80-20dc354abb46/index.html

### Keywords for Search

`vulnerability`

