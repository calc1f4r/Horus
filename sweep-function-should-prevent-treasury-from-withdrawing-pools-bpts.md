---
# Core Classification
protocol: Gauntlet
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7086
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - yield
  - insurance
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Emanuele Ricci
  - Eric Wang
  - Gerard Persoon
---

## Vulnerability Title

sweep function should prevent Treasury from withdrawing pool’s BPTs

### Overview


This bug report is about a critical risk found in AeraVaultV1.sol#L559-L561. This risk allows the vault owner, also known as the Treasury, to sweep any token owned by the vault, including Balancer Pool Tokens (BPTs). BPTs are tokens that are minted by the Vault during the pool’s initialDeposit() function call. The current vault implementation does not need these BPTs to withdraw funds because they are passed directly through the AssetManager flow via withdraw()/finalize(). 

The Treasury is able to withdraw funds without respecting the time period between initiateFinalization() and finalize() calls, without respecting Validator allowance() limits, and without paying the manager’s fee for the last withdraw(). They are also able to finalize the pool, withdrawing all funds and selling valueless BPTs on the market. Furthermore, the Treasury can sell or rent out BPTs and withdraw funds afterwards, thus doubling the funds. This is possible because the Treasury can call setManager(newManager) and setSwapFee(0) to remove the swap fee, which would be applied during an exitPool() event.

To prevent this, the bug report recommends adding a check on the token input parameter to prevent the Treasury from withdrawing the Pool’s BTP tokens. The bug has been fixed in PR #132 and acknowledged by Spearbit.

### Original Finding Content

## Severity: Critical Risk

## Context
AeraVaultV1.sol#L559-L561

## Description
The current `sweep()` implementation allows the vault owner (the Treasury) to sweep any token owned by the vault including BPTs (Balancer Pool Tokens) that have been minted by the Vault during the pool’s `initialDeposit()` function call. The current vault implementation does not need those BPTs to withdraw funds because they are passed directly through the AssetManager flow via `withdraw()` / `finalize()`.

Being able to withdraw BPTs would allow the Treasury to:
- Withdraw funds without respecting the time period between `initiateFinalization()` and `finalize()` calls.
- Withdraw funds without respecting Validator `allowance()` limits.
- Withdraw funds without paying the manager’s fee for the last `withdraw()`.
- Finalize the pool, withdrawing all funds and selling valueless BPTs on the market.
- Sell or rent out BPTs and `withdraw()` funds afterwards, thus doubling the funds.

Swap fees would not be paid because Treasury could call `setManager(newManager)`, where the new manager is someone controlled by the Treasury, subsequently calling `setSwapFee(0)` to remove the swap fee, which would be applied during an `exitPool()` event.

**Note:** Once the BPT is retrieved, it can also be used to call `exitPool()`, as the `mustAllowlistLPs` check is ignored in `exitPool()`.

## Recommendation
Add a check on the token input parameter to prevent Treasury from withdrawing the Pool’s BPT tokens.

## Gauntlet
Fixed in PR #132

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Gauntlet |
| Report Date | N/A |
| Finders | Emanuele Ricci, Eric Wang, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

