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
solodit_id: 19479
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Stopped Validators Do Not Contribute Towards the Operator’s Staking Limit

### Overview

See description below for full details.

### Original Finding Content

## Description

Lido-DAO Node Operators are registered with a "Staking Limit", which restricts the number of validators that the Node Operator is allowed to run on behalf of the DAO. While set in `NodeOperatorRegistry.sol`, this limit is enforced only in `Lido.sol`:

```solidity
500 uint256 stake = entry.usedSigningKeys.sub(entry.stoppedValidators);
if (stake + 1 > entry.stakingLimit)
502 continue;
```

As shown, stopped validators (identified via `NodeOperatorRegistry.reportStoppedValidators()`) do not contribute to an operator’s staking limit. Indeed, a Node Operator who had previously reached the limit would be immediately eligible to receive an additional validator after one was reported stopped.

Based on the comment at `NodeOperatorRegistry.sol:51` and usage, the “stopped validator” status is used to indicate a slashed or exited validator, as opposed to one that is temporarily offline. Prior to the ability to withdraw from Eth2 (expected in Phase 1.5), there is no sound reason for a staking service to perform a voluntary exit or get slashed.

While it may be possible to reduce the operator’s staking limit at the same time as reporting the stopped validator, this may be difficult to do atomically or without the delays associated with an additional DAO vote. Although node operators are expected to be heavily vetted and trustworthy, a malicious operator could (in certain circumstances) slash more than its staking limit of validators. Because the current validator allocation prioritizes operators with fewer active validators, new deposits are more likely allocated to the malicious operator.

The Pausable mechanism can provide some protection against this, but requires external intervention and should be considered a last resort. We would argue that, in these circumstances, a safer default behavior would be for the stopped validators to contribute to the operator’s staking limit.

## Recommendations

Consider allowing stopped validators to count towards an operator’s staking limit (though this will be worth reconsidering when withdrawals are possible). With this, the staking limit can be interpreted as the total number of deposits entrusted to the operator.

In the event of an unexpected withdrawal or slashing (indicative of staking operator neglect or malice), the staking operator can submit an explanation to the DAO and request an increased staking limit.

[Phase 1.5 Details](https://ethereum.org/en/eth2/staking/)

## Resolution

The Lido team acknowledge this issue and plan to release a fix in a subsequent update (post-deployment).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf

### Keywords for Search

`vulnerability`

