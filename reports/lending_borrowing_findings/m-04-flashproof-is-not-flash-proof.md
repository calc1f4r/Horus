---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42164
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-04-vader
source_link: https://code4rena.com/reports/2021-04-vader
github_link: https://github.com/code-423n4/2021-04-vader-findings/issues/218

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
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-04] `flashProof` is not flash-proof

### Overview


The `flashProof` modifier is not working properly and does not prevent flash loan attacks as intended. It only checks for the `tx.origin` address, which can be bypassed by miners using different addresses in the same block. This defeats the purpose of the modifier and it is recommended to apply it to individual user addresses instead. It is also debatable if adding flash loan prevention logic is necessary since similar attacks can also be carried out by whales. The team has acknowledged the issue and will make changes to the modifier in the future. 

### Original Finding Content


The `flashProof` modifier is supposed to prevent flash-loan attacks by disallowing performing several sensitive functions in the same block.

However, it performs this check on `tx.origin` and not on an individual user address basis. This only prevents flash loan attacks from happening within a single transaction.

But flash loan attacks are theoretically not limited to the same transaction but to the same block as miners have full control of the block and include several vulnerable transactions back to back. (Think transaction _bundles_ similar to flashbot bundles that most mining pools currently offer.)

A miner can deploy a proxy smart contract relaying all contract calls and call it from a different EOA each time bypassing the `tx.origin` restriction.

The `flashProof` modifier does not serve its purpose.

Recommend trying to apply the modifier to individual addresses that interact with the protocol instead of `tx.origin`.

Furthermore, attacks possible with flash loans are usually also possible for whales, making it debatable if adding flash-loan prevention logic is a good practice.

**[strictly-scarce (vader) confirmed](https://github.com/code-423n4/2021-04-vader-findings/issues/218#issuecomment-830616044):**
 > Flash loans with the help of miners *was not intended to be countered*, although a check for `msg.sender` AND `tx.origin` will be applied.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-vader
- **GitHub**: https://github.com/code-423n4/2021-04-vader-findings/issues/218
- **Contest**: https://code4rena.com/reports/2021-04-vader

### Keywords for Search

`vulnerability`

