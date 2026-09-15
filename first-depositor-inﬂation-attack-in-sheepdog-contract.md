---
# Core Classification
protocol: Ceazor Snack Sandwich
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52901
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/f9915841-9c6c-4a7f-a601-eec90e45c8b2
source_link: https://cdn.cantina.xyz/reports/sheepcoin-security-review-final.pdf
github_link: none

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
  - r0bert
  - RustyRabbit
---

## Vulnerability Title

First Depositor Inﬂation Attack in SheepDog Contract 

### Overview


The SheepDog contract is vulnerable to a "first depositor inflation attack" where an attacker can manipulate the share allocation system to gain control over other users' deposits. This is done by calling the "protect" function with a small deposit and then transferring a large amount of tokens to the contract, causing an inflation in the total balance without affecting the total shares. This results in subsequent legitimate deposits receiving zero shares due to rounding errors. The attacker can then claim the entire pool after a 2-day withdrawal delay, leaving other users with no returns. To fix this, the report recommends either minting initial shares to a dead address or setting a minimum initial deposit threshold. The bug has been fixed in version 40b898d.

### Original Finding Content

## Security Review Summary

**Context:**  
(No context files were provided by the reviewer)

**Description:**  
The `SheepDog` contract is susceptible to a "first depositor inflation attack" where an attacker can exploit the share allocation mechanism to gain disproportionate control over other users' deposits. By calling `protect` with a minimal deposit (e.g., 1 wei) when `totalShares` is 0, the attacker mints 1 share and becomes the sole shareholder. They then directly transfer a large quantity of SHEEP tokens to the contract via an ERC20 transfer, inflating the `totalSheep` balance without altering `totalShares`. Subsequent legitimate deposits, especially those smaller than the inflated `totalSheep` balance, receive 0 shares due to precision loss in the calculation of `amount * totalShares / totalSheep`, which rounds down to zero as `totalShares` is too small relative to `totalSheep`. After a 2-day withdrawal delay, the attacker can claim the entire pool, including all deposited SHEEP, leaving other users with no returns.

**Recommendation:**  
Consider implementing one of the following solutions:

1. **Mint initial shares to a dead address:** When deploying the `SheepDog` contract, mint a predetermined, fixed amount of shares (e.g., 10,000 shares) and assign them to a dead address like `address(0)`. These shares should be permanently locked, meaning they cannot be redeemed or transferred. This ensures that the `totalShares` (or equivalent total supply variable) starts at a non-zero value.

2. **Set a minimum initial deposit threshold:** Require depositors to contribute a sufficiently large amount of assets (e.g., a minimum `totalSheep` value). This prevents the initial deposit from being too small, which could exacerbate rounding errors or allow manipulation.

**Ceazor Snack Sandwich:**  
Fixed in `40b898d`.

**Cantina:**  
Fix OK.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Ceazor Snack Sandwich |
| Report Date | N/A |
| Finders | r0bert, RustyRabbit |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/sheepcoin-security-review-final.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/f9915841-9c6c-4a7f-a601-eec90e45c8b2

### Keywords for Search

`vulnerability`

