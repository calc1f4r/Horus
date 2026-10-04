---
# Core Classification
protocol: Neptune Mutual Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10493
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/neptune-mutual-audit/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.40
financial_impact: high

# Scoring
quality_score: 2
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - launchpad
  - rwa
  - insurance
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Risk of insufficient liquidity

### Overview


A bug was identified in the Neptune Mutual Protocol, which is responsible for ensuring that enough funds are available when a cover is purchased. The protocol was counting the existing commitments, but only included covers expiring in the next three months, as this is the maximum policy duration. However, some covers may expire in the fourth month and these would be excluded from the calculation. This could lead to the protocol selling more insurance than it can support, and some valid claimants may be unable to retrieve their payment.

To address this, it was suggested to include the extra month in the commitment computation. This bug has now been fixed and the fix can be found in commit `63fce22c67f72cf090ffa124784a3d92935e2d66` in pull request #136.

### Original Finding Content

When purchasing a cover, the protocol [ensures it has enough funds](https://github.com/neptune-mutual-blue/protocol/blob/73fc82fbe0d1388867b7df669983fe42760daeb1/contracts/libraries/PolicyHelperV1.sol#L50) to pay out all potential claimants. The computation of the [existing commitments](https://github.com/neptune-mutual-blue/protocol/blob/73fc82fbe0d1388867b7df669983fe42760daeb1/contracts/libraries/CoverUtilV1.sol#L477-L481) includes all covers expiring in the next 3 months, since this is the [maximum policy duration](https://github.com/neptune-mutual-blue/protocol/blob/133bc8a4157d4f27471b0cf43ac0ce2b51bb5e5a/contracts/libraries/ProtoUtilV1.sol#L14). However, some covers may expire [in the fourth month](https://github.com/neptune-mutual-blue/protocol/blob/73fc82fbe0d1388867b7df669983fe42760daeb1/contracts/libraries/CoverUtilV1.sol#L609) and these would be excluded from the calculation. Therefore, the protocol could sell more insurance than it can support, and some valid claimants may be unable to retrieve their payment.


Consider including the extra month in the commitment computation.


**Update:** *Fixed as of commit `63fce22c67f72cf090ffa124784a3d92935e2d66` in [pull request #136](https://github.com/neptune-mutual-blue/protocol/pull/136).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 2/5 |
| Rarity Score | 4/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Neptune Mutual Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/neptune-mutual-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

