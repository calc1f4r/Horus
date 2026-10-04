---
# Core Classification
protocol: Tezos Etherlink
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41960
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Tezos-Spearbit-Security-Review-September-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Tezos-Spearbit-Security-Review-September-2024.pdf
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
  - Lukasz Glen
  - Wei Tang
---

## Vulnerability Title

Call of FA bridge proxy contract not respecting the depth limit

### Overview


This bug report discusses an issue with the Tezos blockchain platform, specifically with the handler.execute_call function. This function is responsible for executing proxy contracts, but it does not properly enforce a limit on the depth of the call stack. This means that there is a risk of the call stack becoming too large, which could potentially cause problems with the execution of contracts. The recommendation is to create a new "transaction data" layer and enforce the call stack depth limit in order to prevent this issue. This bug has been addressed and fixed in the Spearbit platform.

### Original Finding Content

Severity: Medium Risk
Context: handler.execute_call
Description: After inner_execute_proxy , handler.execute_call takes over and starts to execute the proxy
contract. It notes the call stack depth but does not enforce it.
Recommendation: Properly create a new "transaction data" layer and enforce the call stack depth limit.
Tezos: See MR 15358 where a check was added for call stack before creating a new transaction data layer.
Spearbit: Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Tezos Etherlink |
| Report Date | N/A |
| Finders | Lukasz Glen, Wei Tang |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Tezos-Spearbit-Security-Review-September-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Tezos-Spearbit-Security-Review-September-2024.pdf

### Keywords for Search

`vulnerability`

