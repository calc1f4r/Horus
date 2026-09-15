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
solodit_id: 31434
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-03] Multisig wallets that call `StargateLbpHelper.participate()` could cause received token to be stolen

### Overview


This bug report is about a function called `StargateLbpHelper.participate()` which is used to transfer tokens between different blockchains and then swap them using a pool called Balancer Liquidity Bootstrapping Pool. The issue is that the destination address for the swap is hardcoded to be the same as the sender's address, which can cause problems if the sender is a multisig wallet contract. This is because the wallet owners may not have control over the same address on the destination chain, resulting in lost tokens. In the worst case, an attacker could potentially steal the tokens by taking control of the sender's address on the destination chain. To fix this, the report recommends allowing the caller to specify the destination address for the swap instead of it being hardcoded.

### Original Finding Content

**Severity**

**Impact:** High, as received tokens on destination chain will be lost

**Likelihood:** Medium, this occurs when caller is a multisig wallet contract

**Description**

`StargateLbpHelper.participate()` is used to perform a cross chain transfer to the host chain and then a swap using the Balancer Liquidity Bootstrapping Pool.

The issue is that the receiver address of the LBP swap on the destination chain is hardcoded to `msg.sender` (passed in by `participate()`).

This will be a problem if `msg.sender` is a multisig wallet contract, as the wallet owners may not have control over the same address as `msg.sender` on the destination chain, causing the received tokens to be lost (if the recipient is not willing to return the funds).

In the worst case, the tokens could be sent to an undeployed address and an attacker could seize the opportunity to possibly steal the received tokens by taking control of the `msg.sender` address on destination chain (see [Wintermute hack article](https://rekt.news/wintermute-rekt/)).

```Solidity
    function participate(
        StargateData calldata stargateData,
        ParticipateData calldata lbpData
    ) external payable nonReentrant {
       ...
        router.swap{value: msg.value}(
            stargateData.dstChainId,
            stargateData.srcPoolId,
            stargateData.dstPoolId,
            payable(msg.sender),
            stargateData.amount,
            amountWithSlippage,
            IStargateRouterBase.lzTxObj({
                dstGasForCall: 0,
                dstNativeAmount: 0,
                dstNativeAddr: "0x0"
            }),
            abi.encodePacked(msg.sender),
            abi.encode(lbpData, msg.sender) //@audit receiver address on destination chain should be a parameter and not msg.sender
        );


    function sgReceive(
        uint16,
        bytes memory,
        uint256,
        address token,
        uint256 amountLD,
        bytes memory payload
    ) external {
        ...
        // decode payload
        (ParticipateData memory data, address receiver) = abi.decode( //@audit receiver is set to msg.sender
            payload,
            (ParticipateData, address)
        );
       ...
        IBalancerVault.FundManagement memory fundManagement = IBalancerVault
            .FundManagement({
                sender: address(this),
                recipient: payable(receiver), //@audit token is sent to receiver (which is msg.sender on src chain)
                fromInternalBalance: false,
                toInternalBalance: false
            });

        IERC20(data.assetIn).approve(address(lbpVault), 0);
        IERC20(data.assetIn).approve(address(lbpVault), amountLD);
        lbpVault.swap(
            singleSwap,
            fundManagement,
            data.minAmountOut,
            (data.deadline != 0 ? data.deadline : block.timestamp)
        );
    }

```

**Recommendations**

Allow caller to pass in the `receiver` address for the LBP swap.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

