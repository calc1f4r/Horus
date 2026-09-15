---
# Core Classification
protocol: MetaStreet Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54750
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/d89f3fe2-d0ba-42fd-9625-02ca6cbca5e4
source_link: https://cdn.cantina.xyz/reports/cantina_metastreet_sep2023.pdf
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
  - HickupHH3
  - Anurag Jain
---

## Vulnerability Title

Zero duration will fail all repayment attempt 

### Overview


This bug report is about a problem with loan repayments in a smart contract called `Pool.sol`. If a user sets the duration of their loan to 0, the repayment will fail because of a "divide by zero" error. This means that the user's loan will enter liquidation even if they intended to repay it in the same block. The code causing this issue has been identified and a recommendation has been made to fix it. The bug has been resolved in a recent update to the code. 

### Original Finding Content

## Issue Report: Zero Duration Loan Repayment Failure

## Context
**File Location:** `Pool.sol#L583-L587`

## Description
If a user sets a duration of **0** while borrowing a loan, repaying the loan will fail due to a "divide by zero" error, as `loanReceipt.duration` becomes **0**. This situation causes the user's loan to enter liquidation even if the user intended to repay it in the same block.

### Relevant Code
```solidity
Math.mulDiv(
    block.timestamp - (loanReceipt.maturity - loanReceipt.duration),
    LiquidityManager.FIXED_POINT_SCALE,
    loanReceipt.duration
);
```

## Proof of Concept (POC)
```javascript
it("Zero duration issue", async function () {
    const depositTx = await pool.connect(accountDepositors[0]).deposit(Tick.encode("5"), FixedPoint.from("5"));
    const borrowTx = await pool
        .connect(accountBorrower)
        .borrow(
            FixedPoint.from("5"),
            0,
            nft1.address,
            124,
            FixedPoint.from("6"),
            await sourceLiquidity(FixedPoint.from("5")),
            ethers.utils.solidityPack(["uint16", "uint16", "bytes20"], [3, 20, accountBorrower.address])
        );
    const loanReceipt = (await extractEvent(borrowTx, pool, "LoanOriginated")).args.loanReceipt;
    const repayTx = await pool.connect(accountBorrower).repay(loanReceipt);
});
```

## Recommendation
Add the following check in the borrow function:
```solidity
require(duration > 0, "Invalid duration");
```

## Status
- **MetaStreet:** Resolved in commit `5331f99`.
- **Cantina:** Fixed. It is now checked that the duration is not zero in the `_borrow` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MetaStreet Labs |
| Report Date | N/A |
| Finders | HickupHH3, Anurag Jain |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_metastreet_sep2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/d89f3fe2-d0ba-42fd-9625-02ca6cbca5e4

### Keywords for Search

`vulnerability`

