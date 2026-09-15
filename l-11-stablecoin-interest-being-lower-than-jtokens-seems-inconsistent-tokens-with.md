---
# Core Classification
protocol: Apollon Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53864
audit_firm: Recon Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-22-Apollon_Report.md
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
  - Alex The Entreprenerd
---

## Vulnerability Title

[L-11] Stablecoin interest being lower than jTokens seems inconsistent + Tokens with different volatilities pay the same fee

### Overview

See description below for full details.

### Original Finding Content

**Impact**

Generally speaking jAssets will be more volatile and riskier than a stablecoin that denominates them

The logic for `getBorrowingRate` charges more for stableCoins than for jAssets

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/TroveManager.sol#L898-L901

```solidity
  function getBorrowingRate(bool isStableCoin) public view override returns (uint) {
    if (!isStableCoin) return borrowingFeeFloor;
    return _calcBorrowingRate(stableCoinBaseRate);
  }
```

It's also worth noting that all assets pay the same interest rate which means that they don't pay based on risk

**Mitigation**

Consider whether you should charge different fees for different assets so that the system is compensated for the additional risk it's taking

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Recon Audits |
| Protocol | Apollon Report |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-22-Apollon_Report.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

