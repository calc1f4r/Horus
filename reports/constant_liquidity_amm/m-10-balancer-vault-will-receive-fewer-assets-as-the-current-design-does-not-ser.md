---
# Core Classification
protocol: Notional
chain: everychain
category: uncategorized
vulnerability_type: liquidity_provider_racing

# Attack Vector Details
attack_type: liquidity_provider_racing
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3335
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/2
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-notional-judging/issues/76

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - liquidity_provider_racing

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - xiaoming90
---

## Vulnerability Title

M-10: Balancer Vault Will Receive Fewer Assets As The Current Design Does Not Serve The Interest Of Vault Shareholders

### Overview


This bug report is about the current implementation of reinvesting reward function in Balancer Vaults (MetaStable2TokenAuraVault and Boosted3TokenAuraVault) which does not benefit the vault shareholders. The function is permissionless and can be called by anyone, allowing them to specify the trading configuration such as the DEX (e.g. Uniswap, Curve) that the trade should be executed and the slippage (`params.tradeParams.oracleSlippagePercent`). As a result, the liquidity provider of the supported DEX protocols will want the trade to be executed on the DEX pool that they invested on, allowing them to earn an additional transaction fee from the trade. This misalignment in the objective between the vault shareholders and callers will end up having the vault and its users on the losing end and receive fewer assets than they should.

It is recommended to implement access control on the `reinvestReward` function to ensure that this function can only be triggered by Notional who has the best interest of its vault users. Also, consider sending the `reinvestReward` transaction as a private transaction via Flashbot so that the attacker cannot perform any kind of sandwich attack on the reinvest rewards transaction.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-notional-judging/issues/76 

## Found by 
xiaoming90

## Summary

The current implementation of reinvesting reward function does not benefit the vault shareholders as the current design does not serve the vault shareholder's interest well. Thus, this will result in Balancer vaults receiving fewer assets.

## Vulnerability Detail

The `reinvestReward` function of the Balancer Vaults (MetaStable2TokenAuraVault and Boosted3TokenAuraVault) is permissionless and can be called by anyone. By calling `reinvestReward` function, the vault will trade the reward tokens received by the vault for tokens that are accepted by the balancer pool, and deposit them to the pool to obtain more BPT tokens for the vault shareholders. By continuously reinvesting the reward tokens into the pool, the vault shareholders will be able to lay claim to more BPT tokens per share over time.

https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/vaults/balancer/external/MetaStable2TokenAuraHelper.sol#L114

```solidity
File: MetaStable2TokenAuraHelper.sol
114:     function reinvestReward(
115:         MetaStable2TokenAuraStrategyContext calldata context,
116:         ReinvestRewardParams calldata params
117:     ) external {
```

https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/vaults/balancer/external/Boosted3TokenAuraHelper.sol#L115


```solidity
File: Boosted3TokenAuraHelper.sol
115:     function reinvestReward(
116:         Boosted3TokenAuraStrategyContext calldata context,
117:         ReinvestRewardParams calldata params
118:     ) external {        
```

The caller of the `reinvestReward` function can specify the trading configuration such as the DEX (e.g. Uniswap, Curve) that the trade should be executed and the slippage (`params.tradeParams.oracleSlippagePercent`). Note that the slippage defined must be equal to or less than the ` strategyContext.vaultSettings.maxRewardTradeSlippageLimitPercent` setting that is currently set to 5% within the test scripts.

Notional Vaults support trading in multiple DEX protocols (Curve, Balancer V2, Uniswap V2 & V3 and 0x). Since `reinvestReward` function is callable by anyone, the liquidity provider of the supported DEX protocols will want the trade to be executed on the DEX pool that they invested on. This will allow them to earn an additional transaction fee from the trade. The amount of transaction fee earned will be significant if the volume is large when there are many vaults and reward tokens to be reinvested. In addition, the caller will set the slippage to the maximum configurable threshold (e.g. 5% in this example) to maximize the profit. Therefore, this will end up having various liquidity providers front-running each other to ensure that their `reinvestReward` transaction gets executed in order to extract value.

## Impact

This does not serve the vault shareholder's interest well as the caller of the `reinvestReward` function will not be trading and reinvesting in an optimal way that maximizes the value of the shareholder's assets in the vaults. There is a misalignment in the objective between the vault shareholders and callers. Therefore, the vault and its users will end up on the losing end and receive fewer assets than they should.

## Code Snippet

https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/vaults/balancer/external/MetaStable2TokenAuraHelper.sol#L114
https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/vaults/balancer/external/Boosted3TokenAuraHelper.sol#L115


## Tool used

Manual Review

## Recommendation

It is recommended to implement access control on the `reinvestReward` function to ensure that this function can only be triggered by Notional who has the best interest of its vault users.

Also, consider sending the `reinvestReward` transaction as a private transaction via Flashbot so that the attacker cannot perform any kind of sandwich attack on the reinvest rewards transaction.

## Discussion

**jeffywu**

There is some balance between centralization and decentralization here, but the auditor does bring up some valid points that we can consider.

If re-invest rewards is called at a predictable cadence the amount of fees generated by trading will likely not be significant enough to generate profits for MEV.

**T-Woodward**

Yeah I think this is a legitimate issue. We are permissioning reward reinvestment.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Notional |
| Report Date | N/A |
| Finders | xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-notional-judging/issues/76
- **Contest**: https://app.sherlock.xyz/audits/contests/2

### Keywords for Search

`Liquidity Provider Racing`

