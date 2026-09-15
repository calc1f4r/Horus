---
# Core Classification
protocol: Biconomy Nexus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43820
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 7
finders:
  - Blockdev
  - Devtooligan
  - Chinmay Farkya
  - Christoph Michel
  - Víctor Martínez
---

## Vulnerability Title

Missing call type validation in _installFallbackHandler

### Overview


The bug report is about a medium risk issue in the ModuleManager contract. The problem occurs when installing a fallback handler without checking the call type, resulting in a successful installation but the fallback not working when called. This could have serious consequences for integrators and may not be immediately caught due to lack of error messages. The recommendation is to add a check for the call type in the installation process and update the fallback function to revert if neither call type is called. The issue has been fixed by Biconomy and Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
ModuleManager.sol#L281

## Description
When installing a fallback handler, there is no check that the call type is either `CALLTYPE_STATIC` or `CALLTYPE_SINGLE`. This will result in a successful installation including completion of the initialization steps. However, when the fallback is called, nothing will happen when the selector for the fallback handler is passed. Additionally, the fallback does not revert in this case. This could have a serious effect on an integrator depending on the fallback and it may not be caught immediately due to lack of reverting.

## Recommendation
Add a check in `_installFallbackHandler`:

```solidity
require(calltype == CALLTYPE_SINGLE || calltype == CALLTYPE_STATIC, "Invalid CallType");
```

Also consider updating `fallback()` to revert if neither call type is called:

```solidity
returndatacopy(0, 0, returndatasize());
return(0, returndatasize());
}
```

- }
- if (calltype == CALLTYPE_SINGLE) {
+ } else if (calltype == CALLTYPE_SINGLE) {
assembly {
    calldatacopy(0, 0, calldatasize());
    returndatacopy(0, 0, returndatasize());
    return(0, returndatasize());
}
+ } else {
    revert UnsupportedCallType();
}

## Biconomy
Fixed. See files `ModuleManager.sol#L305` and `ModuleManager.sol#L129`.

## Spearbit
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Biconomy Nexus |
| Report Date | N/A |
| Finders | Blockdev, Devtooligan, Chinmay Farkya, Christoph Michel, Víctor Martínez, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

