---
# Core Classification
protocol: FactoryDAO
chain: everychain
category: dos
vulnerability_type: dust

# Attack Vector Details
attack_type: dust
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2261
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-factorydao-contest
source_link: https://code4rena.com/reports/2022-05-factorydao
github_link: https://github.com/code-423n4/2022-05-factorydao-findings/issues/54

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - dust
  - dos

protocol_categories:
  - dexes
  - cdp
  - yield
  - rwa
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - 0xf15ers
  - pedroais
  - 0x52
  - AuditsAreUS
---

## Vulnerability Title

[M-18] DoS: Attacker may significantly increase the cost of withdrawExcessRewards() by creating a significant number of excess receipts

### Overview


This bug report is about a potential Denial of Service (DoS) attack on the function withdrawExcessRewards() in the PermissionlessBasicPoolFactory.sol contract. An attacker could create a large number of accounts with minimal value deposits, which would need to be withdrawn before the owner can call withdrawExcessRewards(). This would result in an unbounded amount of gas costs for the owner, especially if the gas price has increased since the deposits were made. 

The recommended mitigation steps are to either add a minimum deposit amount for each pool, or to allow the owner to call withdrawExcessRewards() given some other criteria such as a fix period of time has passed since the end of the auction, and 90% of the deposits have been withdrawn. This criteria can be customised according to the design team's needs.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-05-factorydao/blob/db415804c06143d8af6880bc4cda7222e5463c0e/contracts/PermissionlessBasicPoolFactory.sol#L245


## Vulnerability details

## Impact

An attacker may cause a DoS attack on `withdrawExcessRewards()` by creating a excessive number of `receipts` with minimal value. Each of these receipts will need to be withdrawn before the owner can call `withdrawExcessRewards()`. 

The impact is the owner would have to pay an unbounded amount of gas to `withdraw()` all the accounts and receive their excess funds.

## Proof of Concept

`withdrawExcessRewards()` has the requirement that `totalDepositsWei` for the pool is zero before the owner may call this function as seen on line 245.

```solidity
        require(pool.totalDepositsWei == 0, 'Cannot withdraw until all deposits are withdrawn');
```

`pool.totalDepositsWei` is added to each time a user calls `deposit()`. It is increased by the amount the user deposits. There are no restrictions on the amount that may be deposited as a result a user may add 1 wei (or the smallest unit on any currency) which has negligible value.

The owner can force withdraw these accounts by calling `withdraw()` so long as `block.timestamp > pool.endTime`. They would be required to do this for each account that was created.

This could be a significant amount of gas costs, especially if the gas price has increased since the attacker originally made the deposits.

## Recommended Mitigation Steps

Consider adding a minimum deposit amount for each pool that can be configured by the pool owner.

Alternatively, allow the owner to call `withdrawExcessRewards()` given some other criteria such as 
- A fix period of time (e.g. 1 month) has passed since the end of the auction; and
- 90% of the deposits have been withdrawn
These criteria can be customised as desired by the design team.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | FactoryDAO |
| Report Date | N/A |
| Finders | 0xf15ers, pedroais, 0x52, AuditsAreUS |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-factorydao
- **GitHub**: https://github.com/code-423n4/2022-05-factorydao-findings/issues/54
- **Contest**: https://code4rena.com/contests/2022-05-factorydao-contest

### Keywords for Search

`Dust, DOS`

