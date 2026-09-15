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
solodit_id: 32350
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-tapioca
source_link: https://code4rena.com/reports/2024-02-tapioca
github_link: https://github.com/code-423n4/2024-02-tapioca-findings/issues/62

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
finders_count: 2
finders:
  - rvierdiiev
  - KIntern\_NA
---

## Vulnerability Title

[M-27] Cross chain messages in `MagnetarAssetXChainModule` and `MagnetarMintXChainModule` will not work

### Overview


The report highlights an issue with the `MagnetarBaseModule._withdrawToChain` function, which is used to send LZ messages. The function only includes a composed message if `data.unwrap` is set to true. If it is set to false, the `_lzWithdraw` function is called, which does not include a composed message. This can cause problems with cross-chain functionality, specifically with the `MagnetarMintXChainModule.mintBBLendXChainSGL` and `MagnetarAssetXChainModule.depositYBLendSGLLockXchainTOLP` functions, as they both pass `data.unwrap` as false. The recommended solution is to pass `data.unwrap` as true to ensure the composed message is included. This bug has been confirmed and a pull request has been made to address it. 

### Original Finding Content


In order to send LZ message `MagnetarBaseModule._withdrawToChain` function is called. This function allows to include composed message only [if `data.unwrap` is set to true](https://github.com/Tapioca-DAO/tapioca-periph/blob/032396f701be935b04a7e5cf3cb40a0136259dbc/contracts/Magnetar/modules/MagnetarBaseModule.sol#L71-L81). In this case `_lzCustomWithdraw` function will be used, which [will include composed message](https://github.com/Tapioca-DAO/tapioca-periph/blob/032396f701be935b04a7e5cf3cb40a0136259dbc/contracts/Magnetar/modules/MagnetarBaseModule.sol#L155).

In case if `!data.unwrap`, then `_lzWithdraw` function is called, which [calls `_prepareLzSend` function](https://github.com/Tapioca-DAO/tapioca-periph/blob/032396f701be935b04a7e5cf3cb40a0136259dbc/contracts/Magnetar/modules/MagnetarBaseModule.sol#L120), which includes empty composed message. If you want to include composed message, then you should set `data.unwrap` as true.

Now, let's look into `MagnetarMintXChainModule.mintBBLendXChainSGL` function, which [passes false](https://github.com/Tapioca-DAO/tapioca-periph/blob/032396f701be935b04a7e5cf3cb40a0136259dbc/contracts/Magnetar/modules/MagnetarMintXChainModule.sol#L86). Then look into `MagnetarAssetXChainModule.depositYBLendSGLLockXchainTOLP` function, which [passes false](https://github.com/Tapioca-DAO/tapioca-periph/blob/032396f701be935b04a7e5cf3cb40a0136259dbc/contracts/Magnetar/modules/MagnetarAssetXChainModule.sol#L104).

As both of them pass `data.unwrap` as false, it means that compose message will not be crafted and this cross chain functionality will not work.

### Impact

It will be not possible to min `usdo` on one chain and lend it to singularity on another chain.

### Tools Used

VsCode

### Recommended Mitigation Steps

Pass ``data.unwrap` as true.

### Assessed type

Error

**[cryptotechmaker (Tapioca) confirmed and commented](https://github.com/code-423n4/2024-02-tapioca-findings/issues/62#issuecomment-2058663107):**
 > PR [here](https://github.com/Tapioca-DAO/tapioca-periph/pull/234/commits/e08f90070e35d7b08331909e1fcde279fe1ebc10).
> 

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
| Finders | rvierdiiev, KIntern\_NA |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-tapioca
- **GitHub**: https://github.com/code-423n4/2024-02-tapioca-findings/issues/62
- **Contest**: https://code4rena.com/reports/2024-02-tapioca

### Keywords for Search

`vulnerability`

