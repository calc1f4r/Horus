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
solodit_id: 37974
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
  - samuraii77
  - KiteWeb3
  - crunter
  - Draiakoo
---

## Vulnerability Title

QA Report - 0xStalin - Low Severities

### Overview

See description below for full details.

### Original Finding Content

````markdown
## L-01
## Title
Not validating if the report pulled from the DataStream has expired

## Vulnerability Details
The [Chainlink DataStreams](https://docs.chain.link/data-streams/tutorials/streams-direct/streams-direct-onchain-verification#examine-the-code) returns data encoded as bytes. There is a parameter called [`expiresAt`](https://github.com/Cyfrin/2024-07-zaros/blob/main/src/external/chainlink/interfaces/IStreamsLookupCompatible.sol#L23) that determines the latest timestamp where the report can be verified onchain. But, the [`SettlementConfiguration.requireDataStreamsReportIsValid() function`](https://github.com/Cyfrin/2024-07-zaros/blob/main/src/perpetuals/leaves/SettlementConfiguration.sol#L87-L103) doesn't use it to validate if the report has expired or not.


## Impact
Perpetual Markets may work with expired data.

## Tools Used
Manual Audit

## Recommendations
Validate if the report has expired or not.

```
function requireDataStreamsReportIsValid(
    bytes32 streamId,
    bytes memory verifiedReportData,
    uint256 maxVerificationDelay
)
    internal
    view
{
    PremiumReport memory premiumReport = abi.decode(verifiedReportData, (PremiumReport));

    if (
        streamId != premiumReport.feedId
            || block.timestamp > premiumReport.validFromTimestamp + maxVerificationDelay
+           || block.timestamp >= premiumReport.expiresAt
    ) {
        revert Errors.InvalidDataStreamReport(streamId, premiumReport.feedId);
    }
}
```

------
## L-02
## Title
Not disabling initializer on the UpgradeBranch contract

## Vulnerability Details
uninitialized implementation [UpgradeBranch contract](https://github.com/Cyfrin/2024-07-zaros/blob/main/src/tree-proxy/branches/UpgradeBranch.sol) can be taken over by an attacker with initialize function, it’s recommended to invoke the _disableInitializers function in the constructor to prevent the implementation contract from being used by the attacker.


## Impact
Attacker could take over the ownership of the UpgradeBranch contract before it is initialized.

## Tools Used
Manual Audit & [Solodit Report](https://solodit.xyz/issues/no-protection-of-uninitialized-implementation-contracts-from-attacker-fixed-consensys-none-leequid-staking-markdown)

## Recommendations
Invoke _disableInitializers() in the constructors of the UpgradeBranch contract

------
## L-03
## Title
Traders can't set different referralCodes for each of their trading accounts.

## Vulnerability Details
When a TradingAccount is created, the owner is allowed to set a referral code or use a customReferralCode that will be associated to a specific address.
The problem is that [the Referral.Data is loaded based on the `msg.sender`](https://github.com/Cyfrin/2024-07-zaros/blob/main/src/perpetuals/branches/TradingAccountBranch.sol#L254-L277), or in other words, the referral data is stored per Trader, instead of being stored per Account.

This means, Traders are forced to use the same referral code across all of their accounts.

```
    function createTradingAccount(
        bytes memory referralCode,
        bool isCustomReferralCode
    )
        public
        virtual
        returns (uint128 tradingAccountId)
    {
        ...

        //@audit-issue => The referral data is loaded based on the msg.sender.
        //@audit-issue => All the TradingAccounts owned by the same msg.sender are forced to use the same referral code.
        Referral.Data storage referral = Referral.load(msg.sender);

        if (referralCode.length != 0 && referral.referralCode.length == 0) {
            if (isCustomReferralCode) {
                CustomReferralConfiguration.Data storage customReferral =
                    CustomReferralConfiguration.load(string(referralCode));
                if (customReferral.referrer == address(0)) {
                    revert Errors.InvalidReferralCode();
                }
                referral.referralCode = referralCode;
                referral.isCustomReferralCode = true;
            } else {
                address referrer = abi.decode(referralCode, (address));

                if (referrer == msg.sender) {
                    revert Errors.InvalidReferralCode();
                }

                referral.referralCode = referralCode;
                referral.isCustomReferralCode = false;
            }

            emit LogReferralSet(msg.sender, referral.getReferrerAddress(), referralCode, isCustomReferralCode);
        }

        return tradingAccountId;
    }
```

## Impact
Traders are forced to use the same referral code across all of their accounts.

## Tools Used
Manual Audit

## Recommendations
Handle the referral at a TradingAccount level. Allow Account owners to set a different referral code on each of their TradingAccounts.

------
## L-04
## Title
Users can grief the Offchain keeper to waste gas by submitting invalid offchain orders causing the tx to revert, and as such, all the valid orders submited on the same batch will also revert

## Vulnerability Details
When filling an offchain order, [the execution validates if the signer of the current offchain order being filled is actually the owner of the TradingAccount that the order was requested for](https://github.com/Cyfrin/2024-07-zaros/blob/main/src/perpetuals/branches/SettlementBranch.sol#L260-L270). The grieffing is possible because if the signer is not the owner, the entire tx is reverted, and, by reverting the entire tx, the rest of valid orders that could have been filled will also be reverted.

The attacker spends 0 gas because signing an offchain message costs nothing, its free.

This allows attackers to submit offchain orders for TradingAccounts they don't own and that the filling offchain order execution will revert. This will cause that the offchain keeper txs reverts and spends gas on attempting to fill an offchain order that will revert anyways.

```
function fillOffchainOrders(
    uint128 marketId,
    OffchainOrder.Data[] calldata offchainOrders,
    bytes calldata priceData
)
    external
    onlyOffchainOrdersKeeper(marketId)
{
    ...

    for (uint256 i; i < offchainOrders.length; i++) {
        ...

        //@audit => Recovering the original signer of the offchain signature requesting an OffchainOrder!
        // `ecrecover`s the order signer.
        ctx.signer = ECDSA.recover(
            _hashTypedDataV4(ctx.structHash), ctx.offchainOrder.v, ctx.offchainOrder.r, ctx.offchainOrder.s
        );

        // ensure the signer is the owner of the trading account, otherwise revert.
        // NOTE: If an account's owner transfers to another address, this will fail. Therefore, clients must
        // cancel all users offchain orders in that scenario.

        //@audit-issue => Reverting instead of continuing to the next offchain order!
        if (ctx.signer != tradingAccount.owner) {
            revert Errors.InvalidOrderSigner(ctx.signer, tradingAccount.owner);
        }

        ...
    }
}

```

## Impact
Malicious user can make the Offchain Keeper to waste infinite gas without them spending a single wei of gas.

## Tools Used
Manual Audit

## Recommendations
Instead of reverting the tx, do a continue, in this way, the rest of valid orders can still be filled. All good with doing a continue, at this point, nothing has been saved in the storage related to the current order beeing filled.


------
## L-05
## Title
MarketOrders don't have price protection when being filled.

## Vulnerability Details
Traders who uses MarketOrders can not protected themselves against the price of the asset [when their order is filled](https://github.com/Cyfrin/2024-07-zaros/blob/main/src/perpetuals/branches/SettlementBranch.sol#L107-L166). In comparisson against the offchain orders, [Offchain Orders are protected to be filled within a correct range of price](https://github.com/Cyfrin/2024-07-zaros/blob/main/src/perpetuals/branches/SettlementBranch.sol#L236-L238) to allow the Trader execute the trade as planned.


## Impact
MarketOrders can be filled even if the filled price is not valid depending on the type of operation.

## Tools Used
Manual Audit

## Recommendations
Similar to when filling an offchain order, make sure to validate if the fillPrice is valid when filling MarketOrders.

This change will require to allow the Traders to define the `targetPrice` of their order when creating a MarketOrder!

```
function fillMarketOrder(
    uint128 tradingAccountId,
    uint128 marketId,
    bytes calldata priceData
)
    external
    onlyMarketOrderKeeper(marketId)
{
    ...

    //  buy order -> match against the ask price
    // sell order -> match against the bid price
    ctx.indexPriceX18 = ctx.isBuyOrder ? ctx.askX18 : ctx.bidX18;

    // verify the provided price data against the verifier and ensure it's valid, then get the mark price
    // based on the returned index price.
    ctx.fillPriceX18 = perpMarket.getMarkPrice(ctx.sizeDeltaX18, ctx.indexPriceX18);

    //@audit => Verify if the fillPrice is correct
    bool isFillPriceValid = (ctx.isBuyOrder && marketOrder.targetPrice <= ctx.fillPriceX18.intoUint256())
                || (!ctx.isBuyOrder && marketOrder.targetPrice >= ctx.fillPriceX18.intoUint256());

    if (!ctx.isFillPriceValid) {
        continue;
    }

    // perform the fill
    _fillOrder(
        tradingAccountId,
        marketId,
        SettlementConfiguration.MARKET_ORDER_CONFIGURATION_ID,
        ctx.sizeDeltaX18,
        ctx.fillPriceX18
    );

    // reset pending order details
    marketOrder.clear();
}

```
## L-06
## Title
Returning an empty array when checking the amount of liquidable accounts.

## Vulnerability Details
When the total amounts to be liquidated is <= the `peformLowerBound`, the [`LiquidationKeeper.checkUpkeep() function`](https://github.com/Cyfrin/2024-07-zaros/blob/main/src/external/chainlink/keepers/liquidation/LiquidationKeeper.sol#L44-L88) returns an empty array, instead of returning the array that contains the accounts that can be liquidated.

```
function checkUpkeep(bytes calldata checkData)
    external
    view
    returns (bool upkeepNeeded, bytes memory performData)
{
    (uint256 checkLowerBound, uint256 checkUpperBound, uint256 performLowerBound, uint256 performUpperBound) =
        abi.decode(checkData, (uint256, uint256, uint256, uint256));

    if (checkLowerBound >= checkUpperBound || performLowerBound >= performUpperBound) {
        revert Errors.InvalidBounds();
    }

    IPerpsEngine perpsEngine = _getLiquidationKeeperStorage().perpsEngine;

    //@audit => Checks the accounts from `checLowerBound to checkUpperBound` and determines which accounts are liquidables!
    uint128[] memory liquidatableAccountsIds =
        perpsEngine.checkLiquidatableAccounts(checkLowerBound, checkUpperBound);
    uint128[] memory accountsToBeLiquidated;

    if (liquidatableAccountsIds.length == 0 || liquidatableAccountsIds.length <= performLowerBound) {
        
        //@audit-issue => Returning the empty array.
        //@audit => The array that has the liquidable accounts is the `liquidatableAccountsIds`
        performData = abi.encode(accountsToBeLiquidated);

        return (upkeepNeeded, performData);
    }
}
```

## Impact
The function would return an empty array which means that there are no liquidable accounts, when in reality, there can be accounts to be liquidated.

## Tools Used
Manual Audit

## Recommendations
Return the `liquidatableAccountsIds` array instead of `accountsToBeLiquidated`

```
function checkUpkeep(bytes calldata checkData)
    external
    view
    returns (bool upkeepNeeded, bytes memory performData)
{
    (uint256 checkLowerBound, uint256 checkUpperBound, uint256 performLowerBound, uint256 performUpperBound) =
        abi.decode(checkData, (uint256, uint256, uint256, uint256));

    if (checkLowerBound >= checkUpperBound || performLowerBound >= performUpperBound) {
        revert Errors.InvalidBounds();
    }

    IPerpsEngine perpsEngine = _getLiquidationKeeperStorage().perpsEngine;

    uint128[] memory liquidatableAccountsIds =
        perpsEngine.checkLiquidatableAccounts(checkLowerBound, checkUpperBound);
    uint128[] memory accountsToBeLiquidated;

    if (liquidatableAccountsIds.length == 0 || liquidatableAccountsIds.length <= performLowerBound) {
        

+       performData = abi.encode(liquidatableAccountsIds);
-       performData = abi.encode(accountsToBeLiquidated);

        return (upkeepNeeded, performData);
    }
}
```

------
## L-07
## Title
No means for the PerpEngine to receive native to pay the Chainlink Verifier in case Chainlinks charges fees to the protocol

## Vulnerability Details
To [verify a report on the Chainlink DataStreams is required to pay a fee](https://github.com/Cyfrin/2024-07-zaros/blob/main/src/external/chainlink/ChainlinkUtil.sol#L95-L104). At the moment, the protocol has an arrenguement with Chainlink to not pay fees. But, in case in the future is required to pay for these fees, the contracts don't have any means to receive native tokens so that it can be used to pay for fees.

```
    function verifyReport(
        IVerifierProxy chainlinkVerifier,
        FeeAsset memory fee,
        bytes memory signedReport
    )
        internal
        returns (bytes memory verifiedReportData)
    {
        
        //@audit-issue => Contracts don't have a mechanism to receive native token so that it can be used to pay for these fees.
        verifiedReportData = chainlinkVerifier.verify{ value: fee.amount }(signedReport, abi.encode(fee.assetAddress));
    }

```

## Impact
The contracts won't be able to verify the report on the Chainlink DataStream, which that would cause a disruption to the system.

## Tools Used
Manual Audit

## Recommendations
Add a function that would allow the owners to fund the PerpsEngine contract with native token to pay for fees.

------
## L-08
## Title
Order of liquidation would liquidate collaterals with higher LTV first

## Vulnerability Details
When deducting margin from an account, [the collateralLiquidationPriority is iterated from the first item to the last](https://github.com/Cyfrin/2024-07-zaros/blob/main/src/perpetuals/leaves/TradingAccount.sol#L504-L508). If the order of the collateralLiquidation goes from collateral with the highest LTV to the collaterals with the lower LTV at the end, then, the collateral deducted from the TradingAccounts would first take the most stable collaterals.

```
function deductAccountMargin(
    ...
)
    internal
    returns (UD60x18 marginDeductedUsdX18)
{
    ...

    // cache collateral liquidation priority length
    uint256 cachedCollateralLiquidationPriorityLength = globalConfiguration.collateralLiquidationPriority.length();

    //@audit-issue => Iterating from the first item to the last
    // loop through configured collateral types
    for (uint256 i; i < cachedCollateralLiquidationPriorityLength; i++) {
        // get ith collateral type
        address collateralType = globalConfiguration.collateralLiquidationPriority.at(i);
        ...
    }
}
```

## Impact
Most stable collateral will be deducted first, leaving the TradingAccounts with a riskier basket of collaterals.

## Tools Used
Manual Audit

## Recommendations
Iterate from the last to the first collateral in the collateralLiquidationPriority.

```
function deductAccountMargin(
    ...
)
    internal
    returns (UD60x18 marginDeductedUsdX18)
{
    ...

    // cache collateral liquidation priority length
    uint256 cachedCollateralLiquidationPriorityLength = globalConfiguration.collateralLiquidationPriority.length();

    // loop through configured collateral types
+   for (uint256 i = cachedCollateralLiquidationPriorityLength - 1; i = 0; i--) {
-   for (uint256 i; i < cachedCollateralLiquidationPriorityLength; i++) {
        // get ith collateral type
        address collateralType = globalConfiguration.collateralLiquidationPriority.at(i);
        ...
    }
}
````

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Zaros |
| Report Date | N/A |
| Finders | 0xStalin, samuraii77, KiteWeb3, crunter, Draiakoo, KrisRenZo, Slavcheww, cryptomoon, ShahilHussain, 0xTheBlackPanther |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-07-zaros
- **Contest**: https://codehawks.cyfrin.io/c/clyg8slke0001bvhpwszwjr7z

### Keywords for Search

`vulnerability`

