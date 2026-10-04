---
# Core Classification
protocol: Sui Axelar (Gateway V2)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47310
audit_firm: OtterSec
contest_link: https://www.axelar.network/
source_link: https://www.axelar.network/
github_link: https://github.com/axelarnetwork/axelar-cgp-sui

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
finders_count: 3
finders:
  - Robert Chen
  - Tuyết Dương
  - Jessica Clendinen
---

## Vulnerability Title

Utilization of Incorrect Flow Tracking

### Overview


This bug report discusses a vulnerability in the function "give_coin" within the "CoinManagement" code. The function is currently using "add_flow_out" to track the outflow of tokens, even in situations where it should account for the inflow of tokens. This is causing incorrect tracking of token flow, especially when receiving tokens through interchain transfers. The suggested solution is to modify the function to use "add_flow_in" instead of "add_flow_out" when receiving tokens. This issue has been resolved in a recent pull request.

### Original Finding Content

## Vulnerability Report

The vulnerability concerns the incorrect utilization of flow management in `give_coin` within `CoinManagement`. Specifically, the function currently calls `add_flow_out`, which is intended to track the outflow of tokens, even in situations where it should account for the inflow of tokens when receiving transfers.

> _axelar-cgp-sui/move/its/sources/types/coin_management.move rust_

```rust
public(package) fun give_coin<T>(
    self: &mut CoinManagement<T>,
    mut amount: u256,
    clock: &Clock,
    ctx: &mut TxContext,
): Coin<T> {
    amount = amount + self.dust;
    self.dust = amount % self.scaling;
    let sui_amount = (amount / self.scaling as u64);
    self.flow_limit.add_flow_out(sui_amount, clock);
    if (has_capability(self)) {
        self.mint(sui_amount, ctx)
    } else {
        coin::take(self.balance.borrow_mut(), sui_amount, ctx)
    }
}
```

In the current implementation, the function utilizes `self.flow_limit.add_flow_out(sui_amount, clock)` to record the amount of tokens given out. This is inappropriate when the system is receiving tokens through an interchain transfer. Utilizing `add_flow_out` during a reception scenario inaccurately reflects the state of token flow. Instead of tracking tokens that are leaving the system, it should track tokens coming in.

## Remediation

Modify `give_coin` to utilize `add_flow_in` instead of `add_flow_out` when receiving tokens.

## Patch

Resolved in PR #190.

© 2024 Otter Audits LLC. All Rights Reserved. 6/18

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Sui Axelar (Gateway V2) |
| Report Date | N/A |
| Finders | Robert Chen, Tuyết Dương, Jessica Clendinen |

### Source Links

- **Source**: https://www.axelar.network/
- **GitHub**: https://github.com/axelarnetwork/axelar-cgp-sui
- **Contest**: https://www.axelar.network/

### Keywords for Search

`vulnerability`

