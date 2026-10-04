---
# Core Classification
protocol: Allora
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36724
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/454
source_link: none
github_link: https://github.com/sherlock-audit/2024-06-allora-judging/issues/82

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
  - imsrybr0
---

## Vulnerability Title

M-16: Mint and Emissions modules register errors with an error code of 1

### Overview


The user imsrybr0 discovered a bug in the Mint and Emissions modules of the Allora judging system. The error code 1 is being used, which goes against the rule that it must be greater than one. This was found through a manual review and the recommendation is to not use 1 for error codes. The issue has been fixed by the protocol team in a recent pull request.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-06-allora-judging/issues/82 

## Found by 
imsrybr0
## Summary
Mint and Emissions modules register errors with an error code of 1

## Vulnerability Detail
Mint and Emissions modules register errors with an error code of 1

## Impact
According to the Cosmos SDK [Errors documentation](https://docs.cosmos.network/main/build/building-modules/errors#registration), the error code :

> Must be greater than one, as a code value of one is reserved for internal errors.

This breaks that rule.

## Code Snippet
[mint errors](https://github.com/sherlock-audit/2024-06-allora/blob/main/allora-chain/x/mint/types/errors.go#L6)
```golang
var (
	ErrUnauthorized                                    = errors.Register(ModuleName, 1, "unauthorized message signer")
	// ...
)
```

[emissions errors](https://github.com/sherlock-audit/2024-06-allora/blob/main/allora-chain/x/emissions/types/errors.go#L6)
```golang
var (
	ErrTopicReputerStakeDoesNotExist            = errors.Register(ModuleName, 1, "topic reputer stake does not exist")
	// ...
)
```
## Tool used
Manual Review

## Recommendation
Don't use 1 for error codes.



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/allora-network/allora-chain/pull/504

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Allora |
| Report Date | N/A |
| Finders | imsrybr0 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-06-allora-judging/issues/82
- **Contest**: https://app.sherlock.xyz/audits/contests/454

### Keywords for Search

`vulnerability`

