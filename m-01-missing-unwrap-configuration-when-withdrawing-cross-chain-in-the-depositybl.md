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
solodit_id: 32324
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-tapioca
source_link: https://code4rena.com/reports/2024-02-tapioca
github_link: https://github.com/code-423n4/2024-02-tapioca-findings/issues/180

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
finders_count: 5
finders:
  - carrotsmuggler
  - 1
  - 2
  - KIntern\_NA
  - deadrxsezzz
---

## Vulnerability Title

[M-01] Missing unwrap configuration when withdrawing cross-chain in the `depositYBLendSGLLockXchainTOLP()` function of `MagnetarAssetXChainModule` results in being unable to lock and participate on the destination chain

### Overview


The `depositYBLendSGLLockXchainTOLP()` function is used to lend into Singularity and then withdraw the Singularity tokens cross-chain to lock and participate on the destination chain. However, when the function tries to acquire YieldBox's shares of the original Singularity tokens, it fails to unwrap the tokens and cannot complete the locking process. To fix this, the function should call `_withdrawToChain()` with `unwrap` set to true. This bug has been confirmed and fixed by the Tapioca team.

### Original Finding Content


The `depositYBLendSGLLockXchainTOLP()` function attempts to lend into Singularity, then withdraws the Singularity tokens cross-chain to lock and participate on the destination chain. The Singularity tokens are wrapped as TOFT tokens to facilitate cross-chain transfer.

```solidity
uint256 fraction =
    _depositYBLendSGL(data.depositData, data.singularity, IYieldBox(yieldBox), data.user, data.lendAmount);

// wrap SGL receipt into tReceipt
// ! User should approve `address(this)` for `IERC20(data.singularity)` !
uint256 toftAmount = _wrapSglReceipt(IYieldBox(yieldBox), data.singularity, data.user, fraction, data.assetId);
```

This function calls `_withdrawToChain()` with the `unwrap` parameter set to false, indicating that TOFT-wrapped Singularity tokens will not be unwrapped upon receipt on the destination chain.

```solidity
_withdrawToChain(
    MagnetarWithdrawData({
        yieldBox: yieldBox,
        assetId: data.assetId,
        unwrap: false,
        lzSendParams: data.lockAndParticipateSendParams.lzParams,
        sendGas: data.lockAndParticipateSendParams.lzSendGas,
        composeGas: data.lockAndParticipateSendParams.lzComposeGas,
        sendVal: data.lockAndParticipateSendParams.lzSendVal,
        composeVal: data.lockAndParticipateSendParams.lzComposeVal,
        composeMsg: data.lockAndParticipateSendParams.lzParams.sendParam.composeMsg,
        composeMsgType: data.lockAndParticipateSendParams.lzComposeMsgType,
        withdraw: true
    })
);
```

However, the [`TapiocaOptionLiquidityProvision.lock()`](https://github.com/Tapioca-DAO/tap-token/blob/20a83b1d2d5577653610a6c3879dff9df4968345/contracts/options/TapiocaOptionLiquidityProvision.sol#L187) function attempts to acquire YieldBox's shares of the original Singularity tokens. Therefore, upon receiving wrapped Singularity tokens on the destination chain, it should unwrap these tokens to facilitate the execution of subsequent actions.

### Impact

`depositYBLendSGLLockXchainTOLP()` will fail to execute the locking process after receiving wrapped Singularity tokens cross-chain.

### Recommended Mitigation Steps

`depositYBLendSGLLockXchainTOLP()` should call `_withdrawToChain()` with `unwrap` set to true.

### Assessed type

Context

**[cryptotechmaker (Tapioca) confirmed and commented](https://github.com/code-423n4/2024-02-tapioca-findings/issues/180#issuecomment-2031959346):**
 > Fixed [here](https://github.com/Tapioca-DAO/tapioca-periph/pull/204).

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
| Finders | carrotsmuggler, 1, 2, KIntern\_NA, deadrxsezzz |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-tapioca
- **GitHub**: https://github.com/code-423n4/2024-02-tapioca-findings/issues/180
- **Contest**: https://code4rena.com/reports/2024-02-tapioca

### Keywords for Search

`vulnerability`

