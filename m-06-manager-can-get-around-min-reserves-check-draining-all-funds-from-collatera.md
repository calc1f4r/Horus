---
# Core Classification
protocol: prePO
chain: everychain
category: uncategorized
vulnerability_type: bypass_limit

# Attack Vector Details
attack_type: bypass_limit
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6068
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-prepo-contest
source_link: https://code4rena.com/reports/2022-12-prepo
github_link: https://github.com/code-423n4/2022-12-prepo-findings/issues/254

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - bypass_limit

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 14
finders:
  - csanuragjain
  - 8olidity
  - Trust
  - hihen
  - cccz
---

## Vulnerability Title

[M-06] Manager can get around min reserves check, draining all funds from Collateral.sol

### Overview


This bug report outlines a vulnerability in the WithdrawHook.sol smart contract, which is part of the Prepo-monorepo. This vulnerability allows a manager to bypass the minimum reserve balance by making a large deposit, taking a manager withdrawal, and then withdrawing their deposit. 

The proof of concept provided in the report outlines a scenario where the token has a balance of 100, deposits of 1000, and a reserve percentage of 10%. In this situation, the manager should not be able to make any withdrawal. However, the bug allows them to do so by calling the `deposit()`, `managerWithdraw()`, and `withdraw()` functions in succession. This allows the manager to drain the balance of the contract all the way to zero, avoiding the intended restrictions. 

The bug was identified through manual review. The recommended mitigation steps include adding a check on the reserves in the `withdraw()` function, as well as the `managerWithdraw()` function. This will ensure that the minimum reserve balance is not bypassed.

### Original Finding Content


When a manager withdraws funds from Collateral.sol, there is a check in the `managerWithdrawHook` to confirm that they aren't pushing the contract below the minimum reserve balance.

```solidity
require(collateral.getReserve() - _amountAfterFee >= getMinReserve(), "reserve would fall below minimum");
```

However, a similar check doesn't happen in the `withdraw()` function.

The manager can use this flaw to get around the reserve balance by making a large deposit, taking a manager withdrawal, and then withdrawing their deposit.

### Proof of Concept

Imagine a situation where the token has a balance of 100, deposits of 1000, and a reserve percentage of 10%. In this situation, the manager should not be able to make any withdrawal.

But, with the following series of events, they can:

*   Manager calls `deposit()` with 100 additional tokens
*   Manager calls `managerWithdraw()` to pull 100 tokens from the contract
*   Manager calls `withdraw()` to remove the 100 tokens they added

The result is that they are able to drain the balance of the contract all the way to zero, avoiding the intended restrictions.

### Recommended Mitigation Steps

Include a check on the reserves in the `withdraw()` function as well as `managerWithdraw()`.

**[Picodes (judge) commented](https://github.com/code-423n4/2022-12-prepo-findings/issues/254#issuecomment-1356147341):**
 > From what I understand, although it's not clear from the documentation or the code, this `minReserve` requirement is here to keep some funds in the contract to allow for withdrawals but does not provide any additional safety, and it should be clear for users that a compromised manager would immediately lead to a loss of all funds.

**[Picodes (judge) commented](https://github.com/code-423n4/2022-12-prepo-findings/issues/254#issuecomment-1356147976):**
 > I'll merge all issues regarding the manager being able to withdraw all funds, regardless of the method, the core issue being that the managerWithdrawHook check is easily bypassable.

**[ramenforbreakfast (prePO) confirmed](https://github.com/code-423n4/2022-12-prepo-findings/issues/254#issuecomment-1358535548)**

**[Picodes (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-12-prepo-findings/issues/254#issuecomment-1368495032):**
 > Flagging as best for this centralization issue, combined with the other finding by the same warden [#255](https://github.com/code-423n4/2022-12-prepo-findings/issues/255)



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | prePO |
| Report Date | N/A |
| Finders | csanuragjain, 8olidity, Trust, hihen, cccz, joestakey, wait, HE1M, Madalad, hansfriese, deliriusz, rvierdiiev, obront, zaskoh |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-prepo
- **GitHub**: https://github.com/code-423n4/2022-12-prepo-findings/issues/254
- **Contest**: https://code4rena.com/contests/2022-12-prepo-contest

### Keywords for Search

`Bypass limit`

