---
# Core Classification
protocol: Term Structure
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54905
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6f373ea8-adf6-45d2-8d72-a76fe5b7f21e
source_link: https://cdn.cantina.xyz/reports/cantina_competition_term_structure_february2025.pdf
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
finders_count: 3
finders:
  - BengalCatBalu
  - korok
  - 0xNull
---

## Vulnerability Title

Missing Market Whitelist Modiﬁer in borrowTokenFromGt 

### Overview


This bug report discusses an issue with the `borrowTokenFromGt` function in the TermMaxRouter contract. This function allows users to borrow tokens from a specific market, but it does not check whether the market is on the whitelist. This means that users can exploit this vulnerability and use the function on unauthorized markets, potentially leading to the transfer or loss of tokens. The likelihood of this issue occurring is high, especially if the system is used by a large number of users interacting with various markets. The report includes a proof of concept and recommends adding a modifier to prevent this vulnerability. The issue has been fixed in the code. 

### Original Finding Content

## Context
TermMaxRouter.sol#L340

## Summary
The `borrowTokenFromGt` function in the TermMaxRouter contract allows the use of unauthorized markets by not utilizing a modifier to check whether the specified market is whitelisted.

## Finding Description
The `borrowTokenFromGt` function, which is used for borrowing tokens from a specific market, does not use the `ensureMarketWhitelist` modifier, which should be applied in every function interacting with the market. This allows users to invoke this function on markets that are not part of the whitelist. This issue allows individuals to use this function and its logic in unauthorized markets.

## Impact Explanation
The impact is high because this issue could lead to the following:
- Transfer of unauthorized tokens.
- Lending or loss of tokens.

## Likelihood Explanation
The likelihood of this issue occurring is relatively high, especially if the system is used by a large number of users interacting with various markets. Since the `borrowTokenFromGt` function does not check whether the market is on the whitelist, any user can exploit this vulnerability and use the function on unauthorized markets.

## Proof of Concept
The market whitelist status has been set to false, and the execution completes successfully:

```solidity
function testBorrowTokenFromGt() public {
    vm.startPrank(deployer);
    res.router.setMarketWhitelist(address(res.market), false);
    vm.stopPrank();
    vm.startPrank(sender);
    uint256 collInAmt = 1e18;
    (uint256 gtId,) = LoanUtils.fastMintGt(res, sender, 100e8, collInAmt);
    uint128 borrowAmt = 80e8;
    res.debt.mint(sender, borrowAmt);
    res.debt.approve(address(res.market), borrowAmt);
    res.market.mint(sender, borrowAmt);
    res.xt.approve(address(res.router), borrowAmt);
    res.gt.approve(address(res.router), gtId);
    uint256 issueFtFeeRatio = res.market.issueFtFeeRatio();
    uint128 previewDebtAmt = ((borrowAmt * Constants.DECIMAL_BASE) / (Constants.DECIMAL_BASE - issueFtFeeRatio)).toUint128();
    vm.expectEmit();
    emit RouterEvents.Borrow(res.market, 1, sender, sender, 0, previewDebtAmt, borrowAmt);
    res.router.borrowTokenFromGt(sender, res.market, gtId, borrowAmt);
    (, uint128 debtAmt,,) = res.gt.loanInfo(gtId);
    assert(debtAmt == 100e8 + previewDebtAmt);
    assertEq(res.debt.balanceOf(sender), borrowAmt);
    vm.stopPrank();
}
```

## Recommendation
Consider adding the `ensureMarketWhitelist` modifier to prevent this vulnerability.

## Term Structure
Router is just a function aggregation. Whitelist restriction is only used as an additional security precaution and will not actively cause user funds to be lost. Addressed in PR 4 and PR 5.

## Cantina Managed
Fixes verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Term Structure |
| Report Date | N/A |
| Finders | BengalCatBalu, korok, 0xNull |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_term_structure_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6f373ea8-adf6-45d2-8d72-a76fe5b7f21e

### Keywords for Search

`vulnerability`

