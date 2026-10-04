---
# Core Classification
protocol: Cosmos SDK V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47204
audit_firm: OtterSec
contest_link: https://cosmos.network/
source_link: https://cosmos.network/
github_link: https://github.com/cosmos/cosmos-sdk

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
finders_count: 3
finders:
  - James Wang
  - DRA
  - Super Fashi
---

## Vulnerability Title

Code Clarity

### Overview

See description below for full details.

### Original Finding Content

## CosmOS SDK Audit 05 — General Findings

## Remediation

1. In `msg_server::RotateConsPubKey`, the name of the `NewToOldConsKeyMap` mapping implies that it keeps track of the relationship between the new consensus key and the previous one. However, this is not the case. Instead, it stores the relationship between the new consensus key and the initial (original) consensus key for a given validator. This misnomer may result in confusion for developers and maintainers of the code.

2. Lockup accounts track both `DeletegatedLocking` and `DelegatedFree` for delegations, which unnecessarily complicates the internal logic. It also introduces side effects where bond refunds may exceed tracked undelegated amount, and the additional bonuses could not be withdrawn on undelegation.

    > _x/accounts/defaults/lockup/lockup.go_
    ```go
    // NOTE: The undelegation (bond refund) amount may exceed the delegated
    // locking (bond) amount due to the way undelegation truncates the bond refund,
    // which can increase the validator's exchange rate (tokens/shares) slightly if
    // the undelegated tokens are non-integral.
    func (bva *BaseLockup) TrackUndelegation(ctx context.Context, amount sdk.Coins) error {
        bondDenom, err := getStakingDenom(ctx)
        if err != nil {
            return err
        }
        delAmt := amount.AmountOf(bondDenom)
        // return error if the undelegation amount is zero
        if delAmt.IsZero() {
            return sdkerrors.ErrInvalidCoins.Wrap("undelegation attempt with zero coins for staking denom")
        }
        delFreeAmt, err := bva.DelegatedFree.Get(ctx, bondDenom)
        if err != nil {
            return err
        }
        delLockingAmt, err := bva.DelegatedLocking.Get(ctx, bondDenom)
        if err != nil {
            return err
        }
        // compute x and y per the specification, where:
        // X := min(DF, D)
        // Y := min(DV, D - X)
        x := math.MinInt(delFreeAmt, delAmt)
        y := math.MinInt(delLockingAmt, delAmt.Sub(x))
        [...]
    }
    ```

© 2024 Otter Audits LLC. All Rights Reserved. 17/22  
DRAFT

## Proposed Remediation

1. Rename `NewToOldConsKeyMap` to `ConsKeyToValidatorIdentifier` (or a similarly descriptive name).
2. We recommend tracking a single `Delegated` instead, which both simplifies the logic and eliminates undesirable side effects.

© 2024 Otter Audits LLC. All Rights Reserved. 18/22  
DRAFT

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cosmos SDK V3 |
| Report Date | N/A |
| Finders | James Wang, DRA, Super Fashi |

### Source Links

- **Source**: https://cosmos.network/
- **GitHub**: https://github.com/cosmos/cosmos-sdk
- **Contest**: https://cosmos.network/

### Keywords for Search

`vulnerability`

