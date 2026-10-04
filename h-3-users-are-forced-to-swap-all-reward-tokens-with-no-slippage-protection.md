---
# Core Classification
protocol: Blueberry Update
chain: everychain
category: uncategorized
vulnerability_type: slippage

# Attack Vector Details
attack_type: slippage
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18483
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/69
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/121

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
  - slippage
  - deposit/reward_tokens

protocol_categories:
  - lending
  - leveraged_farming
  - options_vault

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - Bauer
  - 0x52
  - J4de
  - n1punp
  - nobody2018
---

## Vulnerability Title

H-3: Users are forced to swap all reward tokens with no slippage protection

### Overview


This bug report is about an issue found in the AuraSpell.sol contract, which is part of the Sherlock Audit project. The issue is that users are forced to swap all reward tokens with no slippage protection. This was found through manual review by 0x52, Bauer, Breeje, J4de, ctf_sec, n1punp, and nobody2018.

The vulnerability detail is that the code snippet for the swap function does not allow users to specify any slippage values, meaning that deposits can be sandwiched and stolen. This can result in all reward tokens being sandwiched and stolen. The code snippet for the vulnerability can be found in AuraSpell.sol#L193-L203 and the full code snippet can be found in AuraSpell.sol#L149-L224.

The impact of this vulnerability is that all reward tokens can be sandwiched and stolen. The recommendation for this issue is to allow users to specify slippage parameters for all reward tokens.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/121 

## Found by 
0x52, Bauer, Breeje, J4de, ctf\_sec, n1punp, nobody2018
## Summary

AuraSpell forces users to swap their reward tokens to debt token but doesn't allow them to specify any slippage values.

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

Above all reward tokens are swapped and always use 0 for min out meaning that deposits will be sandwiched and stolen.

## Impact

All reward tokens can be sandwiched and stolen

## Code Snippet

[AuraSpell.sol#L149-L224](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/AuraSpell.sol#L149-L224)

## Tool used

Manual Review

## Recommendation

Allow user to specify slippage parameters for all reward tokens

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update |
| Report Date | N/A |
| Finders | Bauer, 0x52, J4de, n1punp, nobody2018, Breeje, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/121
- **Contest**: https://app.sherlock.xyz/audits/contests/69

### Keywords for Search

`Slippage, Deposit/Reward tokens`

