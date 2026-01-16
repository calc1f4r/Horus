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
solodit_id: 47447
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

Backstop Deposit Inflation

### Overview


The vulnerability in this report involves the first depositor in the backstop pool. The attacker can manipulate the price of the share token by minting just one share and making a large donation of backstop tokens to the pool. This artificially inflates the calculated price of the share token. During the deposit process, subsequent depositors may see their share tokens rounding down to zero, resulting in loss of funds. The recommended solution is to implement thresholds and permanently lock a portion of the initial deposit, or restrict donations to prevent manipulation. The issue has been fixed in version 26698 by restricting donations.

### Original Finding Content

## Vulnerability Analysis

The vulnerability involves the first depositor in backstop. This initial depositor may exploit the price of the share token. The attacker initiates the attack by calling `execute_deposit` to mint a single share. The attacker influences the share token’s price calculation by minting just one share.

```rust
> _ backstop/src/backstop/pool.rs
pub fn convert_to_shares(&self, tokens: i128) -> i128 {
    if self.shares == 0 {
        return tokens;
    }
    tokens
    .fixed_mul_floor(self.shares, self.tokens)
    .unwrap_optimized()
}
```

After minting a single share, the attacker executes a substantial donation of backstop tokens to the backstop pool using `execute_donate`. This combination of minting a single share and making a large donation of backstop tokens artificially inflates the calculated price of the share token. During the deposit process, subsequent depositors may observe their share tokens rounding down to zero, where the share token price is computed based on the product of the number of shares (self.shares) and the number of tokens (self.tokens). As indicated above, the `fixed_mul_floor` performs fixed-point multiplication with flooring.

The rounding down occurs when the computed number of shares falls below one, and the flooring operation adjusts it to zero. Consequently, depositors lose funds as their planned share allocation becomes zero, and the deposited funds fail to contribute to their share balance as anticipated.

## Remediation

Implement thresholds and permanently lock a portion of the initial deposit, or restrict donations, to prevent manipulation.

## Patch

Fixed in A6 26698 by restricting donations.

© 2024 Otter Audits LLC. All Rights Reserved. 10/22

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

