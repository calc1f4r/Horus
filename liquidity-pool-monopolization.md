---
# Core Classification
protocol: Raydium AMM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48315
audit_firm: OtterSec
contest_link: https://raydium.io/
source_link: https://raydium.io/
github_link: https://github.com/raydium-io/raydium-amm

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
finders_count: 4
finders:
  - Maher Azzouzi
  - Robert Chen
  - OtterSec
  - William Wang
---

## Vulnerability Title

Liquidity Pool Monopolization

### Overview


The bug report states that a malicious user can manipulate the LP token ratio in a pool, causing rounding errors that result in them stealing funds from other users. This can happen when the pool is first started and the attacker sends a small amount of LP tokens, then adds more tokens to increase the exchange rate. This causes subsequent deposits to round down the output LP token amount, resulting in stolen funds. The report also mentions that this could potentially lead to a denial of service situation. The code snippet provided shows that the issue lies in the process_deposit function in the processor.rs file. The suggested solution is to lock or burn a fixed number of LP tokens when providing liquidity for the first time, similar to what Uniswap does. This issue has been resolved in the latest patch.

### Original Finding Content

## Vulnerability Analysis: Malicious Liquidity Provider

A malicious early liquidity provider can maliciously raise the LP token ratio, stealing funds from other users who deposit insufficient funds into the pool due to rounding errors.

## Attack Scenario

When a pool is started, an attacker can:
- Initialize the pool with a small amount of LP tokens.
- Send tokens to the pool to increase the exchange rate.

Subsequent deposit operations will then round down the output LP token amount, which leads to the theft of funds due to the rounding behavior of LP token minting. Alternatively, this could also represent a denial of service scenario due to conditions that prevent minting zero LP tokens.

### Example Code

```rust
src/processor.rs RUST

pub fn process_deposit(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    deposit: DepositInstruction,
) -> ProgramResult {
    ...
    if mint_lp_amount == 0 || deduct_coin_amount == 0 || deduct_pc_amount == 0 {
        return Err(AmmError::InvalidInput.into());
    }
    ...
}
```

## Remediation

Similar to what Uniswap does, when providing liquidity to the pool for the very first time, the contract can lock away or burn a fixed number of LP tokens to ensure that the initial ratio will be preserved, even if an attacker directly sends funds to the vaults.

## Patch

Resolved in commit `3dc6a26`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Raydium AMM |
| Report Date | N/A |
| Finders | Maher Azzouzi, Robert Chen, OtterSec, William Wang |

### Source Links

- **Source**: https://raydium.io/
- **GitHub**: https://github.com/raydium-io/raydium-amm
- **Contest**: https://raydium.io/

### Keywords for Search

`vulnerability`

