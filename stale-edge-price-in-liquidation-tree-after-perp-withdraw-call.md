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
solodit_id: 64551
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

Stale edge price in liquidation tree after perp withdraw call

### Overview


Summary: The bug report describes an issue with the `perp_withdraw` function, where after withdrawing funds from a perpetual position, the liquidation price is not updated. This can lead to incorrect margin call detection and liquidation priority. The recommended mitigation is to call `change_edge_px` at the end of the function. The bug has been fixed in a recent commit and has been verified.

### Original Finding Content

**Description:** In `perp_withdraw`, after withdrawing funds from a perpetual position, the function does not call `change_edge_px` to update the liquidation price(edge price) in the liquidation tree.

When funds are withdrawn, `info.funds` decreases, which affects `total_funds` and consequently the edge price. However, the liquidation trees(`long_px` and `short_px`) continue to store the outdated edge price because `change_edge_px` is never invoked.

**Impact:** After a withdrawal, the liquidation trees retain stale edge prices because `change_edge_px` is never called. This leads to incorrect margin call detection and liquidation priority.


**Recommended Mitigation:** `change_edge_px` should be invoked for the user withdrawing funds at the end of the function.

**Deriverse:** Fixed in commit [4f7bc8](https://github.com/deriverse/protocol-v1/commit/4f7bc8ac68325aa93b339ff91c0ac794ea17ffd9).

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

