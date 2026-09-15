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
solodit_id: 41217
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#5-bond-curve-is-not-reset-inside-the-submitinitialslashing-function
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

Bond Curve is Not Reset Inside the `submitInitialSlashing` Function

### Overview


The report describes a bug in the `submitInitialSlashing` function of the `CSModule` contract. This bug causes the bond curve for a Node Operator to not be reset to the default after being penalized. This could lead to incorrect counting of unbonded validator keys. The severity of this bug is classified as medium. The recommendation is to reset the bond curve for the Node Operator during the penalization event.

### Original Finding Content

##### Description
The issue is identified within the [`submitInitialSlashing`](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSModule.sol#L1174) function of the `CSModule` contract, where the initial slashing penalty is applied to the Node Operator bond. While this penalization occurs, the Bond Curve for that Node Operator is not reset to the default.

The issue is classified as **Medium** severity because it may lead to incorrect accounting of the unbonded validator keys count after the Node Operator penalization.

##### Recommendation
We recommend resetting the Node Operator bond curve during the mentioned penalization event via a call to `accounting.resetBondCurve(nodeOperatorId)`.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#5-bond-curve-is-not-reset-inside-the-submitinitialslashing-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

