---
# Core Classification
protocol: Zaros
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37977
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clyg8slke0001bvhpwszwjr7z
source_link: none
github_link: https://github.com/Cyfrin/2024-07-zaros

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

# Audit Details
report_date: unknown
finders_count: 12
finders:
  - 0xStalin
  - blutorque
  - inh3l
  - inzinko
  - ke1caM
---

## Vulnerability Title

Functions calling `verifyReport` to verify offchain prices from chainlink will fail

### Overview

See description below for full details.

### Original Finding Content

##### Relevant GitHub Links

<https://github.com/Cyfrin/2024-07-zaros/blob/d687fe96bb7ace8652778797052a38763fbcbb1b/src/external/chainlink/ChainlinkUtil.sol#L103>

## Summary

Missing payable and approval functionalities to send verifier fees to chainlink's feemanager contract.

## Vulnerability Details

In ChainlinkUtil.sol, there's the `verifyReport` function which is used to verify chainlink prices using chainlinkVerifier contract. The function is intended to send the fee amount in ETH to VerifierProxy.sol, we can see that the call to chainlink verifier attempts to send the `fee.amount` as ETH.

```solidity
    function verifyReport(
        IVerifierProxy chainlinkVerifier,
        FeeAsset memory fee,
        bytes memory signedReport
    )
        internal
        returns (bytes memory verifiedReportData)
    {
        verifiedReportData = chainlinkVerifier.verify{ value: fee.amount }(signedReport, abi.encode(fee.assetAddress)); //@note
    }
```

