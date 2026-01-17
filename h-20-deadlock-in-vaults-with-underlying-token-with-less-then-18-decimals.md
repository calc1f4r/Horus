---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25815
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/72

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

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - Jeiwan
  - joestakey
  - gz627
  - Tointer
  - chaduke
---

## Vulnerability Title

[H-20] Deadlock in vaults with underlying token with less then 18 decimals

### Overview


A bug has been identified in the Astaria protocol that could cause a deadlock if the underlying token for the vault has less then 18 decimals. This is a high risk bug, because there is a high demand for stablecoin denominated vaults, and this bug is sneaky, as there could be many epochs before the first liquidation that would trigger the deadlock. This would result in all funds being lost, which is catastrophic.

The issue is that the `claim` function in `WithdrawProxy.sol` would revert if the underlying token for the vault has less then 18 decimals. This is because the `PublicVault.sol` needs `claim` to process epoch, and `WithdrawProxy.sol` unlocks funds only after `claim`. Alternatively, if there is more then 18 decimals, `claim` would leave much less funds than needed for withdraw, resulting in withdrawers losing funds.

To replicate the issue, a token with 8 decimals was created, and the `_bid` function was modified to take a token address as a last parameter. A modified "testLiquidation5050Split" test was then run, and the `withdrawProxy.claim();` at the last line reverted.

The recommended mitigation steps for this issue is to change the line in `WithdrawProxy.sol` to `10**18`. SantiagoGregory (Astaria) confirmed via duplicate issue `#482`.

### Original Finding Content


If underlying token for the vault would have less then 18 decimals, then after liquidation there would be no way to process epoch, because `claim` function in `WithdrawProxy.sol` would revert, this would lock all user out of their funds both in vault and in withdraw proxy. Alternatively, if there is more then 18 decimals, claim would leave much less funds than needed for withdraw, resulting in withdrawers losing funds.

To make report more concise, I would focus on tokens with less then 18 decimals, because they are much more frequent. For example, WBTC have 8 decimals and most stablecoins have 6.

### Why is this happening

<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/PublicVault.sol#L314-L316><br>
this part making sure that withdraw ratio are always stored in 1e18 scale.

<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/WithdrawProxy.sol#L271-L274><br>
but here, we are not transforming it into token decimals scale. `transferAmount` would be orders of magnitudes larger than balance 

<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/WithdrawProxy.sol#L277><br>
then, here we would have underflow of `balance` value

<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/WithdrawProxy.sol#L281><br>
and finally, here function would revert.

<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/WithdrawProxy.sol#L156><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/PublicVault.sol#L299><br>
because `PublicVault.sol` need `claim` to proccess epoch, and `WithdrawProxy.sol` unlocks funds only after `claim`, it will result in deadlock of the whole system.

### Proof of Concept

First, creating token with 8 decimals:

    contract Token8Decimals is ERC20{
    constructor() ERC20("TEST", "TEST", 8) {}

    function mint(address to, uint amount) public{
        _mint(to, amount);
    }
    }

Second, I changed `_bid` function in `TestHelpers.t.sol` contract, so it could take token address as a last parameter, and use it instead of WETH.

Then, here is modified "testLiquidation5050Split" test:

    function testLiquidation5050Split() public {
    TestNFT nft = new TestNFT(2);
    _mintNoDepositApproveRouter(address(nft), 5);
    address tokenContract = address(nft);
    uint256 tokenId = uint256(1);

    Token8Decimals token = new Token8Decimals();

    // create a PublicVault with a 14-day epoch
    vm.startPrank(strategistOne);
    //bps
    address publicVault = (ASTARIA_ROUTER.newPublicVault(
      14 days,
      strategistTwo,
      address(token),
      uint256(0),
      false,
      new address[](0),
      uint256(0)
    ));
    vm.stopPrank();

    uint amountToLend = 10**8 * 1000;
    token.mint(address(1), amountToLend);
    vm.startPrank(address(1));
    token.approve(address(TRANSFER_PROXY), amountToLend);

    ASTARIA_ROUTER.depositToVault(
      IERC4626(publicVault),
      address(1),
      amountToLend,
      uint256(0)
    );
    vm.stopPrank();

    ILienToken.Details memory lien = standardLienDetails;
    lien.liquidationInitialAsk = amountToLend*2;

    (, ILienToken.Stack[] memory stack1) = _commitToLien({
      vault: publicVault,
      strategist: strategistOne,
      strategistPK: strategistOnePK,
      tokenContract: tokenContract,
      tokenId: tokenId,
      lienDetails: lien,
      amount: amountToLend/4,
      isFirstLien: true
    });

    uint256 collateralId = tokenContract.computeId(tokenId);

    _signalWithdraw(address(1), publicVault);

    WithdrawProxy withdrawProxy = PublicVault(publicVault).getWithdrawProxy(
      PublicVault(publicVault).getCurrentEpoch()
    );

    skip(14 days);

    OrderParameters memory listedOrder1 = ASTARIA_ROUTER.liquidate(
      stack1,
      uint8(0)
    );

    token.mint(bidder, amountToLend);
    _bid(Bidder(bidder, bidderPK), listedOrder1, amountToLend/2, address(token));
    vm.warp(withdrawProxy.getFinalAuctionEnd());
    emit log_named_uint("finalAuctionEnd", block.timestamp);
    PublicVault(publicVault).processEpoch();

    skip(13 days);

    withdrawProxy.claim();
    }

`withdrawProxy.claim();` at the last line would revert

### Recommended Mitigation Steps

<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/WithdrawProxy.sol#L273><br>
Change this line to `10**18`

### Severity

I think this is high risk, because

1.  There are high demand for stablecoin denominated vaults, and Astaria are designed to support that.
2.  This bug is sneaky, there could be many epochs before first liquidation that would trigger the deadlock.
3.  ALL funds would be lost, which is catastrophic.

**[SantiagoGregory (Astaria) confirmed via duplicate issue `#482`](https://github.com/code-423n4/2023-01-astaria-findings/issues/482#event-8369726739)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Jeiwan, joestakey, gz627, Tointer, chaduke, unforgiven, rvierdiiev, obront |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/72
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

