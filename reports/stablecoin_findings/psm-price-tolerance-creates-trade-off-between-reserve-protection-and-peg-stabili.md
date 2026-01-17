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
solodit_id: 63391
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

PSM Price Tolerance Creates Trade-Off Between Reserve Protection and Peg Stability

### Overview

See description below for full details.

### Original Finding Content

**Update**
Acknowledged by the client. The client provided the following explanation:

> Will set it around 1% to deal with only extraordinary circumstances.

**File(s) affected:**`bucket_psm/sources/pool.move`

**Description:** The `PSM`'s price tolerance mechanism, which disables swaps when the oracle price deviates beyond a threshold from $1, presents a fundamental design trade-off that lacks clear resolution. This feature has both protective and destabilizing effects that become particularly significant during market stress.

From a reserve protection perspective, the threshold serves as a critical safeguard. When `USDB` depegs significantly, unrestricted `PSM` swaps would allow arbitrageurs to drain the entire reserve by exchanging devalued `USDB` for fully-valued stablecoins at a 1:1 rate. Given the protocol's lack of bad debt recovery mechanisms, preserving `PSM` reserves becomes essential for maintaining any semblance of stability. The threshold effectively acts as a circuit breaker, preventing complete reserve depletion during severe depegging events.

However, this same mechanism may accelerate the very crisis it aims to prevent. When `USDB` begins depegging and crosses the threshold, the PSM becomes completely non-functional, eliminating the primary arbitrage mechanism that would normally restore the peg. Without `PSM` support, even minor depegs could spiral out of control. Users observing the disabled `PSM` might panic, rushing to close their `CDP`s before conditions worsen, creating selling pressure that drives `USDB` further from its peg. This self-reinforcing cycle could transform a manageable deviation into a downwards spiral.

**Recommendation:** The optimal approach depends on broader protocol design decisions. If bad debt recovery mechanisms are implemented, consider removing or significantly increasing the price tolerance to prioritize peg stability. The `PSM` could then fulfill its role as a stability mechanism even during stress, with bad debt handled through separate systems. Alternatively, if maintaining the threshold, implement graduated responses rather than binary on/off states - for example, increasing fees progressively as prices deviate, or limiting swap sizes rather than disabling entirely. This would preserve some stabilizing effect while still protecting reserves during extreme events.

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

