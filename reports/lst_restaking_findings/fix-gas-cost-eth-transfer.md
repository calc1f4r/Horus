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
solodit_id: 28140
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#2-fix-gas-cost-eth-transfer
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
  - MixBytes
---

## Vulnerability Title

Fix gas cost ETH transfer

### Overview


This bug report is about the ETH sending process at a certain line of code in the Lido.sol file. The current gas amount used is 2300, but due to the varying gas price, it is possible that it may exceed the gas limit in the future. The recommendation is to send ETH via call instead.

### Original Finding Content

##### Description
ETH sending at this line 
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.4.24/Lido.sol#L301 
uses 2300 gas amount, but gas price can be vary and it is possible that in future it may exceed gas limit.
##### Recommendation
We recommend sending ETH via call.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#2-fix-gas-cost-eth-transfer
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

