---
# Core Classification
protocol: Sablier
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54674
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/5febedab-9e34-4943-bdd3-891559384740
source_link: https://cdn.cantina.xyz/reports/cantina_sablier_jul2023.pdf
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
finders_count: 2
finders:
  - Zach Obront
  - RustyRabbit
---

## Vulnerability Title

Token allowances stay in effect on proxy ownership transfer 

### Overview


This bug report discusses a security issue in the proxy contract, which is a smart contract wallet for its owner. The problem arises when the ownership of the proxy is transferred to someone else, as the existing approvals for other contracts on ERC20 tokens remain in effect. This means that the previous owner could potentially steal tokens using these approvals without the new owner's knowledge. The report recommends reconsidering the ownership transfer use case and mentions that the issue has been fixed in the Sablier and Cantina contracts. 

### Original Finding Content

## Security Context and Recommendations

## Context
- **File Location:** `/prb-proxy/src/PRBProxy.sol#L121-L129`

## Description
The proxy contract acts as a smart contract wallet for its owner, and it is a reasonable scenario that the proxy will, at some point, have (infinite) approvals set for other contracts on some ERC20 tokens.

When the ownership of a proxy, for some reason, is transferred to another entity (either a person or contracts as part of a protocol), the existing approvals stay in effect as they are based on the proxy's address. In such a scenario, the new owner (if a person) is unaware of the existing approvals, and this could allow the old owner to use those approvals to potentially steal the tokens via the approved contracts.

Note that this is also true for approvals on the permit2 contract, although they have an expiration and in the case of AllowanceTransfer, approvals are reset with each new approval.

## Recommendation
Reconsider the proxy ownership transfer use case, as many external contracts depend on the address as an indication of ownership and access control.

## Fixes
- **Sablier:** Fixed with the inclusion of `07fed42`, which resets all the constructor parameters in `_deploy`.
- **Cantina:** Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sablier |
| Report Date | N/A |
| Finders | Zach Obront, RustyRabbit |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sablier_jul2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5febedab-9e34-4943-bdd3-891559384740

### Keywords for Search

`vulnerability`

