---
# Core Classification
protocol: 88mph v3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17602
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/88mph.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/88mph.pdf
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
finders_count: 2
finders:
  - Dominik Teiml
  - Maximilian Krüger
---

## Vulnerability Title

The interest oracle’s money market is not validated upon DInterest initialization

### Overview


This bug report concerns a data validation issue in the xMPH.sol and DInterest.sol contracts. A DInterest contract must have the same money market as its interest oracle, however, DInterest.__DInterest_init does not check this invariant. This could lead to users receiving significantly less interest than they would by using Aave directly. 

In the short term, the report recommends adding require(interestOracle.moneyMarket() == moneyMarket, "BAD_ORACLE") to DInterest.__DInterest_init. Alternatively, it suggests removing moneyMarket from DInterest so the system always fetches moneyMarket from interestOracle.moneyMarket(). 

In the long term, it suggests avoiding the use of duplicated states within the protocol, as they can become inconsistent.

### Original Finding Content

## Data Validation

## Target: xMPH.sol

### Difficulty: High

## Target: DInterest.sol

### Description
A `DInterest` contract must have the same money market as its interest oracle. The function that sets the interest oracle checks this invariant (Figure 1.1).

```solidity
function setInterestOracle(address newValue) external onlyOwner {
    require(newValue.isContract(), "NOT_CONTRACT");
    interestOracle = IInterestOracle(newValue);
    require(interestOracle.moneyMarket() == moneyMarket, "BAD_ORACLE");
    emit ESetParamAddress(msg.sender, "interestOracle", newValue);
}
```

**Figure 1.1:** `setInterestOracle` in `DInterest.sol#L1483-L1488`

However, `DInterest.__DInterest_init` does not check this invariant. A mistake during initialization could cause a `DInterest` to have a different money market than its interest oracle. As a result, the system could provide incorrect interest rates, and either the users or the protocol could lose funds.

### Exploit Scenario
Alice, a developer, deploys a new `DInterest` for DAI and AAVE and calls `DInterest.initialize`. She passes in the Aave money market address as one parameter and accidentally passes in the Yearn interest oracle address as the other. For some time, Yearn yields significantly lower interest than Aave. As a result, users receive significantly less interest than they would by using Aave directly.

### Recommendations
- **Short term:** Add `require(interestOracle.moneyMarket() == moneyMarket, "BAD_ORACLE")` to `DInterest.__DInterest_init`. Alternatively, remove `moneyMarket` from `DInterest` so that the system always fetches `moneyMarket` from `interestOracle.moneyMarket()`.
- **Long term:** Avoid the use of duplicated states within the protocol, as they can become inconsistent.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | 88mph v3 |
| Report Date | N/A |
| Finders | Dominik Teiml, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/88mph.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/88mph.pdf

### Keywords for Search

`vulnerability`