And as can be seen from [VerifierProxy.sol](https://github.com/smartcontractkit/chainlink/blob/9e74eee9d415b386db33bdf2dd44facc82cd3551/contracts/src/v0.8/llo-feeds/VerifierProxy.sol#L127), the function expects and uses msg.value as fee amount.

```solidity
  function verify(
    bytes calldata payload,
    bytes calldata parameterPayload
  ) external payable checkAccess returns (bytes memory) {
    IVerifierFeeManager feeManager = s_feeManager;

    // Bill the verifier
    if (address(feeManager) != address(0)) {
      feeManager.processFee{value: msg.value}(payload, parameterPayload, msg.sender);
    }

    return _verify(payload);
  }
```

This is all well and good, however, none the functions calling the `verifyReport` function are payable, nor do they have a receive functionality with which they can receive and later forward the ETH fee to the verifier contract.

To prove this, we'll follow the function logic.
Using the [search functionality](https://github.com/search?q=repo%3ACyfrin%2F2024-07-zaros+verifyReport%28\&type=code), we can see that the `verifyReport` function is called in SettlementConfiguration.sol library in the `verifyDataStreamsReport` function. The function as can be seen is not marked payable, nor does the library hold a source of receiving ETH.

```solidity
    function verifyDataStreamsReport(
        DataStreamsStrategy memory dataStreamsStrategy,
        bytes memory signedReport
    )
        internal
        returns (bytes memory verifiedReportData)
    {
        IVerifierProxy chainlinkVerifier = dataStreamsStrategy.chainlinkVerifier;

        bytes memory reportData = ChainlinkUtil.getReportData(signedReport);
        (FeeAsset memory fee) = ChainlinkUtil.getEthVericationFee(chainlinkVerifier, reportData);
        verifiedReportData = ChainlinkUtil.verifyReport(chainlinkVerifier, fee, signedReport);  //@note
    }
```

And in [searching](https://github.com/search?q=repo%3ACyfrin%2F2024-07-zaros+%22verifyDataStreamsReport%28%22\&type=code) for `verifyDataStreamsReport` function, we discover it's also in use in the `verifyOffchainPrice` function, also in SettlementConfiguration.sol. And as can be observed, the function is not marked payable, nor does the librarys have any way of receiving ETH.

```solidity
    function verifyOffchainPrice(
        Data storage self,
        bytes memory priceData,
        uint256 maxVerificationDelay
    )
        internal
        returns (UD60x18 bidX18, UD60x18 askX18)
    {
        if (self.strategy == Strategy.DATA_STREAMS_DEFAULT) {
            DataStreamsStrategy memory dataStreamsStrategy = abi.decode(self.data, (DataStreamsStrategy));
            bytes memory verifiedPriceData = verifyDataStreamsReport(dataStreamsStrategy, priceData);  //@note 

            requireDataStreamsReportIsValid(dataStreamsStrategy.streamId, verifiedPriceData, maxVerificationDelay);

            PremiumReport memory premiumReport = abi.decode(verifiedPriceData, (PremiumReport));

            (bidX18, askX18) =
                (ud60x18(int256(premiumReport.bid).toUint256()), ud60x18(int256(premiumReport.ask).toUint256()));
        } else {
            revert Errors.InvalidSettlementStrategy();
        }
    }
```

Repeating the [search process](https://github.com/search?q=repo%3ACyfrin%2F2024-07-zaros+%22verifyOffchainPrice%28%22\&type=code), we discover that `verifyOffchainPrice` is used in two major functions in SettlementBranch.sol. The `fillMarketOrder` and the `fillOffchainOrders` which are called by their keeper respective keepers.

```solidity
    function fillMarketOrder(
        uint128 tradingAccountId,
        uint128 marketId,
        bytes calldata priceData
    )
        external
        onlyMarketOrderKeeper(marketId)
    {
//...
        // verifies provided price data following the configured settlement strategy
        // returning the bid and ask prices
        (ctx.bidX18, ctx.askX18) =
            settlementConfiguration.verifyOffchainPrice(priceData, globalConfiguration.maxVerificationDelay);
//...
    }
```

```solidity
function fillOffchainOrders(
        uint128 marketId,
        OffchainOrder.Data[] calldata offchainOrders,
        bytes calldata priceData
    )
        external
        onlyOffchainOrdersKeeper(marketId)
    {
//...
        // verifies provided price data following the configured settlement strategy
        // returning the bid and ask prices
        (ctx.bidX18, ctx.askX18) =
            settlementConfiguration.verifyOffchainPrice(priceData, globalConfiguration.maxVerificationDelay);
//...
```

Notice that these functions are also not marked payable, neither does the contract have a way of receiving ETH due to its lack of the `receive` functionality.
As a result, calls to these functions, will fail if the `fee.amount` is > 0 as ETH is not sent.

Now, Chainlink probabaly expected this and therefore allows the subscribers to pay in WETH instead, as the native token if ETH is not sent. Following the logic chain from the [`verify`](https://github.com/smartcontractkit/chainlink/blob/9e74eee9d415b386db33bdf2dd44facc82cd3551/contracts/src/v0.8/llo-feeds/VerifierProxy.sol#L132) function in VerifierProxy.sol, the function attempts to process fees in the fee manager through the `processFee` function.

```solidity
  function verify(
    bytes calldata payload,
    bytes calldata parameterPayload
  ) external payable checkAccess returns (bytes memory) {
    IVerifierFeeManager feeManager = s_feeManager;

    // Bill the verifier
    if (address(feeManager) != address(0)) {
      feeManager.processFee{value: msg.value}(payload, parameterPayload, msg.sender);
    }

    return _verify(payload);
  }
```

In the [`processFee`](https://github.com/smartcontractkit/chainlink/blob/9e74eee9d415b386db33bdf2dd44facc82cd3551/contracts/src/v0.8/llo-feeds/FeeManager.sol#L194) function, the `_handleFeesAndRewards` is called using parameters for `i_nativeAddress` not `i_linkaddress` since our chainlinkUtil library uses [that](https://github.com/Cyfrin/2024-07-zaros/blob/d687fe96bb7ace8652778797052a38763fbcbb1b/src/external/chainlink/ChainlinkUtil.sol#L83-L93) as our fee token and fee amount source.

```solidity
  function processFee(
    bytes calldata payload,
    bytes calldata parameterPayload,
    address subscriber
  ) external payable override onlyProxy {
//...
    if (fee.assetAddress == i_linkAddress) {
      _handleFeesAndRewards(subscriber, feeAndReward, 1, 0);
    } else {
      _handleFeesAndRewards(subscriber, feeAndReward, 0, 1);
    }
  }
```

In [`_handleFeesAndRewards`](https://github.com/smartcontractkit/chainlink/blob/9e74eee9d415b386db33bdf2dd44facc82cd3551/contracts/src/v0.8/llo-feeds/FeeManager.sol#L441-L457), we can see how the fee is handled. If msg.value is not sent, an attempt is made to transfer the `i_nativeAddress` from the subscriber, in this case, our msg.sender in VerifierProxy.sol, which is the contract that started the entire chain, (not the libraries) which is SettlementBranch.sol.

```solidity
  function _handleFeesAndRewards(
    address subscriber,
    FeeAndReward[] memory feesAndRewards,
    uint256 numberOfLinkFees,
    uint256 numberOfNativeFees
  ) internal {
//...
    if (msg.value != 0) {
      //there must be enough to cover the fee
      if (totalNativeFee > msg.value) revert InvalidDeposit();

      //wrap the amount required to pay the fee & approve as the subscriber paid in wrapped native
      IWERC20(i_nativeAddress).deposit{value: totalNativeFee}();

      unchecked {
        //msg.value is always >= to fee.amount
        change = msg.value - totalNativeFee;
      }
    } else {
      if (totalNativeFee != 0) {
        //subscriber has paid in wrapped native, so transfer the native to this contract
        IERC20(i_nativeAddress).safeTransferFrom(subscriber, address(this), totalNativeFee);
      }
    }
//...
  }
```

And by [going through](https://github.com/search?q=repo%3ACyfrin%2F2024-07-zaros+%22approve%22\&type=code) SettlementBranch.sol, or the entire codebase, there's no instance of the the FeeManager being approved to transfer `i_nativeAddress` tokens, which according to [arbiscan](https://arbiscan.io/address/0x5d70bd17b04efc1a1846177a49897fa532037df8#readContract#F3) is WETH.

## Impact

In conclusion, any of the functions that require offchain price verification stand the risk of failure, due to fees not being sent as ETH, or chainlink's fee manager being approved to transfer its wrapped counter part. And as a result, such functions will fail.
The function chain to follow goes like this:

`verifyReport` -> `verifyDataStreamsReport` ->  `verifyOffchainPrice` -> `fillOffchainOrders` & `fillMarketOrder`
`fillMarketOrder` is further user in MarketOrderKeeper.sol in the `performUpkeep` function.

## Tools Used

Manual Code Review

## Recommendations

Introduce a payable or receive functionality in the needed contract. Alternatively, approve the feemanager to spend the feeamount of the nativeaddress token before verification.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Zaros |
| Report Date | N/A |
| Finders | 0xStalin, blutorque, inh3l, inzinko, ke1caM, Slavcheww, holydevoti0n, Spearmint, cryptomoon, Infect3d, AlexCzm, ilchovski |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-07-zaros
- **Contest**: https://codehawks.cyfrin.io/c/clyg8slke0001bvhpwszwjr7z

### Keywords for Search

`vulnerability`

