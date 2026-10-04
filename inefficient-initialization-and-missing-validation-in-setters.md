---
# Core Classification
protocol: Internal Exchange Re-Assessment
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52046
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/dappos/internal-exchange-re-assessment
source_link: https://www.halborn.com/audits/dappos/internal-exchange-re-assessment
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Inefficient Initialization and Missing Validation in Setters

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `OrderBookVault` contract includes separate setter functions, such as `setOrderBook` and `setOrderBookConfig`, to configure its dependencies. However, these could be directly initialized in the `initialize` function to streamline the deployment process and reduce operational overhead. Additionally, these setters lack validation checks, such as verifying that the provided addresses are not zero or ensuring compliance with ERC165 standards. This could result in misconfiguration or interaction with incompatible contracts, potentially leading to runtime errors.

##### BVSS

[AO:S/AC:L/AX:L/C:N/I:L/A:N/D:N/Y:N/R:N/S:C (0.6)](/bvss?q=AO:S/AC:L/AX:L/C:N/I:L/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

Combine the configuration of `OrderBook` and `OrderBookConfig` into the `initialize` function to simplify contract setup and improve deployment efficiency. Add validation checks in the setters to ensure the provided addresses are non-zero and compatible with the expected interfaces. For instance, use `Address.isContract()` to confirm the addresses are contracts and verify ERC165 compliance using `IERC165.supportsInterface`.

##### Remediation

**ACKNOWLEDGED:** The **dappOS team** acknowledged this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Internal Exchange Re-Assessment |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/dappos/internal-exchange-re-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/dappos/internal-exchange-re-assessment

### Keywords for Search

`vulnerability`

