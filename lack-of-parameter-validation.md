---
# Core Classification
protocol: Caldera
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47469
audit_firm: OtterSec
contest_link: https://www.caldera.xyz/
source_link: https://www.caldera.xyz/
github_link: https://github.com/ConstellationCrypto/celestia-bedrock

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - James Wang
  - Robert Chen
---

## Vulnerability Title

Lack Of Parameter Validation

### Overview

See description below for full details.

### Original Finding Content

## Configuration Check

**Description:**  
Check in node and batcher fails to validate the correctness and consistency of parameters related to data availability to ensure they fall within valid ranges and to confirm their compatibility with other configured components. Any misconfigurations within the Data Availability setup may result in significant consequences for the reliability and performance of both the node and batcher.

## Remediation

Performs sanity checks on the parameters to lower the chances of chain misconfigurations.

---

© 2024 Otter Audits LLC. All Rights Reserved. 9/12

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Caldera |
| Report Date | N/A |
| Finders | James Wang, Robert Chen |

### Source Links

- **Source**: https://www.caldera.xyz/
- **GitHub**: https://github.com/ConstellationCrypto/celestia-bedrock
- **Contest**: https://www.caldera.xyz/

### Keywords for Search

`vulnerability`

