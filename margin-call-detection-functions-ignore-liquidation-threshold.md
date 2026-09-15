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
solodit_id: 64512
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

Margin call detection functions ignore liquidation threshold

### Overview


The report describes a problem with two functions, `is_long_margin_call()` and `is_short_margin_call()`, that are used to detect margin calls in a financial system. These functions do not take into account a parameter called `liquidation_threshold`, which can lead to incorrect detection of margin calls. This can have several consequences, such as the system failing to freeze funds when it should, allowing users to withdraw more than they should, and triggering rebalancing even when margin calls are active. The report recommends fixing this issue by incorporating the `liquidation_threshold` into the margin call detection functions. The bug has been fixed in the code and verified by another team. 

### Original Finding Content

**Description:** The `is_long_margin_call()` and `is_short_margin_call()` functions used to determine whether margin calls are active do not account for the `liquidation_threshold` parameter. This creates a discrepancy between when the system detects margin calls and when actual margin call occur.
```rust
pub fn is_long_margin_call(&self) -> bool {
    let root = self.long_px.get_root::<i128>();
    if root.is_null() {
        false
    } else {
        self.state.header.perp_underlying_px < (root.max_node().key() >> 64) as i64
    }
}

pub fn is_short_margin_call(&self) -> bool {
    let root = self.short_px.get_root::<i128>();
    if root.is_null() {
        false
    } else {
        self.state.header.perp_underlying_px > (root.min_node().key() >> 64) as i64
    }
}
```
Actual Liquidation Logic:
```rust
pub fn check_long_margin_call(&mut self) -> Result<i64, DeriverseError> {
    let mut trades = 0;
    // Applies liquidation threshold
    let margin_call_px = (self.state.header.perp_underlying_px as f64
        * (1.0 - self.state.header.liquidation_threshold)) as i64;

    loop {
        let root = self.long_px.get_root::<i128>();
        if root.is_null() || trades >= MAX_MARGIN_CALL_TRADES {
            break;
        }
        let node = root.max_node();
        let px = (node.key() >> 64) as i64;

        // Compares edge price to threshold-adjusted price
        if px > margin_call_px {
            // ... liquidation logic ...
        }
    }
    Ok(trades)
}
```
Same `liquidation_threshold` is applied during `check_short_margin_call` also.


Margin call remains false even when margin calls are occurring, which causes the following issues:
* The `perp_spot_price_for_withdrawal` freezing mechanism fails to activate when it should.
* In the perpetual withdrawal flow, `get_avail_funds` is called only with `margin_call` false.
* Rebalancing is invoked even during active margin-call conditions.

**Impact:** This allows users to withdraw more than they should during active margin calls, effectively bypassing the intended withdrawal restrictions.

**Recommended Mitigation:** Use the liquidation threshold into margin-call detection functions to ensure accurate margin-call detection and prevent incorrect withdrawal and rebalancing behavior.

**Deriverse:** Fixed in commit [4f7bc8](https://github.com/deriverse/protocol-v1/commit/4f7bc8ac68325aa93b339ff91c0ac794ea17ffd9).

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

