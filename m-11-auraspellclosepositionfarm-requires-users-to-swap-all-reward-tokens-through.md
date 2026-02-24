---
# Core Classification
protocol: Blueberry Update
chain: everychain
category: uncategorized
vulnerability_type: uniswap

# Attack Vector Details
attack_type: uniswap
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18505
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/69
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/122

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
  - uniswap
  - swap
  - configuration

protocol_categories:
  - lending
  - leveraged_farming
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

M-11: AuraSpell#closePositionFarm requires users to swap all reward tokens through same router

### Overview


A bug was found in the AuraSpell#closePositionFarm function of the Sherlock-Audit/2023-04-blueberry-judging repository by 0x52. This bug requires users to swap all reward tokens through the same UniswapV2 router, resulting in users experiencing forced losses to their reward token due to lack of liquidity. The code snippet responsible for this issue is located in AuraSpell.sol#L193-L203. The impact of this bug is that users are forced to swap through a router even if it doesn't have good liquidity for all tokens. The bug was found through manual review. The recommendation is to allow users to use an aggregator like paraswap or multiple routers instead of only one single UniswapV2 router.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/122 

## Found by 
0x52
## Summary

AuraSpell#closePositionFarm requires users to swap all reward tokens through same router. This is problematic as it is very unlikely that a UniswapV2 router will have good liquidity sources for all tokens and will result in users experiencing forced losses to their reward token.  

## Vulnerability Detail

[AuraSpell.sol#L193-L203
](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/AuraSpell.sol#L193-L203)

        for (uint256 i = 0; i < rewardTokens.length; i++) {
            uint256 rewards = _doCutRewardsFee(rewardTokens[i]);
            _ensureApprove(rewardTokens[i], address(swapRouter), rewards);
            swapRouter.swapExactTokensForTokens(
                rewards,
                0,
                swapPath[i],
                address(this),
                type(uint256).max
            );
        }

All tokens are forcibly swapped through a single router.

## Impact

Users will be forced to swap through a router even if it doesn't have good liquidity for all tokens

## Code Snippet

[AuraSpell.sol#L149-L224](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/AuraSpell.sol#L149-L224)

## Tool used

Manual Review

## Recommendation

Allow users to use an aggregator like paraswap or multiple routers instead of only one single UniswapV2 router.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/122
- **Contest**: https://app.sherlock.xyz/audits/contests/69

### Keywords for Search

`Uniswap, Swap, Configuration`

