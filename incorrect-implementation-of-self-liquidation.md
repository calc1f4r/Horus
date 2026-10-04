---
# Core Classification
protocol: Blend Capital
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47445
audit_firm: OtterSec
contest_link: https://www.script3.io/
source_link: https://www.script3.io/
github_link: https://github.com/blend-capital/blend-contracts

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
finders_count: 2
finders:
  - Andreas Mantzoutas
  - Nicola Vella
---

## Vulnerability Title

Incorrect Implementation Of Self Liquidation

### Overview


The report describes a vulnerability in a function called "fill_user_liq_auction" that can lead to incorrect user positions after a self-liquidation process. This happens when a user is both being liquidated and acting as the filler at the same time. The problem occurs because the function assumes that loading the user's state at the beginning of the process provides an accurate representation of the user's state. However, if the user's state is altered in memory but not yet written to storage, retrieving from storage may fetch an outdated version, resulting in an inconsistency between the expected and actual user positions. This vulnerability has been fixed by preventing self-liquidations.

### Original Finding Content

## Vulnerability in `user_liquidation_auction`'s `fill_user_liq_auction`

There exists a vulnerability in `user_liquidation_auction`'s `fill_user_liq_auction` due to an inconsistency in the state of the liquidated user (`user_state`). The problem emerges when the user acts simultaneously as both the one being liquidated and the filler. `fill_user_liq_auction` incorrectly assumes that loading the user’s state at the outset

```rust
let mut user_state = User::load(e, user);
```

provides a precise and current representation of the user’s state.

## Code Snippet
> _auctions/user_liquidation_auction.rs_

```rust
pub fn fill_user_liq_auction(
    e: &Env,
    pool: &mut Pool,
    auction_data: &AuctionData,
    user: &Address,
    filler_state: &mut User,
) {
    let mut user_state = User::load(e, user);
    [...]
}
```

However, during the self-liquidation process, when the user’s state is altered in memory (cached in `from_state`) but not yet written to storage, retrieving from storage may fetch an outdated version, resulting in an inconsistency between the expected and actual user positions post self-liquidation.

## Proof of Concept
In the provided scenario, the user initially possesses a specific amount of collateral in `Token0` and has liabilities in `Token1`. Concurrently, there is an active auction (`UserAuction`) featuring bids (`bid`) and lots (`lot`) associated with these tokens.

> _example.rs_

```rust
UserPosition: {
    collateral: { Token0: x1 },
    liabilities: { Token1: y1 },
},
UserAuction: {
    bid: { Token1: y2 },
    lot: { Token0: x2 },
}
```

Following self-liquidation, the expected user positions should reflect the changes in collateral and liabilities directly, as shown below:

> _example.rs_

```rust
UserPosition: {
    collateral: { Token0: x1 + x2 },
    liabilities: { Token1: y1 + y2 },
}
```

Due to the vulnerability, the actual updated user position incorrectly combines the existing collateral and liabilities with self-liquidation results.

> _example.rs_

```rust
UserPosition: {
    collateral: { Token0: x1 },
    liabilities: { Token1: y1 },
}
```

In this example, the issue lies in the incorrect aggregation of collateral (`Token0: x1 + x2`) and liabilities (`Token1: y1 + y2`). Thus, the actual state deviates from the expected state.

## Remediation
Ensure that the state loaded from storage (`user_state`) accurately reflects any in-memory changes made during the self-liquidation process.

## Patch
Fixed in a 10f49d by preventing self-liquidations.

© 2024 Otter Audits LLC. All Rights Reserved. 6/22

## Blend Capital Audit 04 — Vulnerabilities

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Blend Capital |
| Report Date | N/A |
| Finders | Andreas Mantzoutas, Nicola Vella |

### Source Links

- **Source**: https://www.script3.io/
- **GitHub**: https://github.com/blend-capital/blend-contracts
- **Contest**: https://www.script3.io/

### Keywords for Search

`vulnerability`

