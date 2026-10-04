---
# Core Classification
protocol: Kakeru Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51819
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/kakeru/kakeru-contracts
source_link: https://www.halborn.com/audits/kakeru/kakeru-contracts
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
  - Halborn
---

## Vulnerability Title

Missing slashing check

### Overview


The `execute_burn` function in the `basset_inj_token_binj` contract does not correctly update the exchange rate in the `basset_inj_hub` contract. This is because it does not call the `CheckSlashing` entry point in the `hub` contract like all other Burn calls. This leads to an incorrect State value in the Hub contract. The BVSS score for this issue is 5.0, which is a moderate risk. The recommended solution is to add the `CheckSlashing` call in the `execute_burn` function to keep the exchange rate updated after modifying the `total_supply` of the token. The Kakeru team has stated that this is expected behavior and no remediation plan is necessary.

### Original Finding Content

##### Description

The `execute_burn` function from the **basset\_inj\_token\_binj** contract does not call the `CheckSlashing`entry point of the **basset\_inj\_hub contract** like all other Burn calls, leading to an incorrect **State** value in the **Hub** contract.

![execute_burn function](https://halbornmainframe.com/proxy/audits/images/660bd1a453b13d194e0edd43)![execute_burn_from function](https://halbornmainframe.com/proxy/audits/images/660bd18153b13d194e0edd3f)

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:M/R:N/S:U (5.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:M/R:N/S:U)

##### Recommendation

It is recommended to add the `CheckSlashing` call to the **Hub** contract in the `execute_burn` function to keep the **binj** exchange rate updated after modifying the `total_supply` of the token.

Remediation Plan
----------------

**NOT APPLICABLE**: The `Kakeru team` have explained that this is the expected behavior:

*The* `execute_burn` *function can only be called by the hub contract and does not require checkSlashing to change the exchange rate, which remains unchanged. The* `execute_burn_from` *function will destroy bINJ but does not initiate the unbond operation, so no INJ will be obtained. In this case, checkSlashing will distribute the excess INJ to all bINJ holders.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Kakeru Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/kakeru/kakeru-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/kakeru/kakeru-contracts

### Keywords for Search

`vulnerability`

