---
# Core Classification
protocol: Reserve Protocol Solana DTFs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55598
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-04-reserve-solana-dtfs-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-04-reserve-solana-dtfs-securityreview.pdf
github_link: none

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
finders_count: 2
finders:
  - Samuel Moelius
  - Coriolan Pinhas
---

## Vulnerability Title

add_tokens_to_basket does not check whether any of the values in mints is Pubkey::default()

### Overview

See description below for full details.

### Original Finding Content

## Difficulty: Low

## Type: Data Validation

## Description
The `add_tokens_to_basket` function takes a vector of public keys and adds them to the `token_amounts` array. The function uses `Pubkey::default()` as a sentinel value to represent an empty slot in the array. The function should check its inputs for this value and reject them when they are present.

The relevant code appears in Figure 10.1. Consider the case where `token_amounts` is full, and the argument, `mints`, consists of just one value, `Pubkey::default()`. Arguably, the function could return success. Instead, the function will return failure because no free slots can be found in `token_amounts`.

```rust
pub fn add_tokens_to_basket(&mut self, mints: &Vec<Pubkey>) -> Result<()> {
    for mint in mints {
        if self.token_amounts.iter_mut().any(|ta| ta.mint == *mint) {
            // Continue if already exists or error out?
            continue;
        } else if let Some(slot) = self
            .token_amounts
            .iter_mut()
            .find(|ta| ta.mint == Pubkey::default())
        {
            slot.mint = *mint;
            slot.amount_for_minting = 0;
            slot.amount_for_redeeming = 0;
        } else {
            // No available slot found, return an error
            return Err(error!(MaxNumberOfTokensReached));
        }
    }

    Ok(())
}
```

Figure 10.1: Definition of `add_tokens_to_basket`  
(dtfs-solana/programs/folio/src/utils/accounts/folio_basket.rs#49–69)

## Exploit Scenario
Alice calls `mint_initial_shares` but passes `Pubkey::default()` as the mint by mistake. The call succeeds despite the invalid mint value.

## Recommendations
- **Short term**: Have `add_tokens_to_basket` check its argument for `Pubkey::default()` values and reject them when they are present. This will alert the caller to the problem when such values are passed by accident.

- **Long term**: If a function takes public keys as arguments and uses `Pubkey::default()` as a sentinel value, have the function check for `Pubkey::default()` among its arguments. This will present users with more predictable and less error-prone interfaces.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Reserve Protocol Solana DTFs |
| Report Date | N/A |
| Finders | Samuel Moelius, Coriolan Pinhas |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-04-reserve-solana-dtfs-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-04-reserve-solana-dtfs-securityreview.pdf

### Keywords for Search

`vulnerability`

