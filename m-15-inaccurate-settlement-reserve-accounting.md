---
# Core Classification
protocol: Notional V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18593
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/59
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-notional-judging/issues/196

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

protocol_categories:
  - liquid_staking
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - xiaoming90
---

## Vulnerability Title

M-15: Inaccurate settlement reserve accounting

### Overview


This bug report is about an issue found in the off-chain accounting of fCash debt or prime cash in the settlement reserve of the Sherlock Audit project. The bug was found by xiaoming90 and was identified as inaccurate accounting due to an error when handling the conversion between signed and unsigned integers.

The bug occurs when an event is emitted to reconcile off-chain accounting for the edge condition when leveraged vaults lend at zero interest. In an event where `s.fCashDebtHeldInSettlementReserve > 0` and `s.primeCashHeldInSettlementReserve <= 0`, no event will be emitted, resulting in the off-chain accounting of fCash debt or prime cash in the settlement reserve being off. This is because `fCashDebtInReserve` is the negation of `s.fCashDebtHeldInSettlementReserve`, which is an unsigned integer, and `fCashDebtInReserve > 0` will always be false and is an unsatisfiable condition.

The impact of this bug is that the off-chain accounting of fCash debt or prime cash in the settlement reserve will be inaccurate. This could lead to users making ill-informed decisions based on inaccurate accounting information and exposing themselves to unintended financial risks.

The code snippet for this bug can be found in the PrimeRateLib.sol file on line 459. The bug was identified through manual review. The recommended fix is to change line 459 from `int256 fCashDebtInReserve = -int256(s.fCashDebtHeldInSettlementReserve)` to `int256 fCashDebtInReserve = int256(s.fCashDebtHeldInSettlementReserve)`.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-notional-judging/issues/196 

## Found by 
xiaoming90
## Summary

The off-chain accounting of fCash debt or prime cash in the settlement reserve will be inaccurate due to an error when handling the conversion between signed and unsigned integers.

## Vulnerability Detail

Events will be emitted to reconcile off-chain accounting for the edge condition when leveraged vaults lend at zero interest. This event will be emitted if there is fCash debt or prime cash in the settlement reserve.

In an event where `s.fCashDebtHeldInSettlementReserve > 0` and `s.primeCashHeldInSettlementReserve <= 0`, no event will be emitted. As a result, the off-chain accounting of fCash debt or prime cash in the settlement reserve will be off. 

The reason is that since `fCashDebtInReserve` is the negation of `s.fCashDebtHeldInSettlementReserve`, which is an unsigned integer, `fCashDebtInReserve` will always be less than or equal to 0. Therefore, `fCashDebtInReserve > 0` will always be false and is an unsatisfiable condition.

https://github.com/sherlock-audit/2023-03-notional/blob/main/contracts-v2/contracts/internal/pCash/PrimeRateLib.sol#L459

```solidity
File: PrimeRateLib.sol
457:         // This is purely done to fully reconcile off chain accounting with the edge condition where
458:         // leveraged vaults lend at zero interest.
459:         int256 fCashDebtInReserve = -int256(s.fCashDebtHeldInSettlementReserve);
460:         int256 primeCashInReserve = int256(s.primeCashHeldInSettlementReserve);
461:         if (fCashDebtInReserve > 0 || primeCashInReserve > 0) {
462:             int256 settledPrimeCash = convertFromUnderlying(settlementRate, fCashDebtInReserve);
463:             int256 excessCash;
464:             if (primeCashInReserve > settledPrimeCash) {
465:                 excessCash = primeCashInReserve - settledPrimeCash;
466:                 BalanceHandler.incrementFeeToReserve(currencyId, excessCash);
467:             } 
468: 
469:             Emitter.emitSettlefCashDebtInReserve(
470:                 currencyId, maturity, fCashDebtInReserve, settledPrimeCash, excessCash
471:             );
472:         }
```

## Impact

The off-chain accounting of fCash debt or prime cash in the settlement reserve will be inaccurate. Users who rely on inaccurate accounting information to conduct any form of financial transaction will expose themselves to unintended financial risks and make ill-informed decisions.

## Code Snippet

https://github.com/sherlock-audit/2023-03-notional/blob/main/contracts-v2/contracts/internal/pCash/PrimeRateLib.sol#L459

## Tool used

Manual Review

## Recommendation

It is recommended to implement the following fix:

```diff
- int256 fCashDebtInReserve = -int256(s.fCashDebtHeldInSettlementReserve);
+ int256 fCashDebtInReserve = int256(s.fCashDebtHeldInSettlementReserve);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Notional V3 |
| Report Date | N/A |
| Finders | xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-notional-judging/issues/196
- **Contest**: https://app.sherlock.xyz/audits/contests/59

### Keywords for Search

`vulnerability`

