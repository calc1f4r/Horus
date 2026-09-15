---
# Core Classification
protocol: Elixir Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41637
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf
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
finders_count: 4
finders:
  - Damilola Edwards
  - Emilio López
  - Bo Henderson
  - Artur Cygan
---

## Vulnerability Title

Delegators can redelegate stakes to jailed delegatee

### Overview


This report discusses a bug in the Elixir Protocol that could lead to a denial of service. The issue is caused by a helper method that does not prevent users from delegating to a validator that has been jailed. This means that honest users could accidentally lose access to their stake. The bug occurs during redelegation, when the status of the new delegatee is not checked and they could potentially be jailed. This could result in a loss of funds for the delegator. The report recommends adding a check to the method to prevent delegating to jailed validators and also suggests improving the system to make it harder for users to make costly mistakes. 

### Original Finding Content

## Denial of Service Vulnerability

**Difficulty:** High

**Type:** Denial of Service

## Description

The internal `_updateDelegation` helper method does not prevent users from delegating to a validator that is jailed, allowing honest users to accidentally lose access to their stake. The delegate function is responsible for handling both delegation and redelegation actions. During redelegation, several validation checks are performed: ensuring that the redelegation has been signaled in advance, confirming that the current delegatee of the delegator is not jailed, and verifying the delegator has not signaled an unstake. However, the status of the new delegatee, to whom the delegator intends to move their stakes, is not checked if they are jailed. This allows for redelegation to a jailed validator, leading to potential loss of funds for the delegator.

## Exploit Scenario

Bob notices that Alice runs a validator with a good performance history, but he is unaware that Alice recently misbehaved. Bob sends a transaction delegating his stake to Alice right after another user sends a transaction jailing Alice, and both transactions succeed. As a result, Bob inadvertently loses access to his funds.

## Recommendations

- **Short term:** Add a check to the `_updateDelegation` method that reverts a transaction that attempts to delegate to a validator who has been jailed.
- **Long term:** Strive to make it as hard as possible for an honest user to make a costly mistake. Pay particular attention to race conditions that occur during contract state transitions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Elixir Protocol |
| Report Date | N/A |
| Finders | Damilola Edwards, Emilio López, Bo Henderson, Artur Cygan |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf

### Keywords for Search

`vulnerability`

