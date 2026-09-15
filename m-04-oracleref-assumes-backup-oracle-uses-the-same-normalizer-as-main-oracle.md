---
# Core Classification
protocol: Volt Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1833
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-volt-protocol-contest
source_link: https://code4rena.com/reports/2022-03-volt
github_link: https://github.com/code-423n4/2022-03-volt-findings/issues/26

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[M-04] `OracleRef` assumes backup oracle uses the same normalizer as main oracle

### Overview


The bug report is about the vulnerability in the 'OracleRef' code on GitHub. The 'OracleRef' code assumes that the backup oracle uses the same normalizer as the main oracle. However, this is not always the case as the backup oracle could be a completely different oracle, not even operated by Chainlink. If the main oracle fails, the backup oracle could be scaled by a wrong amount and return a wrong price, which could lead to users being able to mint volt cheap or redeem volt for inflated underlying amounts. To mitigate this issue, it is recommended that there should be two scaling factors, one for each oracle.

### Original Finding Content

_Submitted by cmichel_

[OracleRef.sol#L104](https://github.com/code-423n4/2022-03-volt/blob/f1210bf3151095e4d371c9e9d7682d9031860bbd/contracts/refs/OracleRef.sol#L104)<br>

The `OracleRef` assumes that the backup oracle uses the same normalizer as the main oracle.<br>
This generally isn't the case as it could be a completely different oracle, not even operated by Chainlink.<br>

If the main oracle fails, the backup oracle could be scaled by a wrong amount and return a wrong price which could lead to users being able to mint volt cheap or redeem volt for inflated underlying amounts.

### Recommended Mitigation Steps

Should there be two scaling factors, one for each oracle?

**[ElliotFriedman (Volt) confirmed and commented](https://github.com/code-423n4/2022-03-volt-findings/issues/26#issuecomment-1092201320):**
 > This is a good catch as it exposes some underlying assumptions made about backup oracles; however, we can assume that both oracles will use the same scaling factor and thus we will not need a second value for the backup oracle.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Volt Protocol |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-volt
- **GitHub**: https://github.com/code-423n4/2022-03-volt-findings/issues/26
- **Contest**: https://code4rena.com/contests/2022-03-volt-protocol-contest

### Keywords for Search

`vulnerability`

