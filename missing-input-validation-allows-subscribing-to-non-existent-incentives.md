---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19607
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Missing Input Validation Allows Subscribing to Non-Existent Incentives

### Overview


This bug report describes a vulnerability in a contract which allows an attacker to steal more rewards than available in a given incentive. This is achieved by exploiting a bug which allows subscribing to incentives which do not yet exist, and by subscribing to an incentive multiple times. The attacker subscribes to a nonexistent, but upcoming, incentive number using a fake zero-address subscription. When a genuine user creates a new incentive with rewards, the attacker fakes their zero-address subscriptions for real ones by unsubscribing and re-subscribing. After some time has passed, the attacker calls claimRewards() for the victim’s incentiveId, allowing them to drain more rewards than those provided by the incentive creator.

This issue was rectified by rejecting subscriptions to non existent proposals with a check that forbids subscribing to an incentive which has a creator value of the zero-address, and by ensuring 0 < incentiveId && incentiveId <= incentiveCount. The fix is outlined in PR 1.

### Original Finding Content

## Description

Missing input validation checks allows an attacker to steal substantially more rewards than available in a given incentive. The attack occurs due to a bug which allows subscribing to incentives which do not yet exist. Furthermore, it is possible to subscribe to an incentive multiple times if it does not yet exist. `subscribeToIncentive` does not check if the user-supplied `incentiveId` is actually valid.

The bug is exploited by subscribing to a nonexistent incentive multiple times as seen in the following scenario:

1. The attacker subscribes 6 times to a nonexistent, but upcoming, incentive number. This is done using a fake zero-address subscription.
2. A genuine user creates a new incentive with X rewards in USDC. The incentive number matches the previously nonexistent one our attacker subscribed to.
3. As other users create similar USDC based rewards, the contract begins to hold a lot of USDC.
4. The attacker fakes their zero-address subscriptions for 6 real ones by unsubscribing and re-subscribing. He proceeds to stake some amount.
5. After some time has passed, the attacker unstakes some strategic amount, choosing to save rewards. This will set their `rewardPerLiquidityLast` erroneously low.
6. The attacker calls `claimRewards()` for the victim’s `incentiveId`. They have the ability to drain more rewards than those provided by the incentive creator, draining funds from other users.

Note that it is also possible to subscribe to the incentive with ID zero, which is never used.

## Recommendations

This issue may be mitigated by preventing the subscription to incentives which have not yet been created. This can be done by adding a check that forbids subscribing to an incentive which has a creator value of the zero-address. Alternatively, this issue may be mitigated by ensuring `0 < incentiveId && incentiveId <= incentiveCount`.

## Resolution

This issue was rectified by rejecting subscriptions to non-existent proposals as seen in the following code snippet:

```solidity
if (incentiveId > incentiveCount || incentiveId <= 0) revert InvalidInput();
```

The fix is outlined in PR 1.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf

### Keywords for Search

`vulnerability`

