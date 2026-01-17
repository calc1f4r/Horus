---
# Core Classification
protocol: Tapioca DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27508
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-tapioca
source_link: https://code4rena.com/reports/2023-07-tapioca
github_link: https://github.com/code-423n4/2023-07-tapioca-findings/issues/1202

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - peakbolt
---

## Vulnerability Title

[H-18] `multiHopSellCollateral()` will fail due to call on an invalid market address causing bridged collateral to be locked up

### Overview


This bug report is about the `multiHopSellCollateral()` function which allows users to leverage down by selling the `TOFT` collateral on another chain and then send it to host chain (Arbitrum) for repayment of USDO loan. The issue is that it will fail as it tries to obtain the `repayableAmount` on the destination chain by calling `IMagnetar.getBorrowPartForAmount()` on a non-existing market. This is because Singularity/BigBang markets are only deployed on the host chain.

This bug will prevent users from using `multiHopSellCollateral()` to leverage down. Furthermore, the failure of the cross-chain transaction will cause the bridged collateral to be locked in the TOFT contract on a non-host chain as the refund mechanism will also revert and `retryMessage()` will continue to fail as this is a permanent error.

The recommended mitigation steps to solve this issue are to obtain the repayable amount on the Arbitrum (host chain) where the BigBang/Singularity markets are deployed. 0xRektora (Tapioca) has confirmed this bug.

### Original Finding Content


<https://github.com/Tapioca-DAO/tapioca-bar-audit/blob/master/contracts/markets/singularity/Singularity.sol#L409-L427> 

<https://github.com/Tapioca-DAO/tapioca-bar-audit/blob/master/contracts/markets/singularity/SGLLeverage.sol#L81> 

<https://github.com/Tapioca-DAO/tapiocaz-audit/blob/master/contracts/tOFT/modules/BaseTOFTLeverageModule.sol#L79-L108> 

<https://github.com/Tapioca-DAO/tapiocaz-audit/blob/master/contracts/tOFT/modules/BaseTOFTLeverageModule.sol#L227>

`multiHopSellCollateral()` allows users to leverage down by selling the `TOFT` collateral on another chain and then send it to host chain (Arbitrum) for repayment of USDO loan.

However, it will fail as it tries to obtain the `repayableAmount` on the destination chain by calling `IMagnetar.getBorrowPartForAmount()` on a non-existing market. That is because Singularity/BigBang markets are only deployed on the host chain.

<https://github.com/Tapioca-DAO/tapiocaz-audit/blob/master/contracts/tOFT/modules/BaseTOFTLeverageModule.sol#L205-L227>

```Solidity
    function leverageDownInternal(
        uint256 amount,
        IUSDOBase.ILeverageSwapData memory swapData,
        IUSDOBase.ILeverageExternalContractsData memory externalData,
        IUSDOBase.ILeverageLZData memory lzData,
        address leverageFor
    ) public payable {
        _unwrap(address(this), amount);

        //swap to USDO
        IERC20(erc20).approve(externalData.swapper, amount);
        ISwapper.SwapData memory _swapperData = ISwapper(externalData.swapper)
            .buildSwapData(erc20, swapData.tokenOut, amount, 0, false, false);
        (uint256 amountOut, ) = ISwapper(externalData.swapper).swap(
            _swapperData,
            swapData.amountOutMin,
            address(this),
            swapData.data
        );

        //@audit this call will fail as there is no market in destination chain
        //repay
        uint256 repayableAmount = IMagnetar(externalData.magnetar)
            .getBorrowPartForAmount(externalData.srcMarket, amountOut);
```

### Impact

The issue will prevent users from using `multiHopSellCollateral()` to leverage down.

Furthermore the failure of the cross-chain transaction will cause the bridged collateral to be locked in the TOFT contract on a non-host chain as the refund mechanism will also revert and `retryMessage()` will continue to fail as this is a permanent error.

### Proof of Concept

Consider the following scenario where a user leverage down by selling the collateral on Ethereum (a non-host chain).

1.  User first triggers `Singularity.multiHopSellCollateral()` on host chain Arbitrum.
2.  That will call `SGLLeverage.multiHopSellCollateral()`, which will conduct a cross chain message via `ITapiocaOFT(address(collateral)).sendForLeverage()` to bridge over and sell the collateral on Ethereum mainnet.
3.  The collateral TOFT contract on Ethereum mainnet will receive the bridged collateral and cross-chain message via `_nonBlockingLzReceive()` and then `BaseTOFTLeverageModule.leverageDown()`.
4.  The execution continues with `BaseTOFTLeverageModule.leverageDownInternal()`, but it will revert as it attempt to call `getBorrowPartForAmount()` for a non-existing market in Ethereum.
5.  The bridgex collateral will be locked in the TOFT contract on Ethereum mainnet as the refund mechanism will also revert and `retryMessage()` will continue to fail as this is a permanent error.

### Recommended Mitigation Steps

Obtain the repayable amount on the Arbitrum (host chain) where the BigBang/Singularity markets are deployed.

**[0xRektora (Tapioca) confirmed](https://github.com/code-423n4/2023-07-tapioca-findings/issues/1202#issuecomment-1702967048)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tapioca DAO |
| Report Date | N/A |
| Finders | peakbolt |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-tapioca
- **GitHub**: https://github.com/code-423n4/2023-07-tapioca-findings/issues/1202
- **Contest**: https://code4rena.com/reports/2023-07-tapioca

### Keywords for Search

`vulnerability`

