---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29427
audit_firm: Oxorio
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2023-10-18-Lido.md
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
  - Oxorio
---

## Vulnerability Title

[FIXED] Missing zero address validation for recepient leads to possible loss of fund in `TopUpAllowedRecipients`

### Overview

See description below for full details.

### Original Finding Content

##### Location
File | Location | Line
--- | --- | ---
[TopUpAllowedRecipients.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L97 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol") | contract `TopUpAllowedRecipients` > function `createEVMScript` | 97
[TopUpAllowedRecipients.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L135 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol") | contract `TopUpAllowedRecipients` > function `_validateEVMScriptCallData` | 135

##### Description
In the function [`createEVMScript`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L97 ), the function [`_validateEVMScriptCallData`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L135) in the `TopUpAllowedRecipients` contract does not validate the recipients from the calldata array for zero address. While the funds can only be sent to allowed recipient addresses, which are validated through the `AllowedRecipientsRegistry` contract (out of scope), the `addRecipient` function of the contract allows adding a zero address as a recipient of the funds.
##### Recommendation
We recommend adding zero-address validation for the recipients' addresses. This will ensure that only valid addresses are allowed to receive funds, preventing potential issues or misuse of funds.
##### Update
Fixed in the commit [`f4efe8e49aa23fe4f1f161386b750659100f39d7`](https://github.com/lidofinance/easy-track/tree/f4efe8e49aa23fe4f1f161386b750659100f39d7/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L137).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Oxorio |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Oxorio |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2023-10-18-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

