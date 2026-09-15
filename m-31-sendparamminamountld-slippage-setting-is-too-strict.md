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
solodit_id: 32354
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-tapioca
source_link: https://code4rena.com/reports/2024-02-tapioca
github_link: https://github.com/code-423n4/2024-02-tapioca-findings/issues/14

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - ladboy233
---

## Vulnerability Title

[M-31] `sendParam.minAmountLD` slippage setting is too strict

### Overview


The bug report discusses an issue with the `minAmountLD` and `amountLD` values being set to the same amount in the code. This causes problems with cross-chain transactions and can result in the asset transfer being blocked. To fix this issue, the report recommends allowing users to input a percentage and computing the `minAmountLD` based on that percentage. This bug falls under the category of Token-Transfer and has been confirmed by a user named Tapioca, who also provided a comment.

### Original Finding Content


Across the codebase, the `minAmonutLD` and `amountLD` is set to equal value:

     if (data.collateralAmount > 0) {
                address collateralWithdrawReceiver = data.withdrawCollateralParams.withdraw ? address(this) : data.user;
                uint256 collateralShare = _yieldBox.toShare(_market.collateralId(), data.collateralAmount, false);

                (Module[] memory modules, bytes[] memory calls) = IMarketHelper(data.marketHelper).removeCollateral(
                    data.user, collateralWithdrawReceiver, collateralShare
                );
                _market.execute(modules, calls, true);

                //withdraw
                if (data.withdrawCollateralParams.withdraw) {
                    uint256 collateralId = _market.collateralId();
                    if (data.withdrawCollateralParams.assetId != collateralId) revert Magnetar_WithdrawParamsMismatch();

                    // @dev re-calculate amount
                    if (collateralShare > 0) {
                        uint256 computedCollateral = _yieldBox.toAmount(collateralId, collateralShare, false);
                        if (computedCollateral == 0) revert Magnetar_WithdrawParamsMismatch();

                        data.withdrawCollateralParams.lzSendParams.sendParam.amountLD = computedCollateral;
                        data.withdrawCollateralParams.lzSendParams.sendParam.minAmountLD = computedCollateral;
                        _withdrawToChain(data.withdrawCollateralParams);
                    }
                }
            }

However, `minAmonutLD` served as a slippage control on layerzero v2 side, and 0% slippage is not always possible. The cross-chain transaction will always reverted in too strict slippage contract and block asset transfer.

<https://github.com/LayerZero-Labs/LayerZero-v2/blob/142846c3d6d51e3c2a0852c41b4c2b63fcda5a0a/oapp/contracts/oft/OFTCore.sol#L345>


     function _debitView(
            uint256 _amountLD,
            uint256 _minAmountLD,
            uint32 /*_dstEid*/
        ) internal view virtual returns (uint256 amountSentLD, uint256 amountReceivedLD) {
            // @dev Remove the dust so nothing is lost on the conversion between chains with different decimals for the token.
            amountSentLD = _removeDust(_amountLD);
            // @dev The amount to send is the same as amount received in the default implementation.
            amountReceivedLD = amountSentLD;

            // @dev Check for slippage.
            if (amountReceivedLD < _minAmountLD) {
                revert SlippageExceeded(amountReceivedLD, _minAmountLD);
            }
        }

### Recommended Mitigation Steps

Let user input a percentage and compute `minAmountLD` based on a percentage of slippage user is willing to take risk of.

### Assessed type

Token-Transfer

**[cryptotechmaker (Tapioca) confirmed, but disagreed with severity and commented](https://github.com/code-423n4/2024-02-tapioca-findings/issues/14#issuecomment-2044438123):**
 > Slippage is only for EVM to Non-EVM transfers. We're good for now. 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tapioca DAO |
| Report Date | N/A |
| Finders | ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-tapioca
- **GitHub**: https://github.com/code-423n4/2024-02-tapioca-findings/issues/14
- **Contest**: https://code4rena.com/reports/2024-02-tapioca

### Keywords for Search

`vulnerability`

