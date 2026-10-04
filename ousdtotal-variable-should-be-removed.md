---
# Core Classification
protocol: Archimedes Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50593
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/archimedes/archimedes-finance-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/archimedes/archimedes-finance-smart-contract-security-assessment
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

OUSDTOTAL VARIABLE SHOULD BE REMOVED

### Overview

See description below for full details.

### Original Finding Content

##### Description

Struct CDP is defined within `CDPosition.sol` contract. It contains information about positions, such as the initial `LvUSD` amount borrowed, the `OUSD` shares held by the position, etc.

However, it has been detected that `oUSDTotal` is declared, used, and never updated, which could cause unpredictable behavior or even render positions unwindable.

According to the comments in the code, this variable holds the total `OUSD` amount held by the position, including the initial `OUSD` amount staked (principle), the leverage obtained, and the profits obtained by interest or rebases. This information could also be retrieved using `CDP.shares`.

However, this variable is never updated, so the `oUSDTotal` value will be stuck forever with the principle + leverage `OUSD` amount. Also, this variable is incorrectly used in a require statement to assert that no more `OUSD` than the available is used:

#### CDPosition.sol

```
    function withdrawOUSDFromPosition(uint256 nftID, uint256 oUSDAmountToWithdraw) external nftIDMustExist(nftID) nonReentrant onlyExecutive {
        require(_nftCDP[nftID].oUSDTotal >= oUSDAmountToWithdraw, "Insufficient OUSD balance");
        _nftCDP[nftID].oUSDTotal -= oUSDAmountToWithdraw;
    }

```

When following the function logic flow, it has been detected that `oUSDTotal` is compared to `oUSDAmountToWithdraw`, that is, the `OUSD` amount remaining under the position after swapping `OUSD` for `LvUSD` to repay the leverage obtained. After the comparison, `oUSDAmountToWithdraw` is subtracted from `oUSDTotal`, leaving its value inconsistent.

Code Location
-------------

#### CDPosition.sol

```
    struct CDP {
        uint256 oUSDPrinciple; // Amount of OUSD originally deposited by user
        uint256 oUSDInterestEarned; // Total interest earned (and rebased) so far
        uint256 oUSDTotal; // Principle + OUSD acquired from selling borrowed lvUSD + Interest earned
        uint256 lvUSDBorrowed; // Total lvUSD borrowed under this position
        uint256 shares; // Total vault shares allocated to this position
    }

```

##### Score

Impact: 3  
Likelihood: 1

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Archimedes Finance |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/archimedes/archimedes-finance-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/archimedes/archimedes-finance-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

