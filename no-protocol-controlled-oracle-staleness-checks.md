---
# Core Classification
protocol: Bucket Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63385
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html
source_link: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html
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
finders_count: 3
finders:
  - Hamed Mohammadi
  - Adrian Koegl
  - Rabib Islam
---

## Vulnerability Title

No Protocol-Controlled Oracle Staleness Checks

### Overview

See description below for full details.

### Original Finding Content

**Update**
Fixed by enforcing freshness in `pyth.move`. It should be noted, however, that these freshness checks depend on the implementation of the respective price feed module added in the future. Addressed in: `31552fce89681883823157ac001f85ead6abf662`.

**File(s) affected:**`bucket_oracle/sources/collector.move`, `price_rules/pyth_rule/sources/pyth_rule.move`

**Description:** The protocol delegates price freshness validation entirely to external price providers rather than enforcing its own staleness requirements. Currently, only Pyth is implemented as a price source, and the protocol relies on Pyth's internal staleness checks without the ability to configure acceptable price age limits. This dependency prevents the protocol from adjusting freshness requirements based on market conditions or risk parameters. Furthermore, price feed providers, such as Pyth, will panic if the price is outdated, leaving the protocol unable to revert to other oracle providers. The lack of protocol-level control also complicates adding new price sources with different staleness guarantees.

**Recommendation:** Implement protocol-controlled staleness checks using `pyth::get_price_no_older_than()` with configurable maximum age parameters during `collector::collect()`. This allows the protocol to enforce consistent freshness requirements across all price sources and gracefully handle stale prices by falling back to alternative oracles rather than reverting transactions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Bucket Protocol V2 |
| Report Date | N/A |
| Finders | Hamed Mohammadi, Adrian Koegl, Rabib Islam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html

### Keywords for Search

`vulnerability`

