---
# Core Classification
protocol: Saffron_2025-07-31
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62954
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review_2025-07-31.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-08] Bytecode validation missing for adapter instances

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

When a vault is created via the `createVault` function, the factory verifies that the adapter address provided by the user corresponds to a registered adapter. However, it does **not verify** whether the adapter's associated bytecode (template) is still valid and present in the factory’s `adapterTypeByteCode` mapping.

The system allows the contract owner to "delete" (deactivate) adapter templates by clearing their bytecode from `adapterTypeByteCode`. Nevertheless, a malicious user can pre-deploy multiple adapter instances (using a soon-to-be-deprecated adapter type), and after the bytecode has been deleted by the owner, these instances can still be used for vault creation. This allows the bypassing of owner-intended deactivation of adapter types, leading to the unintended creation of vaults with deprecated adapter logic.

The issue arises from missing logic that should enforce that **only adapter instances with an active (undeleted) adapter type bytecode can be used**.

**Recommendations**

Add a check in the `createVault` function to ensure that the adapter's associated type ID still has valid bytecode in the factory's storage. Specifically:

```solidity
bytes memory adapterBytecode = adapterTypeByteCode[_adapterInfo.adapterTypeId];
require(adapterBytecode.length != 0, "BDE"); // Bytecode Deleted
```

This ensures that even if an adapter instance was deployed prior to bytecode deletion, it cannot be used to create new vaults after its template has been deactivated.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Saffron_2025-07-31 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review_2025-07-31.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

