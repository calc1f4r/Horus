---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42068
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/4c6155c1-8c90-4b47-a8b5-ad2b40128b5b
source_link: https://cdn.cantina.xyz/reports/cantina_rhinestone_smartsessions_core_aug2024.pdf
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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Chinmay Farkya
  - Riley Holterhus
  - Blockdev
---

## Vulnerability Title

Uninstalling the fallback submodule of SmartSession will break the whole validation pro- cess 

### Overview


The SmartSessionBase.sol file has a problem where it can serve as both a "validator" for a smart account and a fallback handler for a specific function. However, this causes compatibility issues with some smart wallet providers like Biconomy. When trying to uninstall the fallback handler part, it completely wipes out the session storage and breaks the validation process. The recommendation is to move the fallback handler to a separate submodule and make it an optional feature to ensure compatibility with all wallet providers. This issue has been fixed in PR 64 and has been verified by Cantina Managed.

### Original Finding Content

## SmartSession Issues and Recommendations

## Context
- **SmartSessionBase.sol**: Lines 282-287, 300-307

## Description
The SmartSession can behave as a multi-type module, serving as the "validator" for a smart account while also acting as a fallback handler for `supportsNestedTypedDataSign()` callbacks. 

Since the usage of ERC7739 requires the smart account to have a fallback to expose a `supportsNestedTypedDataSign` view function, the same SmartSession module can be used as a fallback handler for this method by installing it on the smart account. 

However, the current implementation breaks compatibility with some smart wallet providers, such as Biconomy. 

For Biconomy's nexus smart account, as seen in **ModuleManager.sol#L346**, whenever any component (validator, fallback handler, etc.) is removed from the account, `onUninstall` is called on the module address. It is expected that the module will distinguish which part of the multi-type module is being uninstalled.

Unfortunately, the SmartSession module lacks the logic to specifically uninstall the fallback submodule when the smart account wants to remove it as a fallback handler while continuing to use it as a validator. When `SmartSessionBase::onUninstall()` is invoked, it completely wipes out the session storage. 

As a result, a smart account attempting to uninstall only the fallback handler portion of the SmartSession module breaks the entire session and validation operations thereafter.

## Recommendation
To ensure compatibility with all wallet providers, it is recommended to move the fallback handler part to an independent submodule and make it an optional feature.

## Rhinestone
- **Status**: Fixed in PR 64.

## Cantina Managed
- **Status**: Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | Chinmay Farkya, Riley Holterhus, Blockdev |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_rhinestone_smartsessions_core_aug2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/4c6155c1-8c90-4b47-a8b5-ad2b40128b5b

### Keywords for Search

`vulnerability`

