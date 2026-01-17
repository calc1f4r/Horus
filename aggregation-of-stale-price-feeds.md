---
# Core Classification
protocol: API3 - Data Feed Proxy Combinators
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61344
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/api-3-data-feed-proxy-combinators/f5a9fb67-a96b-4db2-9828-623fd975d158/index.html
source_link: https://certificate.quantstamp.com/full/api-3-data-feed-proxy-combinators/f5a9fb67-a96b-4db2-9828-623fd975d158/index.html
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Yamen Merhi
  - Adrian Koegl
  - Hytham Farah
---

## Vulnerability Title

Aggregation of Stale Price Feed(s)

### Overview


The report discusses a bug found in the `ProductApi3ReaderProxyV1` contract, which returns the product of possibly stale data feed sources. The contract uses `block.timestamp` as the timestamp for the new value, which can lead to outdated prices and create an opportunity for attackers to exploit protocols using this wrapper. The recommendation is for protocols integrating this contract to consider using the smaller timestamp of the underlying feeds to avoid accepting stale price data. 

### Original Finding Content

**Update**
Acknowledged in: `e0595d4`. The client provided the following explanation:

> The ProductApi3ReaderProxyV1.read() function intentionally returns block.timestamp. This design choice by Api3 reflects that the timestamp accurately marks the on-chain computation time of the derived product value. Aggregating timestamps from underlying feeds is avoided due to complexity and the potential for misinterpretation. Integrators are responsible for checking the staleness of individual underlying feeds directly if required, as per Api3's integration guidelines (https://docs.api3.org/dapps/integration/contract-integration.html#using-timestamp). The contract's NatSpec documents this behavior.

**File(s) affected:**`ProductApi3ReaderProxyV1.sol`

**Description:** The `ProductApi3ReaderProxyV1` returns the product of possibly stale data feed sources. It returns `block.timestamp` as the timestamp for the new value, masking the age of the underlying data feeds. A consuming protocol utilizing this wrapper cannot apply their freshness policy to the returned price, leading to outdated prices and creating an opportunity for attackers. This could lead to protocols unintentionally accepting stale price data and attackers exploiting those protocols.

**Recommendation:** Protocols integrating the `ProductApi3ReaderProxyV1` may want to apply their freshness policy to the least recent price. Therefore, consider propagating the smaller timestamp of the underlying feeds (`MIN(timestamp1, timestamp2)`).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | API3 - Data Feed Proxy Combinators |
| Report Date | N/A |
| Finders | Yamen Merhi, Adrian Koegl, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/api-3-data-feed-proxy-combinators/f5a9fb67-a96b-4db2-9828-623fd975d158/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/api-3-data-feed-proxy-combinators/f5a9fb67-a96b-4db2-9828-623fd975d158/index.html

### Keywords for Search

`vulnerability`

