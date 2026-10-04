---
# Core Classification
protocol: Anchor
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5871
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-anchor-contest
source_link: https://code4rena.com/reports/2022-02-anchor
github_link: https://github.com/code-423n4/2022-02-anchor-findings/issues/41

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
  - dexes
  - cdp
  - services
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[M-06] Simple interest calculation is not exact

### Overview


This bug report is about a vulnerability in the money-market-contracts code on GitHub, which could lead to suppliers losing out on interest. The code uses a simple interest formula to compute the accrued debt, instead of a compounding formula. This means the actual borrow rate and interest for suppliers depend on how often updates are made. In highly active markets, the difference should be negligible, but in low-activity markets, it could lead to a lower borrow rate and suppliers missing out on interest. The recommended mitigation steps are to ensure that the markets are accrued regularly, or switch to a compound interest formula which has a higher computational cost but can be approximated (as seen in Aave).

### Original Finding Content


<https://github.com/code-423n4/2022-02-anchor/blob/7af353e3234837979a19ddc8093dc9ad3c63ab6b/contracts%2Fmoney-market-contracts%2Fcontracts%2Fmarket%2Fsrc%2Fborrow.rs#L304>

The borrow rate uses a simple interest formula to compute the accrued debt, instead of a compounding formula.

```rust
pub fn compute_interest_raw(
    state: &mut State,
    block_height: u64,
    balance: Uint256,
    aterra_supply: Uint256,
    borrow_rate: Decimal256,
    target_deposit_rate: Decimal256,
) {
  // @audit simple interest
    let passed_blocks = Decimal256::from_uint256(block_height - state.last_interest_updated);

    let interest_factor = passed_blocks * borrow_rate;
    let interest_accrued = state.total_liabilities * interest_factor;
    // ...
}
```

This means the actual borrow rate and interest for suppliers depend on how often updates are made.<br>
This difference should be negligible in highly active markets, but it could lead to a lower borrow rate in low-activity markets, leading to suppliers losing out on interest.

### Recommended Mitigation Steps

Ensure that the markets are accrued regularly, or switch to a compound interest formula (which has a higher computational cost due to exponentiation, but can be approximated, see Aave).

**[Alex the Entreprenerd (triage) commented](https://github.com/code-423n4/2022-02-anchor-findings/issues/41#issuecomment-1207281281):**
 > Without Code and explanation, I'm skeptical of Med (loss of yield), as it could just be dust amount, provided that interest is compounded roughly 1 per month or similar (see compound interest math, and how `e` limits max autocompounds to dust variation)
> 
> Either way, the observation is correct.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Anchor |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-anchor
- **GitHub**: https://github.com/code-423n4/2022-02-anchor-findings/issues/41
- **Contest**: https://code4rena.com/contests/2022-02-anchor-contest

### Keywords for Search

`vulnerability`

