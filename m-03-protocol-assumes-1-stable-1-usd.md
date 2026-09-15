---
# Core Classification
protocol: LayerZeroZROClaim
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37818
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/LayerZeroZROClaim-security-review.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Protocol assumes 1 Stable = 1 USD

### Overview


The bug report is about a medium severity issue in the ClaimCore contract where the prices for USDC and USDT are hardcoded to 1 USD. This means that during times of stablecoin volatility, users may be able to contribute less stablecoins for the same amount of ZRO. The report recommends using a chainlink oracle to fetch the stablecoin prices instead.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In the ClaimCore contract constructor, the prices for USDC and USDT are hardcoded to 1 USD:

```solidity
        if (_stargateUsdc != address(0)) {
            numeratorUsdc = 1 * 10 ** (IERC20Metadata(IOFT(_stargateUsdc).token()).decimals() - 1);
        }

        if (_stargateUsdt != address(0)) {
            numeratorUsdt = 1 * 10 ** (IERC20Metadata(IOFT(_stargateUsdt).token()).decimals() - 1);
        }
```

This assumption can lead to problems during stablecoin volatility events. For instance, if users are donating 1000 USDC (equivalent to 1000 USD) in exchange for 1000 ZRO, a depeg event where USDC drops to 0.8 USD means users can contribute 1000 USDC (now worth 800 USD) for the same 1000 ZRO.

## Recommendations

Consider using a chainlink oracle to fetch the stables prices.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | LayerZeroZROClaim |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/LayerZeroZROClaim-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

