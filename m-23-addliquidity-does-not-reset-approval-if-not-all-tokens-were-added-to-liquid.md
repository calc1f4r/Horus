---
# Core Classification
protocol: Malt Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42388
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-11-malt
source_link: https://code4rena.com/reports/2021-11-malt
github_link: https://github.com/code-423n4/2021-11-malt-findings/issues/228

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
  - dexes
  - cdp
  - yield
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-23] `addLiquidity` Does Not Reset Approval If Not All Tokens Were Added To Liquidity Pool

### Overview


The report discusses a bug in the `addLiquidity` function, which is used when users reinvest their tokens through bonding events. The function is supposed to provide protections against slippage and return any dust token amounts to the caller, which is the `RewardReinvestor` contract. However, the token approval for this outcome is not handled properly, which can lead to large Uniswap approval amounts by the `UniswapHandler` contract over time. The report recommends resetting the approval amount in certain cases to prevent this issue.

### Original Finding Content

_Submitted by leastwood_

`addLiquidity` is called when users reinvest their tokens through bonding events. The `RewardReinvestor` first transfers Malt and rewards tokens before adding liquidity to the token pool. `addLiquidity` provides protections against slippage by a margin of 5%, and any dust token amounts are transferred back to the caller. In this instance, the caller is the `RewardReinvestor` contract which further distributes the dust token amounts to the protocol's treasury. However, the token approval for this outcome is not handled properly. Dust approval amounts can accrue over time, leading to large Uniswap approval amounts by the `UniswapHandler` contract.

#### Proof of Concept

<https://github.com/code-423n4/2021-11-malt/blob/main/src/contracts/DexHandlers/UniswapHandler.sol#L212-L214>
<https://github.com/code-423n4/2021-11-malt/blob/main/src/contracts/DexHandlers/UniswapHandler.sol#L216-L218>

#### Recommended Mitigation Steps

Consider resetting the approval amount if either `maltUsed < maltBalance` or `rewardUsed < rewardBalance` in `addLiquidity`.

**[0xScotch (sponsor) confirmed](https://github.com/code-423n4/2021-11-malt-findings/issues/228)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-11-malt-findings/issues/228#issuecomment-1020718747):**
 > The UniV2Router will first [calculate the amounts](https://github.com/Uniswap/v2-periphery/blob/2efa12e0f2d808d9b49737927f0e416fafa5af68/contracts/UniswapV2Router02.sol#L71) and then [pull them](https://github.com/Uniswap/v2-periphery/blob/2efa12e0f2d808d9b49737927f0e416fafa5af68/contracts/UniswapV2Router02.sol#L73) from the msg.sender
> 
> This means that approvals may not be fully utilized, leaving traces of approvals here and there.
> This can cause issues with certain tokens (USDT comes to mind), and will also not trigger gas refunds.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Malt Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-malt
- **GitHub**: https://github.com/code-423n4/2021-11-malt-findings/issues/228
- **Contest**: https://code4rena.com/reports/2021-11-malt

### Keywords for Search

`vulnerability`

