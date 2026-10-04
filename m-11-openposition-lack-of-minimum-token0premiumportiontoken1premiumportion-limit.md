---
# Core Classification
protocol: Particle Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29708
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-particle
source_link: https://code4rena.com/reports/2023-12-particle
github_link: https://github.com/code-423n4/2023-12-particle-findings/issues/27

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
  - dexes

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - bin2chen
  - immeas
---

## Vulnerability Title

[M-11] openPosition() Lack of minimum token0PremiumPortion/token1PremiumPortion limit

### Overview


The `openPosition()` function in the code allows for both `token0PremiumPortion` and `token1PremiumPortion` to be set to 0 at the same time. This can lead to a situation where someone can borrow liquidity without paying any fees, essentially getting a no-cost loan. This can cause issues such as malicious occupation of liquidity, liquidators not being able to execute their function, and borrowers still profiting even though they did not pay any fees. A test case was provided to demonstrate this issue and a suggested solution is to add a minimum limit for `token0PremiumPortion` and `token1PremiumPortion` in the code. The developers have acknowledged this issue and plan to implement the suggested solution.

### Original Finding Content


In `openPosition()`, it allows `token0PremiumPortion` and `token1PremiumPortion` to be 0 at the same time.

In this case, if `tokenId` enters `out_of_price`, for example, `UpperOutOfRange`, anyone might be able to input:

    marginFrom = 0
    marginTo = 0
    amountSwap = 0
    zeroForOne = false
    liquidity > 0

Note: `amountFromBorrowed + marginFrom == 0`, so `fees ==0`

To open a new Position, borrow Liquidity, but without paying any fees. It's basically a no-cost loan.

### Impact

`out_of_price` tokenId, due to the no-cost loan, might lead to the following issues:

1.  Malicious occupation of Liquidity
2.  Since both `token0Premium/token1Premium` are 0, the liquidator will not execute `liquidatePosition()`, because there is no profit.
3.  Since both `token0Premium/token1Premium` are 0, `LP` cannot get fees, but the borrower might still be able to profit.

### Proof of Concept

The following test case demonstrates that if it is `out_of_price`, anyone can borrow at no cost.

Add to `OpenPosition.t.sol`:

```solidity
    function testZeroFees() public {
        _setupUpperOutOfRange();
        uint128 borrowerLiquidity = _liquidity / _borrowerLiquidityPorition;
        console.log("borrowerLiquidity:",borrowerLiquidity);
        address anyone = address(0x123999);
        vm.startPrank(anyone);
        particlePositionManager.openPosition(
            DataStruct.OpenPositionParams({
                tokenId: _tokenId,
                marginFrom: 0,
                marginTo: 0,
                amountSwap: 0,
                liquidity: borrowerLiquidity,
                tokenFromPremiumPortionMin: 0,
                tokenToPremiumPortionMin: 0,
                marginPremiumRatio: type(uint8).max,
                zeroForOne: false,
                data: ""
            })
        );
        vm.stopPrank();
        (
            ,
            uint128 liquidity,
            ,
            uint128 token0Premium,
            uint128 token1Premium,
            ,
            ,            
        ) = particleInfoReader.getLien(anyone, 0);
        console.log("liquidity:",liquidity);
        console.log("token0Premium:",token0Premium);
        console.log("token1Premium:",token1Premium);
    }
```

```console
Logs:
  borrowerLiquidity: 1739134199054731
  liquidity: 1739134199054731
  token0Premium: 0
  token1Premium: 0
```

### Recommended Mitigation

It is suggested that `openPosition()` should add a minimum `token0PremiumPortion/token1PremiumPortion` limit.

```diff
    function openPosition(
        DataStruct.OpenPositionParams calldata params
    ) public override nonReentrant returns (uint96 lienId, uint256 collateralTo) {
...

+       require(params.tokenFromPremiumPortionMin>=MIN_FROM_PREMIUM_PORTION,"invalid tokenFromPremiumPortionMin");
+       require(params.tokenToPremiumPortionMin>=MIN_TO_PREMIUM_PORTION,"invalid tokenToPremiumPortionMin");
```

**[wukong-particle (Particle) confirmed and commented](https://github.com/code-423n4/2023-12-particle-findings/issues/27#issuecomment-1868214226):**
 > It's a good suggestion. We will add minimum premium in contract (current frontend enforces a minimum 1-2%).


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Particle Protocol |
| Report Date | N/A |
| Finders | bin2chen, immeas |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-particle
- **GitHub**: https://github.com/code-423n4/2023-12-particle-findings/issues/27
- **Contest**: https://code4rena.com/reports/2023-12-particle

### Keywords for Search

`vulnerability`

