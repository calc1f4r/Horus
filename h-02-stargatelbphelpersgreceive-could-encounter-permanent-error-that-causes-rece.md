---
# Core Classification
protocol: Tapiocadao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31433
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-02] `StargateLbpHelper.sgReceive()` could encounter permanent error that causes received tokens to be stuck in contract

### Overview


Severity: High
Impact: Tokens may become stuck in contract
Likelihood: Medium, only occurs for permanent errors

Description:
The StargateLbpHelper.sgReceive() function is responsible for receiving tokens sent across chains through Stargate swap and swapping them through the LBP pool. This function has a retryRevert() feature that allows the owner to retry the swap if it fails. However, if the failure is caused by a permanent error, the retryRevert() feature will not be able to recover the tokens. This means that the tokens will be stuck in the StargateLbpHelper contract and cannot be retrieved.

Recommendations:
To prevent tokens from becoming stuck in the contract, it is recommended to either allow the token recipient to retrieve the tokens or automatically transfer them to the recipient when a permanent error occurs. 

### Original Finding Content

**Severity**

**Impact:** High, as tokens will be stuck in contract

**Likelihood:** Medium, as it only occur for permanent errors

**Description**

`StargateLbpHelper.sgReceive()` receives tokens that are sent across chains via Stargate swap, and then swaps them via LBP pool. `StargateLbpHelper` has a `retryRevert()` to allow the owner to retry the execution on stargate swap failure.

However, if the failure is due to a permanent error, `retryRevert()` will not help with the recovery. When that happens, the tokens received will be stuck in the `StargateLbpHelper` contract, with no means to retrieve them.

**Recommendations**

Either allow token recipient to retrieve the tokens or transfer to recipient when such a permanent error occurs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tapiocadao |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

