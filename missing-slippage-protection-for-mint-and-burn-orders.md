---
# Core Classification
protocol: TONCO CLAMM DEX v1.6
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64900
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2026-02-tonco-clamm-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2026-02-tonco-clamm-securityreview.pdf
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
  - Nicolas Donboly Trail of Bits PUBLIC
  - Elvis Skoždopolj
---

## Vulnerability Title

Missing slippage protection for mint and burn orders

### Overview


The report describes a bug in the Mint and Burn orders of a pool. These orders do not have user-defined slippage bounds or a deadline, which means that an attacker can manipulate the price and force unfavorable fills or extract value from the user's withdrawal. The Mint order structure only includes the operation type, liquidity, tick bounds, and receiver, while the Burn order structure only includes a liquidity-to-burn value. This allows an attacker to time the execution of a large swap to manipulate the price and then reverse it to extract value from the user's withdrawal. The report recommends adding per-order slippage bounds and enforcing them during execution, as well as adding tests to simulate price movement and ensure that orders revert when bounds are exceeded. 

### Original Finding Content

## Difficulty: Low

## Type: Timing

### Description

Mint and burn orders do not carry user-defined slippage bounds or a deadline, and the pool executes them against the current pool price without validating user intent. The mint order structure includes only the operation type, liquidity, tick bounds, and receiver, while the burn side carries only a liquidity-to-burn value.

Because these flows execute asynchronously across multiple messages, an attacker can change the price between the inclusion and execution of the order and force unfavorable fills, denial of service, or value extraction.

#### Mint Order Structure

```plaintext
struct MintOrder {
    op: int32;
    liquidity: uint128;
    tickLower: int24;
    tickUpper: int24;
    nftReceiver: address;
}
```

*Figure 7.1: Mint order schema has no minimum amount or deadline fields.*  
*(contracts/common/reforge_message.tolk#L88–L98)*

#### Burn Order Structure

```plaintext
struct BurnOrder {
    index: uint64,
    subindex: uint4,
    data: PosAndFeesData,
    liquidity2Burn: int128;
}
```

*Figure 7.2: Burn order schema has no minimum amount fields to protect withdrawals.*  
*(contracts/common/reforge_message.tolk#L53–L75)*

### Exploit Scenario

Bob, an attacker, monitors newly included blocks for reforge transactions that include burn orders and initiates a large swap to move the pool price to a less favorable level for the position’s tick range. He times the message execution so that the swap lands right before the pool executes the burn. The pool then processes the burn at the manipulated price and pays the user out in an imbalanced or reduced-value mix of tokens because no minimum output or deadline is enforced to validate user intent. Immediately after the burn order is executed, Bob reverses the price move and captures the difference via arbitrage across the pool and external markets, extracting value from the user’s withdrawal. The transaction cannot revert due to missing bounds.

### Recommendations

Short term, add per-order slippage bounds to the mint and burn schemas and enforce them during execution so that orders revert when current amounts violate user thresholds. Long term, add tests that simulate price movement between order creation and execution, and assert that mint and burn orders revert when bounds are exceeded and succeed when values are within bounds.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | TONCO CLAMM DEX v1.6 |
| Report Date | N/A |
| Finders | Nicolas Donboly Trail of Bits PUBLIC, Elvis Skoždopolj |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2026-02-tonco-clamm-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2026-02-tonco-clamm-securityreview.pdf

### Keywords for Search

`vulnerability`

