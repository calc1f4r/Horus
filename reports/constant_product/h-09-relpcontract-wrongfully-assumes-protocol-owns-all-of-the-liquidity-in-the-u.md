---
# Core Classification
protocol: Dopex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29462
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-dopex
source_link: https://code4rena.com/reports/2023-08-dopex
github_link: https://github.com/code-423n4/2023-08-dopex-findings/issues/143

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
finders_count: 7
finders:
  - said
  - kutugu
  - pep7siup
  - deadrxsezzz
  - QiuhaoLi
---

## Vulnerability Title

[H-09] `ReLPContract` wrongfully assumes protocol owns all of the liquidity in the UniswapV2 pool

### Overview


A bug report has been filed for a potential full DoS (Denial of Service) for the `ReLPContract` contract. This occurs when taking out a `bond` in `RdpxV2Core` if `isReLPActive == true`, a call to `ReLPContract#reLP` is made which 're-LPs the pool`. The problem is that the protocol wrongfully assumes that it owns all of the liquidity within the pool. This leads to faulty calculations which can cause full DoS, as `lpToRemove` will be calculated to be more than the LP balance of `UniV2LiquidityAmo` and the transaction will revert. A Proof of Concept (PoC) has been provided to demonstrate the issue.

The recommended mitigation steps are to change the logic and base all calculations on the pair balance of `UniV2LiquidityAmo`. This issue has been confirmed and commented on by psytama (Dopex) and Alex the Entreprenerd (Judge). 

### Original Finding Content


Possible full DoS for `ReLPContract`

### Proof of Concept

When taking out a `bond` in `RdpxV2Core` if `isReLPActive == true`, a call to `ReLPContract#reLP` is made which 're-LPs the pool\` (takes out an amount of RDPX, while still perfectly maintaining the token ratio of the pool).

```solidity
    (uint256 reserveA, uint256 reserveB) = UniswapV2Library.getReserves(  // @audit - here it gets the reserves of the pool and assumes them as owned by the protocol
      addresses.ammFactory,
      tokenASorted,
      tokenBSorted
    );

    TokenAInfo memory tokenAInfo = TokenAInfo(0, 0, 0);

    // get tokenA reserves
    tokenAInfo.tokenAReserve = IRdpxReserve(addresses.tokenAReserve)
      .rdpxReserve(); // rdpx reserves

    // get rdpx price
    tokenAInfo.tokenAPrice = IRdpxEthOracle(addresses.rdpxOracle)
      .getRdpxPriceInEth();

    tokenAInfo.tokenALpReserve = addresses.tokenA == tokenASorted
      ? reserveA
      : reserveB;

    uint256 baseReLpRatio = (reLPFactor *
      Math.sqrt(tokenAInfo.tokenAReserve) *
      1e2) / (Math.sqrt(1e18)); // 1e6 precision

    uint256 tokenAToRemove = ((((_amount * 4) * 1e18) /
      tokenAInfo.tokenAReserve) *
      tokenAInfo.tokenALpReserve *   // @audit - here the total RDPX reserve in the pool is assumed to be owned by the protocol
      baseReLpRatio) / (1e18 * DEFAULT_PRECISION * 1e2);

    uint256 totalLpSupply = IUniswapV2Pair(addresses.pair).totalSupply();

    uint256 lpToRemove = (tokenAToRemove * totalLpSupply) /
      tokenAInfo.tokenALpReserve;
```

The problem is that the protocol wrongfully assumes that it owns all of the liquidity within the pool. This leads to faulty calculations. In best case scenario wrong amounts are passed. However, when the protocol doesn't own the majority of the pool LP balance, this could lead to full DoS, as `lpToRemove` will be calculated to be more than the LP balance of `UniV2LiquidityAmo` and the transaction will revert.

This can all be easily proven by a simple PoC (add the test to the given `Periphery.t.sol`)
Note: there's an added `console.log` in `ReLPContract#reLP`, just before the `transferFrom` in order to better showcase the issue

```solidity
    uint256 lpToRemove = (tokenAToRemove * totalLpSupply) /
      tokenAInfo.tokenALpReserve;

    console.log("lpToRemove value:    ", lpToRemove);  // @audit - added console.log to prove the underflow
    // transfer LP tokens from the AMO
    IERC20WithBurn(addresses.pair).transferFrom(
      addresses.amo,
      address(this),
      lpToRemove
    );
```

```solidity
  function testReLpContract() public {
    testV2Amo();

    // set address in reLP contract and grant role
    reLpContract.setAddresses(
      address(rdpx),
      address(weth),
      address(pair),
      address(rdpxV2Core),
      address(rdpxReserveContract),
      address(uniV2LiquidityAMO),
      address(rdpxPriceOracle),
      address(factory),
      address(router)
    );
    reLpContract.grantRole(reLpContract.RDPXV2CORE_ROLE(), address(rdpxV2Core));

    reLpContract.setreLpFactor(9e4);

    // add liquidity
    uniV2LiquidityAMO.addLiquidity(5e18, 1e18, 0, 0);
    uniV2LiquidityAMO.approveContractToSpend(
      address(pair),
      address(reLpContract),
      type(uint256).max
    );

    rdpxV2Core.setIsreLP(true);


    (uint256 reserveA, uint256 reserveB, ) = pair.getReserves();
    weth.mint(address(2), reserveB * 10);
    rdpx.mint(address(2), reserveA * 10);
    vm.startPrank(address(2));
    weth.approve(address(router), reserveB * 10);
    rdpx.approve(address(router), reserveA * 10);
    router.addLiquidity(address(rdpx), address(weth), reserveA * 10, reserveB * 10, 0, 0, address(2), 12731316317831123);
    vm.stopPrank();
    
    console.log("UniV2Amo balance isn't enough and will underflow");
    uint pairBalance = pair.balanceOf(address(uniV2LiquidityAMO));
    console.log("UniV2Amo LP balance: ", pairBalance);

    vm.expectRevert("ds-math-sub-underflow");
    rdpxV2Core.bond(1 * 1e18, 0, address(this));
}
```

And the logs:

    [PASS] testReLpContract() (gas: 3946961)
    Logs:
      UniV2Amo balance isn't enough and will underflow
      UniV2Amo LP balance:  2235173550604750304
      lpToRemove value:     17832559500122488916

### Recommended Mitigation Steps

Change the logic and base all calculations on the pair balance of `UniV2LiquidityAmo`

**[psytama (Dopex) confirmed and commented](https://github.com/code-423n4/2023-08-dopex-findings/issues/143#issuecomment-1733719078):**
 > The re-LP formula used is incorrect.

**[Alex the Entreprenerd (Judge) commented](https://github.com/code-423n4/2023-08-dopex-findings/issues/143#issuecomment-1755815613):**
 > The incorrect assumption does indeed cause reverts.

***


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Dopex |
| Report Date | N/A |
| Finders | said, kutugu, pep7siup, deadrxsezzz, QiuhaoLi, 0xDING99YA, 0xMango |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-dopex
- **GitHub**: https://github.com/code-423n4/2023-08-dopex-findings/issues/143
- **Contest**: https://code4rena.com/reports/2023-08-dopex

### Keywords for Search

`vulnerability`

