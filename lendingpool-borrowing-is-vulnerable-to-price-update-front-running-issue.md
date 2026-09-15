---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57342
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
  - infect3d
---

## Vulnerability Title

`LendingPool` borrowing is vulnerable to price update front-running issue

### Overview

See description below for full details.

### Original Finding Content

## Summary

Users can front-run the price update of a house to deposit the NFT before the update and borrow up to maximum capacity. Then when the price update happens, the loan is already undercollateralized, allowing the user to leave with an instant profit and not be impacted by the decreased value of the NFT.

## Vulnerability details

A user hold a HouseNFT and detect that its price will drop.\
The attacker front-run the price update to [deposit](https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/core/pools/LendingPool/LendingPool.sol#L225-L225) this houseNFT and [borrow](https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/core/pools/LendingPool/LendingPool.sol#L325-L325) up to maximum capacity in a same transaction, to finally let the price update be executed.\
If the house price drop is bigger than the collateralization ratio protection\[1], the attacker would have borrowed more than what the house NFT is worth after the update, allowing him to leave with the profit and never repay its loan.

\[1] *The* *[collateralization ratio protection](https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/core/pools/LendingPool/LendingPool.sol#L344-L344)* *is represented by the variable* *`liquidationThreshold`, which can be updated to* *[any value between 0% and 100%](https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/core/pools/LendingPool/LendingPool.sol#L129-L129)*, making that attack 

## Impact

Attackers can create undercollateralized positions that he has detected at risk, and leave with a profit.

## Recommended Mitigation Steps

Do not allow to call `depositNFT` and `borrow` in a same block.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | infect3d |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

