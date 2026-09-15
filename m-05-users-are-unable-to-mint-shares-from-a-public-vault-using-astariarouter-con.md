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
solodit_id: 25821
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/488

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - rbserver
  - cccz
  - Jeiwan
  - chaduke
  - adriro
---

## Vulnerability Title

[M-05] Users are unable to mint shares from a public vault using `AstariaRouter` contract when share price is bigger than one

### Overview


This bug report describes an issue with the `AstariaRouter.mint` function when the public vault's share price is bigger than 1. When this occurs, users are unable to mint shares from the public vault using the `AstariaRouter` contract and cannot utilize the slippage control associated with the `maxAmountIn` input. The issue is caused by the `ERC4626Cloned.mint` function trying to transfer an `assets` amount from `msg.sender` to the public vault, which is the `AstariaRouter` contract in this case. However, the `AstariaRouter.mint` function only approves the public vault for transferring `shares` of the asset token on behalf of the router, causing the transfer of `assets` to fail due to the insufficient asset token allowance. 

The recommended mitigation step is to update the `ERC4626RouterBase.mint` function to use the public vault's `previewMint` function to get an `assetAmount` for the `shares` input. This can be done by changing <https://github.com/AstariaXYZ/astaria-gpl/blob/main/src/ERC4626RouterBase.sol#L21> to the following code.

```solidity
    ERC20(vault.asset()).safeApprove(address(vault), assetAmount);
```

In addition, to demonstrate the described scenario, a test can be added to `src\test\AstariaTest.t.sol`. The code for the test is provided in the bug report.

### Original Finding Content


For a public vault, calling the `AstariaRouter.mint` function calls the following `ERC4626RouterBase.mint` function and then the `ERC4626Cloned.mint` function below. After user actions like borrowing and repaying after some time, the public vault's share price can become bigger than 1 so `ERC4626Cloned.previewMint` function's execution of `shares.mulDivUp(totalAssets(), supply)` would return `assets` that is bigger than `shares`; then, calling the `ERC4626Cloned.mint` function would try to transfer this `assets` from `msg.sender` to the public vault. When the `AstariaRouter.mint` function is called, this `msg.sender` is the `AstariaRouter` contract. However, because the `AstariaRouter.mint` function only approves the public vault for transferring `shares` of the asset token on behalf of the router, the `ERC4626Cloned.mint` function's transfer of `assets` of the asset token would fail due to the insufficient asset token allowance. Hence, when the public vault's share price is bigger than 1, users are unable to mint shares from the public vault using the `AstariaRouter` contract and cannot utilize the slippage control associated with the `maxAmountIn` input.

<https://github.com/AstariaXYZ/astaria-gpl/blob/main/src/ERC4626RouterBase.sol#L15-L25>

```solidity
  function mint(
    IERC4626 vault,
    address to,
    uint256 shares,
    uint256 maxAmountIn
  ) public payable virtual override returns (uint256 amountIn) {
    ERC20(vault.asset()).safeApprove(address(vault), shares);
    if ((amountIn = vault.mint(shares, to)) > maxAmountIn) {
      revert MaxAmountError();
    }
  }
```

<https://github.com/AstariaXYZ/astaria-gpl/blob/main/src/ERC4626-Cloned.sol#L38-L52>

```solidity
  function mint(
    uint256 shares,
    address receiver
  ) public virtual returns (uint256 assets) {
    assets = previewMint(shares); // No need to check for rounding error, previewMint rounds up.
    require(assets > minDepositAmount(), "VALUE_TOO_SMALL");
    // Need to transfer before minting or ERC777s could reenter.
    ERC20(asset()).safeTransferFrom(msg.sender, address(this), assets);

    _mint(receiver, shares);

    emit Deposit(msg.sender, receiver, assets, shares);

    afterDeposit(assets, shares);
  }
```

<https://github.com/AstariaXYZ/astaria-gpl/blob/main/src/ERC4626-Cloned.sol#L129-L133>

```solidity
  function previewMint(uint256 shares) public view virtual returns (uint256) {
    uint256 supply = totalSupply(); // Saves an extra SLOAD if totalSupply is non-zero.

    return supply == 0 ? 10e18 : shares.mulDivUp(totalAssets(), supply);
  }
```

### Proof of Concept

Please add the following test in `src\test\AstariaTest.t.sol`. This test will pass to demonstrate the described scenario.

```solidity
  function testUserFailsToMintSharesFromPublicVaultUsingRouterWhenSharePriceIsBiggerThanOne() public {
    uint256 amountIn = 50 ether;
    address alice = address(1);
    address bob = address(2);
    vm.deal(bob, amountIn);

    TestNFT nft = new TestNFT(2);
    _mintNoDepositApproveRouter(address(nft), 5);
    address tokenContract = address(nft);
    uint256 tokenId = uint256(0);

    address publicVault = _createPublicVault({
      strategist: strategistOne,
      delegate: strategistTwo,
      epochLength: 14 days
    });

    // after alice deposits 50 ether WETH in publicVault, publicVault's share price becomes 1
    _lendToVault(Lender({addr: alice, amountToLend: amountIn}), publicVault);

    // the borrower borrows 10 ether WETH from publicVault
    (, ILienToken.Stack[] memory stack1) = _commitToLien({
      vault: publicVault,
      strategist: strategistOne,
      strategistPK: strategistOnePK,
      tokenContract: tokenContract,
      tokenId: tokenId,
      lienDetails: standardLienDetails,
      amount: 10 ether,
      isFirstLien: true
    });
    uint256 collateralId = tokenContract.computeId(tokenId);

    // the borrower repays for the lien after 9 days, and publicVault's share price becomes bigger than 1
    vm.warp(block.timestamp + 9 days);
    _repay(stack1, 0, 100 ether, address(this));

    vm.startPrank(bob);

    // bob owns 50 ether WETH
    WETH9.deposit{value: amountIn}();
    WETH9.transfer(address(ASTARIA_ROUTER), amountIn);

    // bob wants to mint 1 ether shares from publicVault using the router but fails
    vm.expectRevert(bytes("TRANSFER_FROM_FAILED"));
    ASTARIA_ROUTER.mint(
      IERC4626(publicVault),
      bob,
      1 ether,
      type(uint256).max
    );

    vm.stopPrank();
  }
```

### Tools Used

VSCode

### Recommended Mitigation Steps

In the `ERC4626RouterBase.mint` function, the public vault's `previewMint` function can be used to get an `assetAmount` for the `shares` input.<br>
<https://github.com/AstariaXYZ/astaria-gpl/blob/main/src/ERC4626RouterBase.sol#L21> can then be updated to the following code.

```solidity
    ERC20(vault.asset()).safeApprove(address(vault), assetAmount);
```



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | rbserver, cccz, Jeiwan, chaduke, adriro, unforgiven, rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/488
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

