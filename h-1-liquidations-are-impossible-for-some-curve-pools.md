---
# Core Classification
protocol: Notional Update #2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6690
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/52
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-notional-judging/issues/21

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - usmannk
---

## Vulnerability Title

H-1: Liquidations are impossible for some Curve pools

### Overview


This bug report is about the Liquidations being impossible for some Curve pools. It was found by usmannk and was manually reviewed. The issue is that when the `deleverageAccount` function is called, it calls `_checkReentrancyContext` to protect against read-only reentrancy, which uses the `remove_liquidity` function to check the reentrancy context. The problem is that for certain Curve pools like the CRV/ETH pool, calling `remove_liquidity(0, [0,0])` always reverts due to an underflow. This means that liquidations are not possible, and users can go into bad debt with no way to recover the lost funds. 

The recommendation is to use the `claim_admin_fees` function to check Curve's reentrancy state instead of `remove_liquidity`. It was discussed that validating 1 token will be sufficient to pass the underflow check, and that a parameter of 1 or 0 should be passed based on the target pool.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-notional-judging/issues/21 

## Found by 
usmannk

## Summary

Some curve pools have implementations such that Notional liquidations always revert.

## Vulnerability Detail

Liquidations are done, directly or indirectly, via the `deleverageAccount` function. This function calls `_checkReentrancyContext` to protect against read-only reentrancy.

The Curve vault's `_checkReentrancyContext` function uses the Curve `remove_liquidity` function to check the reentrancy context. However, for certain Curve pools like the CRV/ETH pool (0x8301ae4fc9c624d1d396cbdaa1ed877821d7c511, https://curve.fi/#/ethereum/pools/crveth/) calling `remove_liquidity(0, [0,0])` always reverts due to an underflow.

https://github.com/sherlock-audit/2023-02-notional/blob/main/leveraged-vaults/contracts/vaults/curve/mixins/Curve2TokenVaultMixin.sol#L13-L16

## Impact

Liquidations are not possible, users can go into bad debt and there is no way to recover the lost funds.

## Code Snippet

## Tool used

Manual Review

## Recommendation

Use the `claim_admin_fees` function to check Curve's reentrancy state instead of `remove_liquidity`.

## Discussion

**jeffywu**

Valid, appears that removing 1 token will be sufficient to pass the underflow check. We need to make a note of this and ensure that we either pass in a parameter of 1 or 0 based on the target pool.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Notional Update #2 |
| Report Date | N/A |
| Finders | usmannk |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-notional-judging/issues/21
- **Contest**: https://app.sherlock.xyz/audits/contests/52

### Keywords for Search

`vulnerability`

