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
solodit_id: 24325
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/104
source_link: none
github_link: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/102

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
finders_count: 6
finders:
  - 0x52
  - bitsurfer
  - Vagner
  - nobody2018
  - Breeje
---

## Vulnerability Title

M-5: AuraSpell#closePositionFarm exits pool with single token and without any slippage protection

### Overview


A bug report has been filed against the code in the AuraSpell.sol contract, which is part of the Sherlock Audit 2023-07-blueberry-judging repository. The bug is that when exiting the balancer pool, vault#exitPool is called with an empty array for minAmountsOut, causing the position to be exited with no slippage protection. This can cause massive loss when exiting to a single token. The code snippet responsible for this is [AuraSpell.sol#L221-L236](https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/spell/AuraSpell.sol#L221-L236) and [AuraSpell.sol#L358-L361](https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/spell/AuraSpell.sol#L358-L361).

The impact of the bug is that exits can be sandwich attacked, causing massive loss to the user. The bug was found by 0x52, Breeje, Oxhunter526, Vagner, bitsurfer, and nobody2018. The tool used to identify the bug was manual review.

The recommendation to fix the bug is to allow the user to specify the minimum amount received from the exit. After discussion, the bug was classified as a medium severity issue with duplicates. The lead Watson's comment can be found [here](https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/102#issuecomment-1699649100).

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/102 

## Found by 
0x52, Breeje, Oxhunter526, Vagner, bitsurfer, nobody2018

When exiting the balancer pool, vault#exitPool is called with an empty array for minAmountsOut causing the position to be exited with no slippage protection. Typically it is not an issue to exit off axis but since it is exiting to a single token this can cause massive loss.

## Vulnerability Detail

[AuraSpell.sol#L221-L236](https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/spell/AuraSpell.sol#L221-L236)

                (
                    uint256[] memory minAmountsOut,
                    address[] memory tokens,
                    uint256 borrowTokenIndex
                ) = _getExitPoolParams(param.borrowToken, lpToken);

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

When exiting a the balancer vault, closePositionFarm makes a subcall to _getExitPoolParams which is used to set minAmountsOut.

[AuraSpell.sol#L358-L361](https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/spell/AuraSpell.sol#L358-L361)

        (address[] memory tokens, , ) = wAuraPools.getPoolTokens(lpToken);

        uint256 length = tokens.length;
        uint256[] memory minAmountsOut = new uint256[](length);

Inside _getExitPoolParams we see that minAmountsOut are always an empty array. This means that the user has no slippage protection and can be sandwich attacked, suffering massive losses.

## Impact

Exits can be sandwich attacked causing massive loss to the user

## Code Snippet

[AuraSpell.sol#L184-L286](https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/spell/AuraSpell.sol#L184-L286)

## Tool used

Manual Review

## Recommendation

Allow user to specify min amount received from exit



## Discussion

**securitygrid**

Escalate:
Historically, lacking slippage protection is H.


**sherlock-admin2**

 > Escalate:
> Historically, lacking slippage protection is H.
> 

You've created a valid escalation!

To remove the escalation from consideration: Delete your comment.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**Shogoki**

> Escalate: Historically, lacking slippage protection is H.

Can be a high issue

**IAm0x52**

Why would lack of slippage be considered high in this scenario? Even with zero slippage protection sandwich attack profitability is always contingent on a few external factors such as: liquidity of underlying pool, the fee of the underlying pool, the amount being swapped and the current gas prices. The higher the liquidity and fee of the pool the higher the cost to push the pool price then pull it back. The lower the amount being swapped, the less the attacker can steal. If this cost exceeds the gain from the attack then the attack isn't profitable and won't happen.

**VagnerAndrei26**

I think no slippage is considered high most of the time cause sandwich attacks are easily doable in the space, especially for those experienced in doing it, and even if there are factors to consider even one successful can occur loss of funds for the protocol in a pretty easy manner. So considering that and also past contests I think it should be considered also a high.

**Nabeel-javaid**

as far as I know 98% of the times slippage issues are considered as Medium severity

**hrishibhat**

Result:
Medium
Has duplicates 
This is a valid medium issue. Agree with the Lead Watson's comments here:
https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/102#issuecomment-1699649100


**sherlock-admin2**

Escalations have been resolved successfully!

Escalation status:
- [securitygrid](https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/102/#issuecomment-1693593255): rejected

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update #3 |
| Report Date | N/A |
| Finders | 0x52, bitsurfer, Vagner, nobody2018, Breeje, Oxhunter526 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/102
- **Contest**: https://app.sherlock.xyz/audits/contests/104

### Keywords for Search

`vulnerability`

