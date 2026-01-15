---
# Core Classification
protocol: Fantium
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27920
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Fantium/Fantium%20v2/README.md#11-updating-a-token-version-can-cause-a-jump-of-tokens-between-collections
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

Updating a token version can cause a jump of tokens between collections

### Overview


This bug report concerns the FantiumNFTV3 smart contract. It states that one collection can store only 1,000,000 token ids and one version can store a maximum of 10,000 token ids, meaning that a token version can be updated only 100 times. This limit of 100 updates per token is causing tokens to jump to the next collection when the version is updated for the 100th time.

The recommendation is to expand the number of updates for one token without limiting the `maxInvocation` parameter in one collection and to add a check that `tokenVersionUpgrade` doesn't jump between collections. This can be done by following the link provided in the report.

In conclusion, this bug report describes a limit of 100 updates per token that is causing tokens to jump to the next collection when the version is updated for the 100th time. The recommendation is to expand the number of updates for one token and add a check that `tokenVersionUpgrade` doesn't jump between collections.

### Original Finding Content

##### Description
One collection can store only 1_000_000 token ids and one version can store maximum 10_000 of token ids that means a token version can be updated only 100 times. Moreover, updating the token version the 100th time will cause a jump of this token to the next collections.

##### Recommendation
We recommend expanding the number of updates for one token without limiting further the `maxInvocation` parameter in one collection and adding a check that `tokenVersionUpgrade` doesn't jump between collections [here](https://github.com/FantiumAG/smart-contracts/blob/a2d126453c1105028f12277b8f342d2cdbf01a77/contracts/FantiumNFTV3.sol#L812).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Fantium |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Fantium/Fantium%20v2/README.md#11-updating-a-token-version-can-cause-a-jump-of-tokens-between-collections
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

