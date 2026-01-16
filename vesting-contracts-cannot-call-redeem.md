---
# Core Classification
protocol: The Graph Timeline Aggregation Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32999
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/thegraph-timeline-aggregation-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Vesting Contracts Cannot Call redeem

### Overview


This bug report discusses an issue with The Graph's protocol where certain users who participate through a vesting contract are unable to call the "redeem" function in the Escrow contract. This is because the function is restricted to only approved addresses by The Graph. The suggested solution is to use the "getAllocation" function in the Staking contract to derive the Indexer address instead of using the "msg.sender" address. This would allow vesting contracts to call the "redeem" function without needing approval from The Graph. The issue has been resolved in a pull request by The Graph's core developers.

### Original Finding Content

Certain users participate in The Graph's protocol via [a vesting contract](https://github.com/graphprotocol/token-distribution/tree/main), which enables them to be awarded GRT over a period of time and still utilize the tokens for staking, curating, and delegating. In order to prevent the awarded GRT from escaping the vesting lock before the end of the vesting period, the smart contract restricts function calls and function call targets to only those approved by The Graph. Therefore, Indexers that are vesting contracts would initially be unable to call `[redeem](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/blob/d8795c747d44da90f7717b3db9a08698e64a9b2f/src/Escrow.sol#L366)` in the `Escrow` contract until the function signature and address are approved by The Graph. This is because the `redeem` function's logic currently calculates the amount of GRT rewards to forward to the `Staking` contract from the [caller of the function](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/blob/d8795c747d44da90f7717b3db9a08698e64a9b2f/src/Escrow.sol#L377-L384).


Consider deriving the Indexer address to pull GRT from via the `getAllocation` function in the `Staking` contract instead of using the `msg.sender` as the expected address in the `redeem` function. This allows an Indexer who is also a vesting contract to use a separate caller to call the `redeem` function and still get the correct amount of GRT rewards without having to approve the `redeem` function signature for all vesting contracts.


***Update:****Resolved in* [*pull request #58*](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/pull/58)*. The Graph*'s core developers* stated:*



> *This issue is fixed with the same solution as C-01, linking it to the same pull request. The associated issue can be found [here](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/issues/34).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | The Graph Timeline Aggregation Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/thegraph-timeline-aggregation-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

