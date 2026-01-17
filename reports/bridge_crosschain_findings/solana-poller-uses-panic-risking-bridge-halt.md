---
# Core Classification
protocol: Off-chain (Bridge) Full Re-Assessment
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51762
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/RuneMine/off-chain-bridge-full-re-assessment
source_link: https://www.halborn.com/audits/RuneMine/off-chain-bridge-full-re-assessment
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
  - Halborn
---

## Vulnerability Title

Solana Poller Uses Panic, Risking Bridge Halt

### Overview


The Solana poller currently uses panic for error handling in multiple places, which can cause the entire bridge process to stop working if a single error occurs. This is due to the use of a function that panics on error, direct use of panic, and lack of a panic recovery mechanism. This can lead to goroutine leaks and partial system failure. The RuneMine team has accepted the risk of this issue.

### Original Finding Content

##### Description

The current implementation of the Solana poller uses panic for error handling in several places. This approach can cause the entire bridge process to halt when a single error occurs.  
  
Problematic Code Example  
  
1. In the poll function:  
  
  
`util.Check(err) // This function panics on error`  
  
2. Direct use of panic:  
  
  
`if fee < 50000000 {  
panic(fmt.Sprintf("sol fee paid to small to cover transaction cost: %d", fee))  
}`  
  
  
3. In utility functions:  
  
  
`func Check(err error) {  
if err != nil {  
panic(err)  
}  
}`

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:M/D:M/Y:N/R:N/S:C (7.8)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:M/D:M/Y:N/R:N/S:C)

##### Recommendation

There's no visible panic recovery mechanism in the main function to catch panics from goroutines. This could lead to goroutine leaks and partial system failure.

##### Remediation

**RISK ACCEPTED:** The **RuneMine team** accepted the risk of the issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Off-chain (Bridge) Full Re-Assessment |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/RuneMine/off-chain-bridge-full-re-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/RuneMine/off-chain-bridge-full-re-assessment

### Keywords for Search

`vulnerability`

