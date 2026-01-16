---
# Core Classification
protocol: GMI and Lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51837
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/gloop-finance/gmi-and-lending
source_link: https://www.halborn.com/audits/gloop-finance/gmi-and-lending
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

LendingPool::repay is missing the updatePoints modifier

### Overview


This bug report highlights an issue with the `repay` function in the `LendingPool` contract of the Gloop Finance lending protocol. The function is missing the `updatePoints` modifier, which means that calls to this function do not account for accrued points. This can result in a loss of funds for users who were expecting to earn points and cash them out later. The missing modifier is also the reason why the `testBorrowingAndRepayingUSDCEarnsGMPoints` test fails. The proof of concept shows that the `repay` function does not have the modifier, while its counterparts `deposit`, `withdraw`, and `borrow` do. The BVSS score for this issue is 9.4 out of 10. The recommendation is to add the modifier to the `repay` function definition. The Gloop Finance team has already solved this issue by adding the modifier in a recent commit. 

### Original Finding Content

##### Description

The function `repay` in `LendingPool` does not have the `updatePoints` modifier in its function definition like the others. That makes calls to this function to not account for the accrued points, meaning a loss of funds for users who used their assets with the expectation to, among other things, earn points to be cashed out later on. This behavior is the reason the test `testBorrowingAndRepayingUSDCEarnsGMPoints` reverts, as the expected functionality is missing.

##### Proof of Concept

It can be seen in the `repay` function definition that `updatePoints` is missing:

<https://github.com/GloopFinance/gm-lending-protocol/blob/37c4ebbf16e997a5aefad9c8c6715af8454ed14d/src/LendingPool.sol#L488>

```
    function repay(ERC20 asset, uint256 amount) external {
        ...
    }
```

which is not the same in its counterparts `deposit`, `withdraw` and `borrow`:

<https://github.com/GloopFinance/gm-lending-protocol/blob/37c4ebbf16e997a5aefad9c8c6715af8454ed14d/src/LendingPool.sol#L318C1-L321C76>

```
    function deposit(
        ERC20 asset,
        uint256 amount
    ) external updatePoints(asset, GMPoints.PoolActivity.Deposit, amount) {
        ...
    }
```

<https://github.com/GloopFinance/gm-lending-protocol/blob/37c4ebbf16e997a5aefad9c8c6715af8454ed14d/src/LendingPool.sol#L362C1-L365C77>

```
    function withdraw(
        ERC20 asset,
        uint256 amount
    ) external updatePoints(asset, GMPoints.PoolActivity.Withdraw, amount) {
        ...
    }
```

<https://github.com/GloopFinance/gm-lending-protocol/blob/>[37c4ebbf16e997a5aefad9c8c6715af8454ed14d/src/LendingPool.sol#L433C1-L436C75](https://github.com/GloopFinance/gm-lending-protocol/blob/37c4ebbf16e997a5aefad9c8c6715af8454ed14d/src/LendingPool.sol#L433C1-L436C75)

```
    function borrow(
        ERC20 asset,
        uint256 amount
    ) external updatePoints(asset, GMPoints.PoolActivity.Borrow, amount) {
        ...
    }
```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:H/Y:H/R:N/S:U (9.4)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:H/Y:H/R:N/S:U)

##### Recommendation

Add the modifier to the `repay` function definition.

### Remediation Plan

**SOLVED:** The **Gloop Finance team** solved this issue as recommended above.

##### Remediation Hash

<https://github.com/GloopFinance/gm-lending-protocol/commit/4a94248ce53f1a3d374809e5bc25e42c9d4340d0>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | GMI and Lending |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/gloop-finance/gmi-and-lending
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/gloop-finance/gmi-and-lending

### Keywords for Search

`vulnerability`

