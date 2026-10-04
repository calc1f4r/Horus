---
# Core Classification
protocol: GooseFX v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47706
audit_firm: OtterSec
contest_link: https://www.goosefx.io/
source_link: https://www.goosefx.io/
github_link: https://github.com/GooseFX1/gfx-ssl-v2

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
finders_count: 4
finders:
  - OtterSec
  - Robert Chen
  - Ajay Kunapareddy
  - Thibault Marboud
---

## Vulnerability Title

Missing Checks

### Overview

See description below for full details.

### Original Finding Content

## SSL Pool Configuration Improvements

1. **Add More Validations**  
   Add more validations within `configure` for `SSLMathParams` to guarantee the proper configuration of an `SSLPool`, thus averting the pool setup with inconsistent or invalid parameter values.

2. **Sanity Checks in Pool Registry**  
   `configPoolRegistry` should include sanity checks on `PoolRegistryConfig.MaxPoolTokenRatio` to ensure that the values set for the maximum pool token ratio are valid and within acceptable ranges.

3. **Enforcement of Mint Account Ordering**  
   Currently, there is a lack of enforcement regarding ordering mint accounts in the seed construction for the pair account within `CreatePair`. This absence of ordering constraints may create duplicate pair accounts for the same pair of mints with reversed order. Therefore, enforce a consistent ordering of the mint accounts in the seed construction.

## Remediation  
Ensure to incorporate the checks mentioned above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | GooseFX v2 |
| Report Date | N/A |
| Finders | OtterSec, Robert Chen, Ajay Kunapareddy, Thibault Marboud |

### Source Links

- **Source**: https://www.goosefx.io/
- **GitHub**: https://github.com/GooseFX1/gfx-ssl-v2
- **Contest**: https://www.goosefx.io/

### Keywords for Search

`vulnerability`

