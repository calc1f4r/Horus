---
# Core Classification
protocol: StakeDAO_2025-07-21
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63603
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
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

[M-04] Deploy functions is vulnerable to DoS attack vectors

### Overview


This bug report is about a problem that occurs when creating a market in the morpho blue platform. The issue is caused by a lack of checks for market parameters, which can be exploited by a malicious actor to front-run the market and manipulate its parameters. The severity and likelihood of this bug are both considered medium. The report recommends implementing checks to ensure that a market has not already been created before proceeding with the creation process.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

While creating the morpho market, there are several checks for market parameters in morpho blue. If the market is already created with the same parameters, it will fail in the required line.

```solidity
        require(isIrmEnabled[marketParams.irm], ErrorsLib.IRM_NOT_ENABLED);
        require(isLltvEnabled[marketParams.lltv], ErrorsLib.LLTV_NOT_ENABLED);
@>      require(market[id].lastUpdate == 0, ErrorsLib.MARKET_ALREADY_CREATED);

        // Safe "unchecked" cast.
        market[id].lastUpdate = uint128(block.timestamp);
```

Malicious actor can simulate the transaction and frontrun the market parameters with createMarket function. In here, oracle address should be determined by attacker in order to execute the attack, but it's already very easy because the address of oracle depends on the contract's nonce and address.

## Recommendations

Check whether the market has already been created or not.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StakeDAO_2025-07-21 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

