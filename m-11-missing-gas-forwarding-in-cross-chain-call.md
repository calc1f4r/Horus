---
# Core Classification
protocol: Tapiocadao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31449
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-11] Missing gas forwarding in cross-chain call

### Overview


This bug report is about a problem with a function called `TOFT_REMOVE_AND_REPAY` in the `MagnetarV2.sol` contract. This function is used to exit a position and remove collateral from a market. However, when the function is called, it sends out a LayerZero call, but no gas is forwarded to it. This means that the external call will have a `msg.value` of 0, which causes it to fail. The recommendation is to modify the call in `MagnetarV2.sol` to forward the gas by adding `{value: _action.value}` to the call. This will fix the issue and allow the function to work properly.

### Original Finding Content

**Severity**

**Impact**: Medium, broken functionality of an important function

**Likelihood**: Medium, `TOFT_REMOVE_AND_REPAY` operation always reverts when called

**Description**

The operation `TOFT_REMOVE_AND_REPAY` is used to exit a position and then remove collateral from a market. The issue is that the function being called sends out a LayerZero call, but no gas is forwarded to it.

The function call can be found in `MagnetarV2.sol` contract under the action id `TOFT_REMOVE_AND_REPAY` as shown below.

```solidity
if (_action.id == TOFT_REMOVE_AND_REPAY) {
                HelperTOFTRemoveAndRepayAsset memory data = abi.decode(
                    _action.call[4:],
                    (HelperTOFTRemoveAndRepayAsset)
                );

                _checkSender(data.from);
                IUSDOBase(_action.target).removeAsset(
                    data.from,
                    data.to,
                    data.lzDstChainId,
                    data.zroPaymentAddress,
                    data.adapterParams,
                    data.externalData,
                    data.removeAndRepayData,
                    data.approvals,
                    data.revokes
                );
```

Since no gas is forwarded to the external call, the external call will have `msg.value` of 0. However if we check the `removeAsset` function in BaseUSDO.sol, we see a subsequent layerzero call via the USDOMarketModule.

```solidity
bytes memory lzPayload = abi.encode(
            PT_MARKET_REMOVE_ASSET,
            to,
            externalData,
            removeAndRepayData,
            approvals,
            revokes,
            airdropAmount
        );

        _checkAdapterParams(
            lzDstChainId,
            PT_MARKET_REMOVE_ASSET,
            adapterParams,
            NO_EXTRA_GAS
        );

        _lzSend(
            lzDstChainId,
            lzPayload,
            payable(from),
            zroPaymentAddress,
            adapterParams,
            msg.value
        );
```

The issue here is that `msg.value` is 0, hence no gas will be sent to the layerzero endpoint, failing the cross-chain call.

**Recommendations**

Modify the call in magnetar to forward the gas.

```solidity
 IUSDOBase(_action.target).removeAsset{value: _action.value}(...)
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tapiocadao |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

