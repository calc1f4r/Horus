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
solodit_id: 28344
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/WstETH/README.md#5-incorrect-burning-of-shares
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

Incorrect burning of shares

### Overview


This bug report is about a potential issue with the Lido contract, which is a decentralized finance (DeFi) platform. The issue is that when a user attempts to burn shares in the WstETH contract from the stETH contract, it can lead to a block on the unwrap function. This could cause problems for users, as they would be unable to access their funds.

To address this issue, the report recommends adding a check to the Lido contract, so that the Burner cannot burn shares for WstETH. This would prevent the issue from occurring and ensure that users can access their funds as expected.

Overall, this bug report highlights a potential issue with the Lido contract, and suggests a solution in the form of adding a check to the contract. This would prevent the issue from occurring and ensure that users can access their funds without any problems.

### Original Finding Content

##### Description
Burning of shares for `WstETH` contract from `stETH` contract can lead to block `unwrap` function for users:
https://github.com/lidofinance/lido-dao/tree/ea6fa222004b88e6a24b566a51e5b56b0079272d/contracts/0.6.12/WstETH.sol#L69-L75
##### Recommendation
We recommend to add a check to `Lido` contract, that Burner can't burn shares for `WstETH`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/WstETH/README.md#5-incorrect-burning-of-shares
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

