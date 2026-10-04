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
solodit_id: 64503
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
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
finders_count: 4
finders:
  - RajKumar
  - Ctrus
  - Alexzoid
  - JesJupyter
---

## Vulnerability Title

Fee Discount Calculation Ignores Base Currency Value Differences

### Overview


The fee discount calculation in `fees_deposit` is not taking into account the actual value differences between different base currencies. This means that users depositing low-value base currencies can receive the same discount as users depositing high-value currencies, even though there is a significant difference in their actual value. This issue becomes more problematic as the protocol expands to support additional base currencies in the future. To fix this, a value normalization factor will be stored for each base currency to represent its relative value. This bug has been fixed in the Deriverse protocol and verified by Cyfrin.

### Original Finding Content

**Description:** The fee discount calculation in `fees_deposit` uses the raw token amount divided by decimal factor, without considering the actual value differences between base currencies. This can lead to unfair discount distribution when multiple base currencies with different values are supported.

In `fees_deposit`, the `prepayment` amount is calculated as:
```rust
let dec_factor = get_dec_factor(community_state.base_crncy[crncy_index].decs_count) as f64;
let prepayment = data.amount as f64 / dec_factor;
let fees_discount = community_state.fees_discount(prepayment);
```
The calculation only normalizes for decimal places but does not account for the actual value of different base currencies. For example:
- Depositing 1000 USDC (worth $1000)
- Depositing 1000 tokens of a low-value base currency (worth $0.001 each = $1 total)
- Deposit 1000 SOL would be quite impossible

Both would receive the same discount rate, despite a 1000x value difference.

This becomes more problematic as **the protocol expands to support additional base currencies through governance, as mentioned in the documentation. Different base currencies may have vastly different market values, but the current implementation treats them equally based on raw token count.**

From the documentation https://deriverse.gitbook.io/deriverse-v1/launchpad/launchpad#supported-base-currency:

```plaintext
Supported Base Currency
Current Support:

USDC: Circle USD Stablecoin

Future Expansion:

- Additional base currencies may be added through governance

- Multi-denomination support under consideration

- Community can propose new base currencies
```

**Impact:** Unfair discount distribution: Users depositing low-value base currencies can achieve the same discount thresholds as users depositing high-value currencies with much less actual value

**Recommended Mitigation:** Store a value normalization factor for each base currency that represents its relative value.

**Deriverse:** Fixed in commit [35602457](https://github.com/deriverse/protocol-v1/commit/35602457ebebccacca51749aad6270077724fb38).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

