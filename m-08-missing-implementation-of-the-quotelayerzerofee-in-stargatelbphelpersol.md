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
solodit_id: 31446
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

[M-08] Missing implementation of the `quoteLayerZeroFee()` in StargateLbpHelper.sol

### Overview


The report discusses a bug in the `participate()` function used for cross-chain transfers. The function calls the `swap` method using Stargate router, but there is no implementation of the `quoteLayerZero()` function to calculate the required fee. This means that users do not know how much fee to send for the transfer to be successful, leading to a high likelihood of failure. The recommendation is to implement the `quoteLayerZero()` function as described in the Stargate documentation.

### Original Finding Content

**Severity**

**Impact**: Low, because the user can still use `participate()` without this implementation.

**Likelihood**: High, because there is no implementation of this function.

**Description**

We use the `participate()` function when we want to do a cross-chain transfer. The function calls the `swap` method using Stargate router:

```solidity
        router.swap{value: msg.value}(
            stargateData.dstChainId,
            stargateData.srcPoolId,
            stargateData.dstPoolId,
            payable(msg.sender), //refund address
            stargateData.amount,
            amountWithSlippage,
            IStargateRouterBase.lzTxObj({
                dstGasForCall: 0,
                dstNativeAmount: 0,
                dstNativeAddr: "0x0"
            }),
            abi.encodePacked(msg.sender), // StargateLbpHelper.sol destination address
            abi.encode(lbpData, msg.sender)
        );
```

To pay `fee` we send `msg.value`:

```solidity
swap{value:msg.value}
```

From Stargate [documentation](https://stargateprotocol.gitbook.io/stargate/developers/how-to-swap) we see that we have to call `quoteLayerZero()` to calculate the fee.

> For the native gas fee required for `swap()` you need to call `quoteLayerZero()` on the Router.sol contract to get the amount you should send as msg.value.

But such a function is missing. Because of this, we don't know how many fees to send for the transfer to be successful. If we send more than needed it will refund, but if we send less than needed the cross-chain transfer will fail.

**Recommendations**

Implement the `quoteLayerZeroFee()` function. See the [documentation](https://stargateprotocol.gitbook.io/stargate/developers/cross-chain-swap-fee) for more information.

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

