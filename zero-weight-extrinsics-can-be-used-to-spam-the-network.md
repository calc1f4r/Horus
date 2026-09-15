---
# Core Classification
protocol: Polkaswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48902
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
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
finders_count: 2
finders:
  - Dominik Czarnota
  - Artur Cygan
---

## Vulnerability Title

Zero-weight extrinsics can be used to spam the network

### Overview


This bug report describes a problem with the code in the SORA Network's technical library. Specifically, there are several functions that have a weight of zero, which means they can be used to spam the network and cause a denial of service. This could happen if an attacker sends many low-fee transactions using these functions. The report recommends benchmarking these functions and changing their weights to prevent this type of attack.

### Original Finding Content

## Type: Undefined Behavior
## Target: sora2-substrate/pallets/technical/src/lib.rs

**Difficulty:** High

## Description
The following extrinsics have a base weight set to zero and can therefore be used to spam the network, causing a denial of service:

- `PswapDistribution::claim_incentive`
- `BridgeMultisig::register_multisig`
- `BridgeMultisig::remove_signatory`
- `BridgeMultisig::add_signatory`
- `BridgeMultisig::as_multi_threshold_1`
- `BridgeMultisig::as_multi`
- `BridgeMultisig::approve_as_multi`
- `BridgeMultisig::cancel_as_multi`

Note, though, that `BridgeMultisig::as_multi` can be used for network spamming only if the account ID of the sender is not found in the `Accounts` storage map (specifically due to `unwrap_or(0)`).

## Exploit Scenario
An attacker sends numerous batch transactions that make many calls to the `pswap-distribution` pallet's `claim_incentive` extrinsic, each for a very low fee. By spamming the network in this way, the attacker causes a denial of service of the SORA Network.

## Recommendations
Short term, benchmark the extrinsics that have a base weight set to zero. Then, based on the results of that benchmarking, change the weights so that they cannot be used to spam the network.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Polkaswap |
| Report Date | N/A |
| Finders | Dominik Czarnota, Artur Cygan |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf

### Keywords for Search

`vulnerability`

