---
# Core Classification
protocol: Deriverse Dex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64540
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
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
finders_count: 4
finders:
  - RajKumar
  - Ctrus
  - Alexzoid
  - JesJupyter
---

## Vulnerability Title

Users incur losses when selling seats

### Overview


This bug report is about a problem in a program that calculates the price of a seat when it is bought or sold. The program uses a function called `get_reserve` to calculate the price, but the function returns a value that is too big for the program to handle. This causes the program to give incorrect prices, which could lead to losses for users and create opportunities for attackers to take advantage of the situation. The recommended solution is to fix the function so that it returns a more manageable value, and this has already been done in the latest version of the program. The bug has been verified and fixed.

### Original Finding Content

**Description:** Whenever a user buys or sells a seat, we calculate the seat price at that moment using the difference between `get_reserve` from the new/current position and the old position.
```rust
    pub fn get_place_buy_price(supply: u32, dec_factor: u32) -> Result<i64, DeriverseError> {
        let df = get_dec_factor(dec_factor);
        Ok(get_reserve(supply + 1, df)? - get_reserve(supply, df)?)
    }

    pub fn get_place_sell_price(supply: u32, dec_factor: u32) -> Result<i64, DeriverseError> {
        let df = get_dec_factor(dec_factor);
        Ok(get_reserve(supply, df)? - get_reserve(supply - 1, df)?)
    }
```
The `get_reserve` function returns an i64, whose maximum value is 9223372036854775807. and, in `get_reserve` calculation is done in f64 and if the result in f64 exceeds this limit, casting it back to i64 will clamp the value to the maximum i64 value (9223372036854775807).

Example: The seat price from 249,995 to 250,000, the value becomes zero when `crncy_token_decs_count` is 9.


**Impact:** This leads to unexpected behavior, which can result in losses for regular users and create opportunities for an attacker to extract value if `perp_clients_count` is close 250000.



**Recommended Mitigation:** `get_reserve` should return f64. After computing the difference between the results of both `get_reserve` calls, we can then convert the final value back to i64 for more accurate result.

**Deriverse:** Fixed in commit [c8d26d](https://github.com/deriverse/protocol-v1/commit/c8d26d57c1d9f24add2ed449f422d79ec983c13a).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Deriverse Dex |
| Report Date | N/A |
| Finders | RajKumar, Ctrus, Alexzoid, JesJupyter |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

