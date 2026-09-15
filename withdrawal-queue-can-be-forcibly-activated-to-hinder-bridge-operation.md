---
# Core Classification
protocol: Immutable Smart Contracts
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26528
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-08-immutable-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-08-immutable-securityreview.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - business_logic
  - 1/64_rule
  - denial-of-service

protocol_categories:
  - bridge

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Priyanka Bose
  - Elvis Skoždopolj
  - Michael Colburn
---

## Vulnerability Title

Withdrawal queue can be forcibly activated to hinder bridge operation

### Overview


The RootERC20PredicateFlowRate contract implements a withdrawal queue to more easily detect and stop large withdrawals from passing through the bridge. This queue can be activated in four different ways: if a token's flow rate has not been configured by the rate control admin, if the withdrawal amount is larger than or equal to the large transfer threshold for that token, if the total withdrawals of that token are larger than the defined token capacity, or if the rate controller manually activates the queue. Once the queue is active, all withdrawals from the bridge must wait a specified time before the withdrawal can be finalized. This can be exploited by malicious actors to hinder the expected operation of the bridge. 

For example, Eve could observe Alice initiating a transfer to bridge her tokens back to the mainnet, and then initiate a transfer of enough tokens to exceed the expected flow rate. This would cause Alice's withdrawal to be pushed into the withdrawal queue and activate the queue for every other bridge user. Mallory could also exploit the queue by repeatedly triggering it for the bridge, degrading the user experience until Immutable disables the queue. This would give Mallory a window of time to carry out her exploit, bridge the funds, and move them into a mixer.

To prevent this type of exploitation, Immutable should explore the feasibility of withdrawal queues on a per-token basis instead of having only a global queue. Additionally, they should develop processes for regularly reviewing the configuration of the various token buckets, as fluctuating token values may make this type of grieﬁng more feasible.

### Original Finding Content

## Target: RootERC20PredicateFlowRate.sol

## Description

The withdrawal queue can be forcibly activated to impede the proper operation of the bridge.

The `RootERC20PredicateFlowRate` contract implements a withdrawal queue to more easily detect and stop large withdrawals from passing through the bridge (e.g., bridging illegitimate funds from an exploit). A transaction can enter the withdrawal queue in four ways:

1. If a token’s flow rate has not been configured by the rate control admin.
2. If the withdrawal amount is larger than or equal to the large transfer threshold for that token.
3. If, during a predefined period, the total withdrawals of that token are larger than the defined token capacity.
4. If the rate controller manually activates the withdrawal queue by using the `activateWithdrawalQueue` function.

In cases 3 and 4 above, the withdrawal queue becomes active for all tokens, not just the individual transfers. Once the withdrawal queue is active, all withdrawals from the bridge must wait a specified time before the withdrawal can be finalized. As a result, a malicious actor could withdraw a large amount of tokens to forcibly activate the withdrawal queue and hinder the expected operation of the bridge.

## Exploit Scenario 1

Eve observes Alice initiating a transfer to bridge her tokens back to the mainnet. Eve also initiates a transfer, or a series of transfers to avoid exceeding the per-transaction limit, of sufficient tokens to exceed the expected flow rate. With Alice unaware she is being targeted for grieving, Eve can execute her withdrawal on the root chain first, cause Alice’s withdrawal to be pushed into the withdrawal queue, and activate the queue for every other bridge user.

## Exploit Scenario 2

Mallory has identified an exploit on the child chain or in the bridge itself, but because of the withdrawal queue, it is not feasible to exfiltrate the funds quickly enough without risking getting caught. Mallory identifies tokens with small flow rate limits relative to their price and repeatedly triggers the withdrawal queue for the bridge, degrading the user experience until Immutable disables the withdrawal queue. Mallory takes advantage of this window of time to carry out her exploit, bridge the funds, and move them into a mixer.

## Recommendations

**Short term:** Explore the feasibility of withdrawal queues on a per-token basis instead of having only a global queue. Be aware that if the flow rates are set low enough, an attacker could feasibly use them to grief all bridge users.

**Long term:** Develop processes for regularly reviewing the configuration of the various token buckets. Fluctuating token values may unexpectedly make this type of grieving more feasible.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | TrailOfBits |
| Protocol | Immutable Smart Contracts |
| Report Date | N/A |
| Finders | Priyanka Bose, Elvis Skoždopolj, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-08-immutable-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-08-immutable-securityreview.pdf

### Keywords for Search

`Business Logic, 1/64 Rule, Denial-Of-Service`

