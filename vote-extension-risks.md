---
# Core Classification
protocol: Cosmos SDK
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47515
audit_firm: OtterSec
contest_link: https://cosmos.network/
source_link: https://cosmos.network/
github_link: https://github.com/cosmos/cosmos-sdk

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
finders_count: 3
finders:
  - James Wang
  - Naoya Okanami
  - Tuyết Dương
---

## Vulnerability Title

Vote Extension Risks

### Overview


The bug report discusses an issue with the ValidateVoteExtensions function, which is used in PrepareProposal and ProcessProposal handlers. The function calculates the total voting power based on the sum of the powers of the votes present in the extCommit.Votes variable. However, since proposers can inject any votes, including potentially malicious ones, the calculated total voting power may not accurately represent the true total voting power of the network. This can lead to security vulnerabilities, especially when the vote extensions influence critical decisions such as the value of an oracle. Additionally, the function uses the extCommit.Round value in the construction of CanonicalVoteExtension. If a past round value is injected, validators may incorrectly consider vote extensions from that past round as valid. This can be exploited by a malicious proposer to selectively include advantageous vote extensions from historical rounds, potentially influencing the outcome in their favor. The report suggests implementing additional checks to validate the voting power calculation and ensure that the vote extensions are representative of the entire validator set, rather than controlled by a single entity. It also recommends adding additional validation checks to ensure that the Round value injected by the proposer is not from a past round. The issue has been patched in version 7155a1c.

### Original Finding Content

## ValidateVoteExtensions Overview

`ValidateVoteExtensions`, which is designed for use in `PrepareProposal` and `ProcessProposal` handlers, raises issues on its usage in `ProcessProposal`:

1. The calculation of `totalVP` is based on the sum of the powers of the votes present in `extCommit.Votes`. However, since proposers have the ability to inject any vote set, including potentially malicious ones, the calculated `totalVP` may not accurately represent the true total voting power of the network. This discrepancy can lead to security vulnerabilities, especially when the vote extensions influence critical decisions such as the value of an oracle.

   ```go
   func ValidateVoteExtensions(
       ctx sdk.Context,
       valStore ValidatorStore,
       currentHeight int64,
       chainID string,
       extCommit abci.ExtendedCommitInfo,
   ) error {
       [...]
       for _, vote := range extCommit.Votes {
           totalVP += vote.Validator.Power
           [...]
       }
       [...]
   }
   ```

2. In the construction of `CanonicalVoteExtension`, `ValidateVoteExtensions` uses `extCommit.Round` as the Round value. If a past round value is injected, validators may incorrectly consider vote extensions from that past round as valid. By injecting a past round value, a malicious proposer gains the ability to selectively include advantageous vote extensions from historical rounds, potentially influencing the outcome in their favor. 

## Remediation

1. Implement additional checks to validate the voting power calculation and ensure that the vote extensions are representative of the entire validator set rather than being controlled by a single entity.

2. Add additional validation checks to ensure that the Round value injected by the proposer is not from a past round.

---

© 2024 Otter Audits LLC. All Rights Reserved. 6/16  
Cosmos SDK Audit 04 — Vulnerabilities  
Patch  
Fixed in 7155a1c.  
© 2024 Otter Audits LLC. All Rights Reserved. 7/16

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cosmos SDK |
| Report Date | N/A |
| Finders | James Wang, Naoya Okanami, Tuyết Dương |

### Source Links

- **Source**: https://cosmos.network/
- **GitHub**: https://github.com/cosmos/cosmos-sdk
- **Contest**: https://cosmos.network/

### Keywords for Search

`vulnerability`

