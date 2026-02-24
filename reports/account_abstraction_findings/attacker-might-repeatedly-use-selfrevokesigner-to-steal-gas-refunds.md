---
# Core Classification
protocol: Ondefy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40377
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/4ff1e282-3e2e-4ebb-8476-68fe28aa0eee
source_link: https://cdn.cantina.xyz/reports/cantina_zyfi_jun2024.pdf
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
finders_count: 2
finders:
  - chris
  - deadrosesxyz
---

## Vulnerability Title

Attacker might repeatedly use selfRevokeSigner to steal gas refunds 

### Overview


The bug report is about a function called selfRevokeSigner in a file called PermissionlessPaymaster.sol. The function currently sets a variable called previousManager to the currently set manager of the signer. However, if a certain condition is met, this can lead to a security vulnerability where an attacker can steal all gas refunds. The recommendation is to not change the previousManager variable within the selfRevokeSigner function. The bug has been fixed in a pull request and is considered to have a low risk.

### Original Finding Content

## Vulnerability Report: PermissionlessPaymaster.sol

## Context
- **File:** PermissionlessPaymaster.sol
- **Line:** 377

## Description
Currently, the `selfRevokeSigner` function sets `previousManager` to the signer's currently set manager.

```solidity
function selfRevokeSigner() public {
    previousManager = managers[msg.sender];
    managers[msg.sender] = address(0);
    emit SignerRevoked(previousManager, msg.sender);
}
```

In case `updateRefund` hasn't been called since the last refund, this would lead to distributing the refund to the just revoked manager (instead of the actual `previousManager`). An attacker can utilize this and back-run all transactions that utilize the Paymaster and ultimately steal all gas refunds.

## Recommendation
Do not change `previousManager` within `selfRevokeSigner`.

## Status
- **Zyfi:** Fixed in PR 1.
- **Cantina Managed:** Fix looks good. `previousManager` is no longer changed within `selfRevokeSigner`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Ondefy |
| Report Date | N/A |
| Finders | chris, deadrosesxyz |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_zyfi_jun2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/4ff1e282-3e2e-4ebb-8476-68fe28aa0eee

### Keywords for Search

`vulnerability`

