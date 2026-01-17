---
# Core Classification
protocol: DIA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55418
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Multi%20Scope/README.md#7-missing-ism-validation-in-requestoraclehandle-and-pushoraclereceiverhandle
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Missing ISM validation in `RequestOracle.handle()` and `PushOracleReceiver.handle()`

### Overview


The bug report identifies a problem in the `handle()` function of `RequestOracle` and `PushOracleReceiver` contracts. The function does not properly verify if the Interchain Security Module (ISM) has been configured, which could allow an attacker to send unauthorized messages from DIA chain. The severity of the issue is classified as Medium because it only occurs when the ISM is not set. The recommendation is to add a check in the `handle()` function to ensure the ISM is not set to `address(0)`.

### Original Finding Content

##### Description
This issue has been identified within the `handle()` function of `RequestOracle` and `PushOracleReceiver`  contracts.

The `handle()` function only validates that the message sender is the trusted mailbox but does not verify if the Interchain Security Module has been properly configured. If the ISM is not set via `setInterchainSecurityModule()`, Hyperlane will use default ISM which does not validate the origin of messages.

This vulnerability could allow an attacker to send unauthorized messages from DIA chain, potentially leading to manipulation of oracle data.

The issue is classified as Medium severity because it requires specific conditions when ISM wasn't set.

##### Recommendation
We recommend adding a check in the `handle()` function to ensure ISM is not `address(0)`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Multi%20Scope/README.md#7-missing-ism-validation-in-requestoraclehandle-and-pushoraclereceiverhandle
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

