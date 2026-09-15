---
# Core Classification
protocol: Beedle - Oracle free perpetual lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34492
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx
source_link: none
github_link: https://github.com/Cyfrin/2023-07-beedle

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
finders_count: 52
finders:
  - offkey
  - HALITUS
  - dacian
  - lealCodes
  - toshii
---

## Vulnerability Title

During refinance() new Pool balance debt is subtracted twice

### Overview


This report highlights a bug in the code where the debt is subtracted twice during a refinancing process, resulting in a loss of funds to the new pool. This can occur when a borrower moves their loan to another pool with new lending conditions. The vulnerability can be found in the code at lines 636 and 696. The impact of this bug is that pool balances are reduced twice by the transferred debt, resulting in a greater loss for larger loans. A proof of concept has been provided using the Borrow and Refinance functions, and manual review and Foundry were used to identify the bug. The recommended mitigation step is to remove the second debt transfer at line 696.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Marzel7/Beedle/blob/main/test/POC/Refinance.t.sol">https://github.com/Marzel7/Beedle/blob/main/test/POC/Refinance.t.sol</a>




## Summary

A borrower has the opportunity to move their loan to another pool under new lending conditions.

During refinancing interest from the loan is transferred to the old pool.

The debt is then transferred to the new pool however this subraction occurs twice, resulting in loss of funds to the Lenders pool.



## Vulnerability Details

In refinance() the debt to the new pool is transferred at line 636


```solidity

_updatePoolBalance(poolId, pools[poolId].poolBalance - debt);

```

The debt is subtracted again at line 696

```solidity

pools[poolId].poolBalance -= debt;

```

##  Impact


Pool balances are reduced twice by the transferred debt. The larger the loan the greater the loss of funds to the new pool.


## Code Snippet

https://github.com/Cyfrin/2023-07-beedle/blob/main/src/Lender.sol#L636

https://github.com/Cyfrin/2023-07-beedle/blob/main/src/Lender.sol#L698


## Proof of Concept

```solidity

  function test_Refinance() public {
        vm.startPrank(lender1);
        Pool memory p1 = Pool({
            lender: lender1,
            loanToken: address(loanToken),
            collateralToken: address(collateralToken),
            minLoanSize: 100 * 10 ** 18,
            poolBalance: POOL_LOAN_TOKEN_BALANCE,
            maxLoanRatio: 2 * 10 ** 18,
            auctionLength: 1 days,
            interestRate: 1000,
            outstandingLoans: 0
        });

        Pool memory p2 = Pool({
            lender: lender2,
            loanToken: address(loanToken),
            collateralToken: address(collateralToken),
            minLoanSize: 100 * 10 ** 18,
            poolBalance: POOL_B_LOAN_TOKEN_BALANCE,
            maxLoanRatio: 2 * 10 ** 18,
            auctionLength: 1 days,
            interestRate: 1000,
            outstandingLoans: 0
        });

        bytes32 poolIdOne = lender.setPool(p1);

        vm.startPrank(lender2);
        bytes32 poolIdTwo = lender.setPool(p2);

        bytes32[] memory poolIds = new bytes32[](3);
        poolIds[0] = poolIdOne;
        poolIds[1] = poolIdTwo;

        uint256[] memory loansIds = new uint256[](1);
        loansIds[0] = 0;

        vm.startPrank(borrower);
        Borrow memory b = Borrow({poolId: poolIdOne, debt: LOAN_AMOUNT, collateral: 1000 * 10 ** 18});
        Borrow[] memory borrows = new Borrow[](1);
        borrows[0] = b;
        lender.borrow(borrows);

        Refinance memory r =
            Refinance({loanId: 0, poolId: poolIdTwo, debt: 1000 * 10 ** 18, collateral: 1000 * 10 ** 18});
        Refinance[] memory refinances = new Refinance[](1);
        refinances[0] = r;

        vm.warp(10 days);

        // New Pool balance before refinancing
        (,,,, uint256 poolBalance,,,,) = lender.pools(poolIdTwo);
        assertEq(poolBalance, (POOL_B_LOAN_TOKEN_BALANCE));

        lender.refinance(refinances);

        (,,,, poolBalance,,,,) = lender.pools(poolIdTwo);
        // Debt is transferred to new pool twice
        assertEq(poolBalance, (POOL_B_LOAN_TOKEN_BALANCE) - (2 * 1000 * 10 ** 18));

  }

```

## Tools Used

Manual review and Foundry for the POC

## Recommended Mitigation Steps

Remove the second debt transfer at line 696

```solidity

pools[poolId].poolBalance -= debt;

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beedle - Oracle free perpetual lending |
| Report Date | N/A |
| Finders | offkey, HALITUS, dacian, lealCodes, toshii, Mlome, CircleLooper, sobieski, JMTT, akalout, trachev, B353N, Marzel, MahdiKarimi, 0x11singh99, sonny2k, JrNet, Saskloch, Juntao, serialcoder, tiesstevelink, KupiaSec, ohi0b, amar, deadrosesxyz, 0xDanielH, Mukund, Cosine, qckhp, pacelli, Bernd, Aamir, 0xbepresent, Kose, Niki, 0xDetermination, 0xdeth, 0x3b, kutu, GoSoul22, khegeman, 0xlemon, Crunch, StErMi, ABA, trtrth, KrisApostolov, pengun, ubermensch, 0xCiphky, Lalanda, rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-beedle
- **Contest**: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx

### Keywords for Search

`vulnerability`

