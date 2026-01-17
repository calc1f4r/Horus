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
solodit_id: 31461
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-07] `StargateLbpHelper.participate()` could leave dust amount in contract

### Overview

See description below for full details.

### Original Finding Content

In `StargateLbpHelper.participate()`, `stargateData.amount` of `srcToken` is transferred into the contract and then sent to another chain via Stargate `router.swap()`.

However, Stargate `router.swap()` may send less than the entire `stargateData.amount` due to a conversion that will leave dust amount in the contract. This will occur for tokens that has different decimals on different chains, where Stargate router will convert from a local decimals (on source chain) to a shared decimals (normalized for all chains).

For example, Stargate LUSD pool has a local decimals of 18 for Optimism and shared decimals of 6. So the conversion (from local decimals to shared decimals and then back to local decimals) will remove the dust amount that is not represented in shared decimals, which is lower than local decimals.

```Solidity
    function participate(
        StargateData calldata stargateData,
        ParticipateData calldata lbpData
    ) external payable nonReentrant {
        IERC20 erc20 = IERC20(stargateData.srcToken);

        // retrieve source token from sender
        erc20.safeTransferFrom(msg.sender, address(this), stargateData.amount);

        // compute min amount to be received on destination
        uint256 amountWithSlippage = stargateData.amount -
            ((stargateData.amount * stargateData.slippage) /
                SLIPPAGE_PRECISION);

        // approve token for Stargate router
        erc20.safeApprove(address(router), stargateData.amount);

        //@audit this could leave dust amount due to a conversion within swap()
        // send over to another layer using the Stargate router
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
    }
```

```Solidity
    function swap(
        uint16 _dstChainId,
        uint256 _srcPoolId,
        uint256 _dstPoolId,
        address payable _refundAddress,
        uint256 _amountLD,
        uint256 _minAmountLD,
        lzTxObj memory _lzTxParams,
        bytes calldata _to,
        bytes calldata _payload
    ) external payable override nonReentrant {
        require(_amountLD > 0, "Stargate: cannot swap 0");
        require(_refundAddress != address(0x0), "Stargate: _refundAddress cannot be 0x0");
        Pool.SwapObj memory s;
        Pool.CreditObj memory c;
        {
            Pool pool = _getPool(_srcPoolId);
            {
                uint256 convertRate = pool.convertRate();
                //@audit this converts from local decimals to shared decimals and then back to local decimals.
                //            it will remove dust amount that is not represented in shared decimals
                _amountLD = _amountLD.div(convertRate).mul(convertRate);
            }

            s = pool.swap(_dstChainId, _dstPoolId, msg.sender, _amountLD, _minAmountLD, true);
            _safeTransferFrom(pool.token(), msg.sender, address(pool), _amountLD);
            c = pool.sendCredits(_dstChainId, _dstPoolId);
        }
        bridge.swap{value: msg.value}(_dstChainId, _srcPoolId, _dstPoolId, _refundAddress, c, s, _lzTxParams, _to, _payload);
    }
```

This could be resolved by checking the actual amount that was transferred by `router.swap` and use it to determine the leftover dust that will be refunded to the caller.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

