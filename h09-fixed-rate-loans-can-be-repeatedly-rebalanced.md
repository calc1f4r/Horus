---
# Core Classification
protocol: Aave Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11605
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/aave-protocol-audit/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H09] Fixed-rate loans can be repeatedly rebalanced

### Overview


This bug report is about a flaw in the code that affects the fixed-rate loans. The code is intended to rebalance any loan if the rate falls outside an acceptable range, with the lower boundary being the current liquidity rate and the upper boundary being a configurable percentage higher than the reserve’s fixed borrow rate. However, the upper threshold is set below the reserve’s fixed borrow rate, meaning that new loans will start outside the acceptable range and will remain that way after rebalancing. This essentially means that “fixed-rate loans” are actually vulnerable to any change in the market rate. 

The issue has been fixed in Merge Request #44, after being discussed with the Aave team. The team concluded that although the logic flaw exposed caused unwanted behavior that needed to be fixed, it did not pose any security risk for the protocol and is actually ending up in a potentially acceptable use case.

### Original Finding Content

Any user’s fixed-rate loan [can be rebalanced](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L493) if the rate falls outside an acceptable range. The lower boundary of this range is the current liquidity rate, while the upper boundary is intended to be a [configurable percentage](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/configuration/LendingPoolParametersProvider.sol#L38-40) higher than the reserve’s fixed borrow rate.


However, the upper threshold is [set below the reserve’s fixed borrow rate](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L520-525). This means that new loans will start outside the acceptable range and will remain that way after rebalancing so that “fixed-rate loans” are actually vulnerable to any change in the market rate.


Consider redefining the upper threshold to be higher than the reserve rate (by the configurable down-rate delta parameter) rather than lower by that percentage. Related issues that must be taken into consideration are [**“[H06] It is impossible to rebalance another account’s fixed borrow rate”**](#h06) and [**“[C04] Rogue borrower can manipulate other account’s borrow balance”**](#c04).


**Update**: *Fixed in [MR#44](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/44/diffs). This issue was originally labeled as Critical since it implies fixed-rate loans can be made to follow the variable rate. After discussing with the Aave team, it has been downgraded to High. In Aave’s words:*



> 
>  “Although the logic flaw exposed caused unwanted behavior that needed fix, this issue didn’t actually pose any security risk for the protocol, and is actually ending up in a potentially acceptable use case”.
> 
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Aave Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/aave-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

