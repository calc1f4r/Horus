---
# Core Classification
protocol: Blueberry Update #3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24326
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/104
source_link: none
github_link: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/103

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
  - rwa
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

M-6: AuraSpell#closePositionFarm will take reward fees on underlying tokens when borrow token is also a reward

### Overview


This bug report is about an issue that was found in the AuraSpell#closePositionFarm code. It was found that when the borrow token is also a reward, the BLP is burned before taking the reward cut. This causes the user to lose funds due to incorrect fees. The code snippet that is causing the issue can be found at AuraSpell.sol#L184-L265. The tool used to find this bug was manual review. The recommendation for this issue is to use the same order as ConvexSpell and sell rewards BEFORE burning BLP. This will ensure that the user does not lose funds due to incorrect fees being taken.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/103 

## Found by 
0x52

AuraSpell#AuraSpell#closePositionFarm will take reward fees on underlying tokens when borrow token is also a reward. This is because the BLP is burned before taking the reward cut.

## Vulnerability Detail

[AuraSpell.sol#L227-L247](https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/spell/AuraSpell.sol#L227-L247)

                wAuraPools.getVault(lpToken).exitPool(
                    IBalancerPool(lpToken).getPoolId(),
                    address(this),
                    address(this),
                    IBalancerVault.ExitPoolRequest(
                        tokens,
                        minAmountsOut,
                        abi.encode(0, amountPosRemove, borrowTokenIndex),
                        false
                    )
                );
            }
        }

        /// 4. Swap each reward token for the debt token
        uint256 rewardTokensLength = rewardTokens.length;
        for (uint256 i; i != rewardTokensLength; ) {
            address sellToken = rewardTokens[i];
            if (sellToken == STASH_AURA) sellToken = AURA;

            _doCutRewardsFee(sellToken);

We can see above that closePositionFarm redeems the BLP before it takes the reward cut. This can cause serious issues. If there is any overlap between the reward tokens and the borrow token then _doCutRewardsFee will take a cut of the underlying liquidity. This causes loss to the user as too many fees are taken from them.

## Impact

User will lose funds due to incorrect fees

## Code Snippet

[AuraSpell.sol#L184-L265](https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/spell/AuraSpell.sol#L184-L265)

## Tool used

Manual Review

## Recommendation

Use the same order as ConvexSpell and sell rewards BEFORE burning BLP

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update #3 |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/103
- **Contest**: https://app.sherlock.xyz/audits/contests/104

### Keywords for Search

`vulnerability`

