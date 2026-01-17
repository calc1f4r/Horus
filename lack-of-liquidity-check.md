---
# Core Classification
protocol: Radiant Riz Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35160
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant-riz-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Lack of Liquidity Check

### Overview


The RizLendingPool contract has a bug where there are no checks in place to confirm if there is enough liquidity in the market when a user tries to withdraw or borrow assets. This can lead to the transaction failing, but it may not be obvious to the user. The team has acknowledged the issue and is considering implementing a check at the beginning of these functions to prevent this from happening. 

### Original Finding Content

In the `RizLendingPool` contract, within the [`withdraw`](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPool.sol#L184-L227) and the [`borrow` functions](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPool.sol#L264-L276), there are no checks which confirm the existence of liquidity in the market. In the case that a user attempts to withdraw or borrow more assets than the pool has, the transaction is likely to revert upon [transferring to the user](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPool.sol#L222). However, this may not be obvious to users. In addition, since tokens can implement arbitrary logic, it is possible that the call does not revert but the user receives significantly less than expected.


Consider implementing a check at the beginning of these functions to ensure that the desired withdrawal or borrow amount is available in the lending pool.


***Update:** Acknowledged, not resolved. The Radiant team stated:*



> *We think that we have never had any checks for token balances during deposits/withdrawals. Aave v2 does not have them either. We think we can accept that transactions are still reverting in case there are not enough token balances.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant Riz Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant-riz-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

