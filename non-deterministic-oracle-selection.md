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
solodit_id: 63380
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

Non-Deterministic Oracle Selection

### Overview

See description below for full details.

### Original Finding Content

**Update**
Fixed by the client by requiring that users need to collect the prices of _all_ price feeds. This prevents users from "cherry-picking" favorable prices. Addressed in: `d8badbbeea0e666415187a47f065c9c0f3b2c6c0`.

**File(s) affected:**`bucket_oracle/sources/aggregator.move`

**Description:** The oracle system allows users to select different subsets of price feeds to reach the weight threshold, enabling them to obtain multiple valid prices within the same transaction. While we did not identify a direct exploitation path in the current CDP and PSM modules (which only use prices for health checks and divergence thresholds), this non-deterministic design violates oracle best practices and could become exploitable if the protocol evolves. Furthermore, sophisticated users can currently pick a subset of oracles that is most advantageous to them.

The current implementation enables scenarios where a user with oracles weighted 1/1/1 and a threshold of 2 can choose between any two, potentially obtaining different aggregated prices. This flexibility becomes particularly concerning during periods of high volatility when oracle prices naturally diverge due to update delays or network conditions.

**Recommendation:** Implement a deterministic oracle selection model following industry standards. A robust approach uses primary, secondary, and fallback oracles where the primary and secondary prices must agree within a threshold, with the fallback used only when they diverge. This ensures price consistency by requiring two out of three oracles to provide similar values.

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

