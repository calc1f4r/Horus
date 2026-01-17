---
# Core Classification
protocol: Autonomint Colored Dollar V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45490
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/1052

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
  - 0x73696d616f
---

## Vulnerability Title

H-37: `treasury.updateYieldsFromLiquidatedLrts()` updates the yield in the current chain, but collateral may be in the other chain

### Overview


This bug report is about a function called `treasury.updateYieldsFromLiquidatedLrts()` that updates the yield in one chain, but may use collateral from another chain. This can cause the protocol to withdraw yields that it should not, which can result in other deposited collateral not being able to be withdrawn. This can lead to a lack of funds in one chain, causing withdrawals to be delayed. The bug can be fixed by setting the yields in the chain where the liquidation happened and the collateral is held.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/1052 

## Found by 
0x73696d616f

### Summary

[treasury.updateYieldsFromLiquidatedLrts()](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/lib/CDSLib.sol#L667-L670) updates the yield from liquidated collateral in the current chain, but this collateral could have been present in the other chain. As such, it will allow the protocol to withdrawal yields that it should not in the current chain, which means other deposited collateral may not be withdrawn due to having been allocated as yield instead.

### Root Cause

In `CDSLib::667`, the treasury is updated with liquidated collateral yield, but this yield may be present in the other chain.

### Internal pre-conditions

None.

### External pre-conditions

None.

### Attack Path

1. Borrower is liquidated in chain B.
2. Some time passes and a cds depositor in chain A withdraws a part of the collateral, and updates the treasury with yield generated.
3. The yield generated is not actually present in chain A, and is in chain B instead, so it will add yield to the treasury that is not actually backed in chain A.
4. Protocol withdraws the yield in chain A, which is taken from other borrower deposits, who may not be able to withdraw due to lack of liquidity (or similar).

### Impact

Lack of funds in chain A, leading to DoSed withdrawals.

### PoC

None.

### Mitigation

The yields should always be set in the chain that the liquidation happened and the collateral is held.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | 0x73696d616f |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/1052
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

