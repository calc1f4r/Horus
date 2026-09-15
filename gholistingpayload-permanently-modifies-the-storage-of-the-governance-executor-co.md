---
# Core Classification
protocol: Aave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19179
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-aip/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-aip/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

GhoListingPayload permanently modifies the storage of the governance executor contract

### Overview


The bug report is about the storage of the governance executor contract being affected when executing the GhoListingPayload payload. GhoListingPayload contains two state variables, GHO_TOKEN and GHO_FLASHMINTER, which are modified by the execute() function. When execute() is called in a standard CALL, these values would be stored in the storage of GhoListingPayload itself. However, when executed by DELEGATECALL, the function would modify the storage of the Executor contract, causing unexpected results when the next payload is executed.

The development team's recommendation was to not declare GHO_TOKEN and GHO_FLASHMINTER as state variables, but instead as immutable variables within the constructor. This would allow the values to be calculated at construction time. This recommendation was implemented at 957b050.

### Original Finding Content

## Description

Executing the `GhoListingPayload` payload will change the storage of the governance executor contract, which could affect future payloads. Most of the variables in `GhoListingPayload` are either constant or immutable, which do not affect the contract’s storage.

However, `GhoListingPayload` does contain two state variables: `GHO_TOKEN` and `GHO_FLASHMINTER`. The `execute()` function modifies both of these variables. If `execute()` is called in a standard `CALL`, these values would be stored in the storage of `GhoListingPayload` itself. As it is intended to be called by `DELEGATECALL` when executed, it means that the function would modify the storage of the Executor contract.

This will not prevent `execute()` from functioning properly; however, it will store the values of `GHO_TOKEN` and `GHO_FLASHMINTER` in the first two storage slots of the Executor contract. This creates a permanent hazard. When the next payload is executed and accesses the storage slots of the Executor contract, then it would have unexpected values in those slots, which would produce unexpected results.

## Recommendations

Do not declare `GHO_TOKEN` and `GHO_FLASHMINTER` as state variables. Instead, consider declaring them as immutable variables within the constructor. The values are deterministic and can be calculated at construction time.

## Resolution

The development team implemented the recommendation at commit `957b050`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Aave |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-aip/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-aip/review.pdf

### Keywords for Search

`vulnerability`

