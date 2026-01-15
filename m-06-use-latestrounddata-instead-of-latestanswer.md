---
# Core Classification
protocol: Radiant June
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36377
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Radiant-security-review-June.md
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

[M-06] Use `latestRoundData` instead of `latestAnswer`

### Overview


The `UniV3TokenizedLp` is using a method called `latestAnswer()` to get the last oracle price. However, this method does not allow for checking if the data is fresh. It is recommended to use a different method called `latestRoundData()` which allows for extra validations. These validations include checking if the price is greater than 0, if the round is complete, and if the price is not stale. It is important to use these additional checks to ensure accurate and up-to-date data from the oracle. 

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** Medium

**Description**

`UniV3TokenizedLp` is calling `latestAnswer()` to get the last oracle price. This method will return the last value, but you will not be able to check if the data is fresh. On the other hand, calling the method `latestRoundData()` allows you to run some extra validations.

**Recommendations**

Consider using latestRoundData() with the following additional checks:

```solidity
 (
          roundId,
          rawPrice,
          ,
          updateTime,
          answeredInRound
        ) = IChainlinkAdapter(_oracle).latestRoundData();
        require(rawPrice > 0, "Chainlink price <= 0");
        require(updateTime != 0, "Incomplete round");
        require(answeredInRound >= roundId, "Stale price");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Radiant June |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Radiant-security-review-June.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

