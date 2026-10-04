---
# Core Classification
protocol: Raydium AMM V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48451
audit_firm: OtterSec
contest_link: https://raydium.io/
source_link: https://raydium.io/
github_link: github.com/raydium-io/raydium-amm-v3.

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
finders_count: 5
finders:
  - Michal Bochnak
  - Maher Azzouzi
  - Robert Chen
  - OtterSec
  - William Wang
---

## Vulnerability Title

Arbitrary AMM Config Possible Usage

### Overview


This bug report discusses an issue with the SwapRouterBaseIn instruction in a program. This instruction does not have the same checks as the Swap instruction, which allows for any AMM Config to be passed and manipulate the fee value. To fix this, the instruction should verify that the AMM Config passed is the same one assigned to the PoolState. This issue has been fixed in a patch.

### Original Finding Content

## PoolState and AMM Configs

Every `PoolState` is created using one of the existing AMM configs. The `AmmConfig` structure is used in the `swap_internal` function to determine `trade_fee_rate`, `protocol_fee_rate`, and `fund_fee_rate` that is used in the current pool. 

In the Swap instruction, there are implemented anchor checks that validate the given `AmmConfig` to be the one that `PoolState` was initialized with. However, the instruction `SwapRouterBaseIn` doesn’t implement those checks. The lack of checks makes it possible to pass any AMM config to the `UwapRouterBaseIn` and as a result, manipulate the fee value.

## Remediation

In order for the issue to be remediated, the `SwapRouterBaseIn` instruction should verify that the `amm_config`, which was passed to the instruction, is the one assigned to the `PoolState`. This can be done by adding the same check that is implemented for the Swap instruction.

**File**: `src/instructions/swap_router_base_in.rs`  
**Language**: RUST

```rust
require!(pool_state.amm_config == amm_config.key());
```

## Patch

Fixed in #35.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Raydium AMM V3 |
| Report Date | N/A |
| Finders | Michal Bochnak, Maher Azzouzi, Robert Chen, OtterSec, William Wang |

### Source Links

- **Source**: https://raydium.io/
- **GitHub**: github.com/raydium-io/raydium-amm-v3.
- **Contest**: https://raydium.io/

### Keywords for Search

`vulnerability`

