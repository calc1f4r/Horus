---
# Core Classification
protocol: Malda
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62732
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1029
source_link: none
github_link: https://github.com/sherlock-audit/2025-07-malda-judging/issues/304

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

# Audit Details
report_date: unknown
finders_count: 13
finders:
  - ExtraCaterpillar
  - 0xmechanic
  - ZanyBonzy
  - bulgari
  - elolpuer
---

## Vulnerability Title

M-9: The rebalancing system is broken when everclear bridge contract is used

### Overview


Summary:

The bug report discusses an issue with the EverclearBridge contract in the Malda Protocol. The sendMsg function in the contract only approves the transfer amount for the FeeAdapter, but the FeeAdapter attempts to pull both the amount and the fee from the bridge contract. This results in a revert due to insufficient allowance, causing cross-chain rebalancing to fail. The root cause is a mismatch between the approved amount and the actual amount required by the FeeAdapter. This can be fixed by updating the allowance logic in the EverclearBridge contract. The impact of this bug is that all cross-chain rebalancing operations using EverclearBridge will fail. The protocol team has fixed this issue in a recent PR. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-07-malda-judging/issues/304 

## Found by 
0xmechanic, 10ap17, Angry\_Mustache\_Man, Cybrid, ExtraCaterpillar, PeterSR, ZanyBonzy, bube, bulgari, dan\_\_vinci, elolpuer, farismaulana, oxwhite

### Summary

The [sendMsg](https://github.com/sherlock-audit/2025-07-malda/blob/798d00b879b8412ca4049ba09dba5ae42464cfe7/malda-lending/src/rebalancer/bridges/EverclearBridge.sol#L110) in EverclearBridge contract only approves the **transfer amount** (not including the fee) for the **FeeAdapter** when calling `newIntent`. However, the **FeeAdapter** attempts to pull **both the amount and the fee** from the bridge contract. This results in a revert due to insufficient allowance causing cross-chain rebalancing to fail. 

### Root Cause

The root case stem from  a mismatch between the **approved amount** and the **actual amount required** by the `FeeAdaptor`.

The sendMsg() in everclearBridge.sol is as follows: 
```solidity
 function sendMsg(
        uint256 _extractedAmount,
        address _market,
        uint32 _dstChainId,
        address _token,
        bytes memory _message,
        bytes memory // unused
    ) external payable onlyRebalancer {
        IntentParams memory params = _decodeIntent(_message);

        require(params.inputAsset == _token, Everclear_TokenMismatch());
        require(_extractedAmount >= params.amount, BaseBridge_AmountMismatch());

        uint256 destinationsLength = params.destinations.length;
        require(destinationsLength > 0, Everclear_DestinationsLengthMismatch());

        bool found;
        for (uint256 i; i < destinationsLength; ++i) {
            if (params.destinations[i] == _dstChainId) {
                found = true;
                break;
            }
        }
        require(found, Everclear_DestinationNotValid());

        if (_extractedAmount > params.amount) {
            uint256 toReturn = _extractedAmount - params.amount;
 @>           IERC20(_token).safeTransfer(_market, toReturn);//@audit-info the excess is sent back to the market
            emit RebalancingReturnedToMarket(_market, toReturn, _extractedAmount);
        }

 @>       SafeApprove.safeApprove(params.inputAsset, address(everclearFeeAdapter), params.amount);//@audit approve is done for amount
        (bytes32 id,) = everclearFeeAdapter.newIntent(
            params.destinations,
            params.receiver,
            params.inputAsset,
            params.outputAsset,
            params.amount,
            params.maxFee,
            params.ttl,
            params.data,
            params.feeParams
        );
        emit MsgSent(_dstChainId, _market, params.amount, id);
    }
```
The [newIntent](https://etherscan.io/address/0x15a7cA97D1ed168fB34a4055CEFa2E2f9Bdb6C75#code) method in  feeAdaptor contract is  defined as: 
```solidity
/// @inheritdoc IFeeAdapter
  function newIntent(
    uint32[] memory _destinations,
    bytes32 _receiver,
    address _inputAsset,
    bytes32 _outputAsset,
    uint256 _amount,
    uint24 _maxFee,
    uint48 _ttl,
    bytes calldata _data,
    IFeeAdapter.FeeParams calldata _feeParams
  ) external payable returns (bytes32 _intentId, IEverclear.Intent memory _intent) {
    // Transfer from caller
@>    _pullTokens(msg.sender, _inputAsset, _amount + _feeParams.fee);//@audit amount+fee is pulled from bridge contract

    // Create intent
    (_intentId, _intent) =
      _newIntent(_destinations, _receiver, _inputAsset, _outputAsset, _amount, _maxFee, _ttl, _data, _feeParams);
  }
```
As shown, `_amount + _feeParams.fee` is pulled from bridge contract, which will  result in revert as the approve was done only for the specified amount. 

### Internal Pre-conditions
There is an imbalance and `sendMsg` is invoked in the  rebalancer contract.  

### External Pre-conditions
Market B requires rebalancing
Assets are available in Market A


### Attack Path

1. Market A on X chain has **12,000 USDC** extractable value.
2. Market B on Y chain  needs **10,000 USDC**.
3. The `sendMsg()` function is invoked in the `Rebalancer` contract with `_amount = 12,000 USDC`.
4. The **12,000 USDC** is sent to the `EverclearBridge` contract. Since the extracted amount is greater than the amount specified in the message, the excess **2,000 USDC** is sent back to Market A.
5. The `FeeAdaptor` contract is **approved** for only **10,000 USDC**.
6. The `newIntent()` function is called on the `FeeAdaptor`. This function attempts to **pull `10,000 USDC + fee`**, but it **reverts** due to insufficient approval.
As result, the rebalancing will not succeed.

**Additinal Notes:** 
According to the [FeeAdaptor](https://etherscan.io/address/0x15a7cA97D1ed168fB34a4055CEFa2E2f9Bdb6C75#code) and [Spoke](https://etherscan.io/address/0xd18c19169e7c87e7d84f27ad412a56c5d743d560#code) contract logic in everclear platform, the fee is not deducted from the specified transfer amount but instead added on top during token transfer. Therefore, the fee cannot be zero, and any under-approval results in failure.
If the fee were instead deducted from the approved amount, Market B would receive less than 10,000 USDC, potentially leading to issues like insufficient liquidity.

### Impact
All cross-chain rebalancing operations using EverclearBridge  will fail.

### PoC
See the function flow and contract state change given above

### Mitigation

Update the allowance logic in EverclearBridge to approve enough amount for the FeeAdapter.



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/malda-protocol/malda-lending/pull/114/files


**CergyK**

Fix looks good





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Malda |
| Report Date | N/A |
| Finders | ExtraCaterpillar, 0xmechanic, ZanyBonzy, bulgari, elolpuer, dan\_\_vinci, 10ap17, farismaulana, Cybrid, Angry\_Mustache\_Man, dan\_\_vinci, PeterSR, bube, oxwhite |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-07-malda-judging/issues/304
- **Contest**: https://app.sherlock.xyz/audits/contests/1029

### Keywords for Search

`vulnerability`

