---
# Core Classification
protocol: 1inch Fusion
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58727
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/1-inch-fusion/46247b92-ba5f-4f49-a397-76f7867ff4a4/index.html
source_link: https://certificate.quantstamp.com/full/1-inch-fusion/46247b92-ba5f-4f49-a397-76f7867ff4a4/index.html
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
finders_count: 3
finders:
  - Paul Clemson
  - Yamen Merhi
  - Hamed Mohammadi
---

## Vulnerability Title

Potential Bypass of Fees Parameters in Order Creation

### Overview


The client has acknowledged an issue in the fusion-swap program where makers are not strictly required to set protocol and integrator fees, potentially allowing them to receive a higher amount than intended. This could be exploited by malicious makers, and while takers are incentivized to only fill orders with correct fee configurations, there is still a risk. The recommendation is to either have the protocol owner set the protocol fee or implement on-chain validations for fees. 

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Noted

**File(s) affected:**`fusion-swap/src/lib.rs`

**Description:** In the `Create` context of the fusion-swap program, makers are required to specify protocol fee and integrator fee parameters as well as their corresponding associated token accounts (protocol_dst_ata and integrator_dst_ata). However, the current implementation does not enforce these parameters strictly. This means that a maker can potentially create an order without setting protocol or integrator fees or by misconfiguring the protocol_dst_ata. Consequently, the maker might avoid fee deductions and receive a higher net amount than intended by the protocol fee design. Note that even if the UI enforces fee parameters, malicious makers could bypass these checks by directly interacting with the program.

While this issue might be less impactful because takers (or resolvers) must be whitelisted by the protocol and are incentivized to fill only orders with correct fee configurations, it still poses a risk. In practice, resolvers may refuse to fill orders that do not have fees applied to the correct token accounts, but the absence of on-chain enforcement or fixed values allows makers to manipulate these parameters.

**Recommendation:** Consider fixing the protocol fee to be set by the protocol owner, and having the integrator fee set in the UI or clearly documenting this risk in the protocol specification. Alternatively, if the protocol fees are intended to be set by the makers, implement on-chain validations that enforce a defined minimum and maximum for each fee, and ensure that the sum of `protocol_fee` and `integrator_fee` remains below a specified threshold, as outlined in [IFS-8](https://certificate.quantstamp.com/full/1-inch-fusion/46247b92-ba5f-4f49-a397-76f7867ff4a4/index.html#findings-qs8).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | 1inch Fusion |
| Report Date | N/A |
| Finders | Paul Clemson, Yamen Merhi, Hamed Mohammadi |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/1-inch-fusion/46247b92-ba5f-4f49-a397-76f7867ff4a4/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/1-inch-fusion/46247b92-ba5f-4f49-a397-76f7867ff4a4/index.html

### Keywords for Search

`vulnerability`

