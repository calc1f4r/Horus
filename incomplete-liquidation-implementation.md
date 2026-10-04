---
# Core Classification
protocol: Pike
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47965
audit_firm: OtterSec
contest_link: https://www.pike.finance/
source_link: https://www.pike.finance/
github_link: https://github.com/nutsfinance/pike-universal

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
  - Robert Chen
  - Woosun Song
  - OtterSec
---

## Vulnerability Title

Incomplete Liquidation Implementation

### Overview


The liquidation process in the Pike Finance system has several issues that need to be addressed. Firstly, the liquidator is not required to make any payment, even though they are supposed to purchase collateral from a potentially unhealthy position and repay the associated loan. Secondly, the debt owner receives the collateral instead of the liquidator. Finally, the liquidation process can be invoked on any debt regardless of its position and health. These issues need to be fixed by re-implementing the liquidation process. The bug has been fixed in the latest updates.

### Original Finding Content

## Liquidation Logic Issues

The implemented liquidation logic is incorrect for multiple reasons.

## 1. Liquidator Payment

First, the liquidator does not incur any payment. The liquidation process involves the liquidator purchasing collateral from a potentially unhealthy position, which should result in the liquidator being responsible for repaying the loan associated with that position. However, the current implementation lacks validation or enforcement of the repayment amount indicated by the `repayAmount` variable.

```solidity
src/contracts/spoke/SpokeHandler.sol SOLIDITY
function initiateLiquidation(
    uint16 targetChainId,
    address borrower,
    address liquidator,
    uint256 repayAmount
)
internal
{
    require(isActive, Errors.SPOKE_NOT_ACTIVE);
    require(targetChainId == spokeChainId, Errors.INVALID_ARGUMENTS);
    require(borrower != address(0), Errors.ZERO_ADDRESS_NOT_VALID);
    require(msg.value > 0, Errors.ZERO_VALUE_PROVIDED);
    
    bytes memory payload = abi.encode(
        DataTypes.HubLiquidate({
            action: DataTypes.Action.HUB_LIQUIDATE,
            user: borrower,
            liquidator: liquidator,
            repayAmount: repayAmount,
            sourceChainId: spokeChainId,
            targetChainId: targetChainId
        })
    );

    if (spokeChainId == hubChainId) {
        // We are on hub, skip cross-chain messaging
        IGateway(gateway).pike_send_intrachain(
            DataTypes.Transport.INTRACHAIN,
            hubChainId,
            payload,
            payable(liquidator),
            address(0)
        );
    } else {
        (uint256 fee,) = estimateTransportCost(hubChainId, GAS_LIMIT);
        (uint256 forwardFee,) = estimateTransportCost(targetChainId, GAS_LIMIT);
        require(msg.value > fee + forwardFee, Errors.INVALID_ARGUMENTS);
        
        IGateway(gateway).pike_send{value: msg.value}(
            DataTypes.Transport.WORMHOLE,
            hubChainId,
            payload,
            payable(liquidator),
            address(0)
        );
    }
}
```

## 2. Collateral Recipient

Second, the debt owner receives the collateral instead of the liquidator. Currently, the recipient of the collateral is set as `params.user`, which represents the debt opener. `params.user` should be revised to `params.liquidator` instead.

```solidity
src/contracts/spoke/SpokeHandler.sol SOLIDITY
function confirmLiquidation(
    DataTypes.SpokeLiquidate memory params,
    bytes32 sourceAddress,
    uint16 sourceChainId
)
internal
onlyHubChain(sourceAddress, sourceChainId)
{
    require(params.targetChainId == spokeChainId, Errors.SPOKE_NOT_FOUND);
    require(params.user != params.liquidator, Errors.INVALID_ARGUMENTS);
    require(
        address(pikeToken).balance >= params.totalDiscounted,
        Errors.RESERVE_NOT_ENOUGH
    );
    require(params.user != address(0), Errors.ZERO_ADDRESS_NOT_VALID);
    
    PikeToken(pikeToken).safeTransfer(payable(params.user), params.totalDiscounted);
}
```

## 3. Health Factor Check

Third, liquidation may be invoked on any debt regardless of position and health. The hub’s liquidation logic does not compute the health factor of the debt and performs liquidations regardless of it.

```solidity
src/contracts/hub/HubMessageHandler.sol SOLIDITY
DataTypes.HubLiquidate memory params,
bytes32 sourceAddress
)
external
payable
onlyAuthorizedGateway
onlyAuthorizedChannels(sourceAddress)
{
    require(params.user != params.liquidator, Errors.INVALID_ARGUMENTS);
    /* ... */
    
    uint256 userBalance = collateralBalances[params.targetChainId][params.user];
    uint256 maxLiquidatableAmount = userBalance * closeFactor / DECIMALS;
    uint256 discount = params.repayAmount * DECIMALS / (1e18 - liquidationDiscount);
    uint256 penalty = params.repayAmount * liquidationPenalty / DECIMALS;
    
    require(maxLiquidatableAmount >= discount, "Liquidator receives more");
    collateralBalances[params.targetChainId][params.user] -= penalty + discount;
    userBorrows[params.targetChainId][params.user].principal -= params.repayAmount;
    totalBorrows[params.targetChainId] -= params.repayAmount;
    totalReserves[params.targetChainId] += penalty;

    /* ... */
}
```

## Remediation

Re-implement the liquidation process to satisfy the above requirements.

### Patch

Fixed in commits `9b55707`, `25feb31`, `68261d4`, and `8349624`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pike |
| Report Date | N/A |
| Finders | Robert Chen, Woosun Song, OtterSec |

### Source Links

- **Source**: https://www.pike.finance/
- **GitHub**: https://github.com/nutsfinance/pike-universal
- **Contest**: https://www.pike.finance/

### Keywords for Search

`vulnerability`

