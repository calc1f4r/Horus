---
# Core Classification
protocol: Alchemy Modular Account
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59702
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/alchemy-modular-account/2c13aab2-5d5f-4f45-a9ef-b890bdb12b97/index.html
source_link: https://certificate.quantstamp.com/full/alchemy-modular-account/2c13aab2-5d5f-4f45-a9ef-b890bdb12b97/index.html
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
finders_count: 4
finders:
  - Shih-Hung Wang
  - Nikita Belenkov
  - Ruben Koch
  - Alejandro Padilla
---

## Vulnerability Title

Missing Validation for Execution Function in `SessionKeyPermissionsPlugin` Hooks

### Overview

See description below for full details.

### Original Finding Content

**Update**
A selector check has been added as recommended. Fixed in commits `540b0e3884d1f3a315c4f9046c3af25b5d21fd76` and `617677a0703da3107e5980c89162eb510254ae16`.

![Image 73: Alert icon](https://certificate.quantstamp.com/full/alchemy-modular-account/2c13aab2-5d5f-4f45-a9ef-b890bdb12b97/static/media/info-icon-alert.3c9578483b1cf3181c9bfb6fec7dc641.svg)

**Update**
For the second part of our recommendation, the client responded: "If a plugin is authorized to call executeWithSessionKey, therefore passes the validations and hook checks, then updating limit for the session key is fine. No fix needed here."

**File(s) affected:**`plugins/session/permissions/SessionKeyPermissionsPlugin.sol`

**Description:** The pre-execution hook defined by `SessionKeyPermissionsPlugin` updates the spending limit of a session key according to the provided call data. However, it does not validate that the selector (the first 4 bytes of the calldata) is exactly `executeWithSessionKey.selector`.

Since a plugin can reuse another plugin's hook (by specifying it in the manifest or by injected hooks), if a plugin adds the pre-hook from `SessionKeyPermissionsPlugin` to a random execution function, whenever that function is executed, the pre-hook is executed as well. This can cause an issue as the pre-hook is designed to be applied only to the `executeWithSessionKey()` function. Otherwise, the spending limit of a session key may be reduced without the user actually spending any token or gas.

**Recommendation:** Generally, hooks should validate the function selector in the provided call data to ensure that it is applied on an execution function that the hook recognizes and reverts the transaction if not.

Consider checking whether the function selector is `executeWithSessionKey.selector` at the beginning of the `_updateLimitsPreExec()` function to avoid another plugin triggering the call to the pre-hook either accidentally or intendedly. For the same reason, the `_checkUserOpPermissions()` function should validate the function selector (i.e., `userOp.callData[:4]`) as well.

However, even if the function selector is validated in the pre-execution hook, the plugin still cannot ensure that the hook is not triggered by a random plugin via the `executeFromPlugin()` call. Checking whether the sender supports the `IPlugin` interface does not fully solve the issue since the sender can manipulate the return values of the `supportsInterface()` call. A possible mitigation is to add a flag that indicates whether the call to the hook is triggered via `executeFromPlugin()` or not.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Alchemy Modular Account |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Nikita Belenkov, Ruben Koch, Alejandro Padilla |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/alchemy-modular-account/2c13aab2-5d5f-4f45-a9ef-b890bdb12b97/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/alchemy-modular-account/2c13aab2-5d5f-4f45-a9ef-b890bdb12b97/index.html

### Keywords for Search

`vulnerability`

