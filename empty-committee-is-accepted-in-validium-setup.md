---
# Core Classification
protocol: Polygon zkEVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53612
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/polygon/Sigma_Prime_Polygon_LXLY_Bridge_Security_Assessment_Report_v2_1.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/polygon/Sigma_Prime_Polygon_LXLY_Bridge_Security_Assessment_Report_v2_1.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Empty Committee Is Accepted In Validium Setup

### Overview


The `setupCommittee()` function in Validium allows for the creation of a signing committee, but due to a lack of input validation, it is possible to register an empty committee. This means that any sequenced batches will pass the Validium signature checks without the need for a committee to sign the message. To prevent this issue, the function should include a check that the committee has at least one member. However, the development team has decided to keep the code as is, as it is a desired feature. It is recommended to use timelocks and multisig contracts as access control for `setupCommittee()` to reduce the likelihood of setting incorrect parameters. 

### Original Finding Content

## Description

Setting up the Validium rollup signing committee is achieved by calling `setupCommittee()`. Due to a lack of input validation, it is possible to register an empty committee.

An empty committee occurs when the following parameters are submitted:
- `_requiredAmountOfSignatures = 0`
- `urls.length = 0`
- `addrsBytes.length = 0`

Any existing members will be removed, and no new members are added. The result is that any sequenced batches will pass the Validium signatures checks without the need for a committee to sign the message.

The issue may be exploited since `CDKDataCommittee.verifySignatures()` is called with `requiredAmountOfSignatures = 0`. Thus, passing an empty `signaturesAndAddrs` will successfully verify the `signedHash`.

## Recommendations

When setting up a signing committee, `setupCommittee()` should include a check that `membersLength` is non-zero to prevent deleting the existing committee and the use of an empty committee.

## Resolution

The development team is aware of this use case and has chosen to leave the code as is since it is a desirable feature. To ensure the update function is called with the correct parameters, additional comments have been added to `setupCommittee()` as follows.

It is advised to use timelocks for the admin address in case of Validium since it can change the `dataAvailabilityProtocol`. By using a timelock and multisig contract as access control for `setupCommittee()`, the likelihood of setting incorrect parameters is significantly reduced.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Polygon zkEVM |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/polygon/Sigma_Prime_Polygon_LXLY_Bridge_Security_Assessment_Report_v2_1.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/polygon/Sigma_Prime_Polygon_LXLY_Bridge_Security_Assessment_Report_v2_1.pdf

### Keywords for Search

`vulnerability`

