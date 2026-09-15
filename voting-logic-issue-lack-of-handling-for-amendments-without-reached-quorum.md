---
# Core Classification
protocol: MetaLeX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43855
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/MetaVesT/README.md#2-voting-logic-issue-lack-of-handling-for-amendments-without-reached-quorum
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

Voting Logic Issue: Lack of Handling for Amendments without Reached Quorum

### Overview


The MetaVesTController contract has a bug in the `voteOnMetaVesTAmendment` function. If the amendment does not reach the required quorum within one week, the associated set becomes locked, preventing any future changes. This is a serious issue as it can cause disruptions in decision-making. To fix this, the voting logic should be updated to allow for the removal or cancellation of amendments that do not meet the quorum requirement within the specified timeframe.

### Original Finding Content

##### Description
This issue has been identified in the `voteOnMetaVesTAmendment` function of the [MetaVesTController](https://github.com/MetaLex-Tech/MetaVesT/blob/b614405e60bce8b852e46d06c03fd47b04d86dde/src/MetaVesTController.sol#L598-L618) contract.
Currently, if the voting period for an amendment extends beyond the allowed one-week timeframe without reaching the required quorum, the associated set becomes locked. This situation prevents any further changes, such as adding or removing grants, deleting the set, or proposing a new amendment, effectively blocking future governance actions for that set.
The issue is classified as **High** severity because it can lead to governance gridlock and prevent the proper functioning of the contract's voting mechanism, causing potential disruptions in decision-making.
##### Recommendation
We recommend updating the voting logic to include a mechanism that allows for the removal or cancellation of amendments for which the quorum was not reached within the specified timeframe. This change would ensure that sets do not become permanently blocked due to unmet quorum requirements.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | MetaLeX |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/MetaVesT/README.md#2-voting-logic-issue-lack-of-handling-for-amendments-without-reached-quorum
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

