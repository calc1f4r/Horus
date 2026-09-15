---
# Core Classification
protocol: Malda
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62735
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1029
source_link: none
github_link: https://github.com/sherlock-audit/2025-07-malda-judging/issues/686

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
  - befree3x
---

## Vulnerability Title

M-12: Rebalancer can drain market funds via excessive bridge fees

### Overview


Summary:

The `REBALANCER_EOA` role in the Malda protocol allows for a slow but steady extraction of value from the protocol's liquidity pools. This is due to a vulnerability in the `Rebalancer::sendMsg` function, which allows the `REBALANCER_EOA` to set an arbitrarily high `maxFee` when initiating a bridge transfer through `EverclearBridge.sol`. This can result in a loss of funds from the protocol's liquidity pools. The protocol team has fixed this issue by implementing a maximum fee limit and validating the `maxFee` parameter in the `EverclearBridge.sendMsg` function. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-07-malda-judging/issues/686 

## Found by 
befree3x

### Summary

The `REBALANCER_EOA` role, which is considered semi-trusted, can drain funds from any market by specifying an arbitrarily high `maxFee` when initiating a bridge transfer through `EverclearBridge.sol`. This violates the trust assumption that the Rebalancer "cannot transfer user funds" and can only perform DDoS-style attacks, as it allows for a slow but steady extraction of value from the protocol's liquidity pools.

### Root Cause

The [`Rebalancer::sendMsg`](https://github.com/sherlock-audit/2025-07-malda/blob/main/malda-lending/src/rebalancer/Rebalancer.sol#L129) function allows the `REBALANCER_EOA` to pass an unchecked `_message` blob to the selected bridge contract. The [`EverclearBridge.sendMsg`](https://github.com/sherlock-audit/2025-07-malda/blob/main/malda-lending/src/rebalancer/bridges/EverclearBridge.sol#L79) function decodes this message to extract bridging parameters, including a `maxFee`. However, the bridge contract fails to validate this `maxFee` against any protocol-defined limit, instead passing it directly to the external [`everclearFeeAdapter.newIntent`](https://github.com/sherlock-audit/2025-07-malda/blob/main/malda-lending/src/rebalancer/bridges/EverclearBridge.sol#L111-L117) call. A malicious `REBALANCER_EOA` can therefore set this fee to an extreme value, causing the protocol to lose most of the bridged amount to fees.

### Internal Pre-conditions

- A market (e.g., `mWethHost`) has liquidity.
- The `EverclearBridge` is whitelisted in the Rebalancer.

### External Pre-conditions

The `REBALANCER_EOA` private key is compromised or its operator acts maliciously.

### Attack Path

A malicious actor controlling the `REBALANCER_EOA` decides to drain funds from the `mWethHost` market.

- The actor calls `Rebalancer.sendMsg`, targeting the `EverclearBridge` and `mWethHost`.
- It provides a valid `_amount` to extract from the market, for example, `10 WETH`.
- It crafts the `_message` parameter. Inside this message, which is decoded by `EverclearBridge`, it sets the amount to be bridged to 10 WETH but sets the `maxFee` parameter to an extremely high value, such as `9.9 WETH`.
- The `Rebalancer` contract extracts `10 WETH` from `mWethHost` and calls `EverclearBridge.sendMsg`.
- `EverclearBridge` decodes the message but performs no validation on the `maxFee`.
- It calls `everclearFeeAdapter.newIntent`, passing along the malicious maxFee of `9.9 WETH`.
- The external `Everclear` protocol executes the bridge transfer. It sends `10 WETH` but is authorized to take up to `9.9 WETH` as a fee, which is lost from the protocol. Only 0.1 WETH (or less) arrives at the destination market.
- The attacker can repeat this process, draining a substantial portion of the market's liquidity over time through exorbitant fees.

### Impact

`Rebalancer` can cause permanent loss of protocol funds. This attack directly drains the liquidity provided by users from the market contracts. While the `REBALANCER_EOA` does not receive the funds directly, their action causes value to be extracted from the protocol and paid to third-party bridge relayers.


### PoC

_No response_

### Mitigation

The protocol should not blindly trust the `maxFee` parameter provided by the semi-trusted `REBALANCER_EOA`. A centrally-controlled, maximum allowable fee should be enforced.

- The `GUARDIAN_BRIDGE` role (a more trusted admin) should set a maximum fee limit (e.g., as a percentage or basis points) on a per-token, per-chain basis within the `Rebalancer` or bridge contracts.
- The `EverclearBridge.sendMsg` function must validate that the `maxFee` parameter decoded from the message does not exceed the configured maximum fee limit for that specific bridging route.

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/malda-protocol/malda-lending/pull/139


**CergyK**

Fix looks good





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Malda |
| Report Date | N/A |
| Finders | befree3x |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-07-malda-judging/issues/686
- **Contest**: https://app.sherlock.xyz/audits/contests/1029

### Keywords for Search

`vulnerability`

