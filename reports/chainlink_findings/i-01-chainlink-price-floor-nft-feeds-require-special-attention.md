---
# Core Classification
protocol: Fungify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31831
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
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
finders_count: 1
finders:
  - Zach Obront
---

## Vulnerability Title

[I-01] Chainlink Price Floor NFT feeds require special attention

### Overview

See description below for full details.

### Original Finding Content

Chainlink provides a categorization of the security of all their feeds. As we can see on the [NFT Floor Price Feed](https://docs.chain.link/data-feeds/nft-floor-price/addresses?network=ethereum&page=1) page, each of the NFT Floor feeds is considered a "Specialized Feed".

Their documentation explains:

> [Specialized feeds] are purpose-built feeds that might rely heavily on contracts maintained by external entities. Typical users of these feeds are large institutional users with deep expertise in the market space they operate in.
> These feeds are monitored and well-supported, but they might not meet the same levels of resiliency as the above categories. We strongly advise you to speak with the Chainlink Labs team to understand their use cases, properties, and associated risks.

While they appear to be safe, Chainlink does not appear to publicly share the exact methodology and associated risks for this type of feed.

**Recommendation**

Contact Chainlink's team via their [Contact Page](https://chain.link/contact?ref_id=DataFeed) to get an explanation of risks they foresee in NFT Price Floor Feeds and consider whether any of these risks may be a problem for the protocol.

**Review**

Confirmed: "Our team communicates with Chainlink regularly and have discussed the NFT feeds at length."

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Fungify |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

