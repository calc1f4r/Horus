---
# Core Classification
protocol: The Standard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41604
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clql6lvyu0001mnje1xpqcuvl
source_link: none
github_link: https://github.com/Cyfrin/2023-12-the-standard

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
finders_count: 3
finders:
  - rvierdiiev
  - pontifex
  - 0xCiphky
---

## Vulnerability Title

swap fees going to the liquidation pool manager contract will be accounted for as part of the liquidation amount

### Overview


This bug report discusses an issue where swap fees, meant for the protocol, are mistakenly included in liquidation amounts. This occurs when users swap collateral types, incurring a fee that is transferred to the LiquidationPoolManager contract. These fees are then considered as part of the liquidated assets and are distributed during the liquidation process, leading to incorrect allocation of funds and potential losses for the protocol. The report recommends transferring these fees to a different address to avoid this issue.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-the-standard/blob/91132936cb09ef9bf82f38ab1106346e2ad60f91/contracts/SmartVaultV3.sol#L214">https://github.com/Cyfrin/2023-12-the-standard/blob/91132936cb09ef9bf82f38ab1106346e2ad60f91/contracts/SmartVaultV3.sol#L214</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-the-standard/blob/91132936cb09ef9bf82f38ab1106346e2ad60f91/contracts/SmartVaultV3.sol#L196">https://github.com/Cyfrin/2023-12-the-standard/blob/91132936cb09ef9bf82f38ab1106346e2ad60f91/contracts/SmartVaultV3.sol#L196</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-the-standard/blob/91132936cb09ef9bf82f38ab1106346e2ad60f91/contracts/SmartVaultV3.sol#L190">https://github.com/Cyfrin/2023-12-the-standard/blob/91132936cb09ef9bf82f38ab1106346e2ad60f91/contracts/SmartVaultV3.sol#L190</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-the-standard/blob/91132936cb09ef9bf82f38ab1106346e2ad60f91/contracts/LiquidationPoolManager.sol#L59">https://github.com/Cyfrin/2023-12-the-standard/blob/91132936cb09ef9bf82f38ab1106346e2ad60f91/contracts/LiquidationPoolManager.sol#L59</a>


## **Summary:**

In the protocol, users can create Smart Vaults to deposit collateral and borrow EURO stablecoins. They also have the option to swap collateral types, incurring a swap fee that is transferred to the LiquidationPoolManager contract. A issue arises because these swap fees, meant for the protocol, are incorrectly included in the liquidation amounts.

## **Vulnerability Details:**

The SmartVaultV3 contract's swap function charges a fee for each collateral swap. This fee is forwarded to the LiquidationPoolManager contract via either the **executeNativeSwapAndFee** or **executeERC20SwapAndFee** function.

```solidity
function swap(bytes32 _inToken, bytes32 _outToken, uint256 _amount) external onlyOwner {
        uint256 swapFee =
            _amount * ISmartVaultManagerV3(manager).swapFeeRate() / ISmartVaultManagerV3(manager).HUNDRED_PC();
        ...
        inToken == ISmartVaultManagerV3(manager).weth()
            ? executeNativeSwapAndFee(params, swapFee)
            : executeERC20SwapAndFee(params, swapFee);
    }
```

These functions transfer the collected swap fee to the LiquidationPoolManager:

```solidity
function executeNativeSwapAndFee(ISwapRouter.ExactInputSingleParams memory _params, uint256 _swapFee) private {
        (bool sent,) = payable(ISmartVaultManagerV3(manager).protocol()).call{value: _swapFee}("");
        require(sent, "err-swap-fee-native");
        ...
    }

function executeERC20SwapAndFee(ISwapRouter.ExactInputSingleParams memory _params, uint256 _swapFee) private {
        IERC20(_params.tokenIn).safeTransfer(ISmartVaultManagerV3(manager).protocol(), _swapFee);
        ...
    }
```

The issue emerges as swap fees accumulate in the LiquidationPoolManager contract and are erroneously considered as part of the liquidation assets. 

Specifically, the **runLiquidation** function within the LiquidationPoolManager contract, triggered during a liquidation event, assesses the liquidated assets' value using the **balanceOf** function. This will include the swap fees in its calculation, thus conflating them with the liquidation assets.

```solidity
function runLiquidation(uint256 _tokenId) external {
        ...
        ITokenManager.Token[] memory tokens = ITokenManager(manager.tokenManager()).getAcceptedTokens();
        ILiquidationPoolManager.Asset[] memory assets = new ILiquidationPoolManager.Asset[](tokens.length);
        uint256 ethBalance;
        for (uint256 i = 0; i < tokens.length; i++) {
            ITokenManager.Token memory token = tokens[i];
            if (token.addr == address(0)) {
                ethBalance = address(this).balance;
                if (ethBalance > 0) assets[i] = ILiquidationPoolManager.Asset(token, ethBalance);
            } else {
                IERC20 ierc20 = IERC20(token.addr);
                uint256 erc20balance = ierc20.balanceOf(address(this));
                if (erc20balance > 0) {
                    assets[i] = ILiquidationPoolManager.Asset(token, erc20balance);
                    ierc20.approve(pool, erc20balance);
                }
            }
        }
        LiquidationPool(pool).distributeAssets{value: ethBalance}(assets, manager.collateralRate(), manager.HUNDRED_PC());
        ...
    }
```

As a result, swap fees are inadvertently treated as part of the liquidated assets and are distributed during the liquidation process, leading to an incorrect allocation of funds.

## Impact:

This miscalculation leads to the unintended distribution of swap fees as part of liquidated assets causing losses to the protocol. Furthermore, an incorrectly inflated liquidation amount can disrupt the protocol's accounting balance and potentially give rise to further complications.

## **Tools Used:**

Manual analysis

## **Recommendation:**

One solution is to transfer these fees to a different address, ensuring they are not mistakenly included in liquidation distributions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | The Standard |
| Report Date | N/A |
| Finders | rvierdiiev, pontifex, 0xCiphky |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-12-the-standard
- **Contest**: https://codehawks.cyfrin.io/c/clql6lvyu0001mnje1xpqcuvl

### Keywords for Search

`vulnerability`

