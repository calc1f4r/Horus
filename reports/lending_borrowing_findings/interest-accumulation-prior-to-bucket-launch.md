---
# Core Classification
protocol: Primex Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59041
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html
source_link: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html
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
  - Jennifer Wu
  - Andy Lin
  - Adrian Koegl
  - Hytham Farah
---

## Vulnerability Title

Interest Accumulation Prior to Bucket Launch

### Overview


The team has fixed a bug in the `Bucket.sol` file that caused lenders to earn interest on their deposited funds before the bucket had launched. This was not intended according to the documentation, which stated that lenders would only start earning interest after the stabilization period. The bug was triggered when a user deposited and withdrew funds before the bucket had launched, causing interest to accumulate incorrectly. The team has recommended adding a condition check in the `withdraw()` function to prevent this from happening.

### Original Finding Content

**Update**
The team fixed the issue as recommended in the commit `541096b`. Notably, the client also adjusted the bar to register as zero when "ur" holds a zero value, a modification unrelated to the current fix.

**File(s) affected:**`Bucket.sol`

**Description:** According to the [documentation](https://docs.primex.finance/guides/credit-buckets/liquidity-mining), it states that "During the stabilization period, Traders can now borrow funds from the Credit Bucket, and Lenders start earning interest on the liquidity they provide for margin trading." Based on this information, we assume that lenders only start earning interest after moving to the stabilization period, which occurs when the bucket launches. Additionally, the implementation of `_depositLM()` does not update indexes and rates. However, the `withdraw()` function allows lenders to withdraw funds before the bucket launches. Within this function, both `_updateIndexes()` and `_updateRates()` are called, causing the index to be updated and start accumulating before the bucket launches.

**Exploit Scenario:**

 Alice deposits 101 into a bucket and immediately withdraws 1 to trigger interest accumulation. The bucket starts owing Alice lending interest, despite no borrowing activities occurring to repay the accrued interest.

**Recommendation:** Add a condition check in the `withdraw()` function so that it only calls the `_updateIndexes()` and `_updateRates()` functions after the bucket has launched.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Primex Finance |
| Report Date | N/A |
| Finders | Jennifer Wu, Andy Lin, Adrian Koegl, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html

### Keywords for Search

`vulnerability`

