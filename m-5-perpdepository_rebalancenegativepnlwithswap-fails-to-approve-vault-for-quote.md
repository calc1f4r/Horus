---
# Core Classification
protocol: UXD Protocol
chain: everychain
category: uncategorized
vulnerability_type: allowance

# Attack Vector Details
attack_type: allowance
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6263
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/33
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/372

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - allowance

protocol_categories:
  - liquid_staking
  - services
  - derivatives
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - 0x52
  - Bahurum
  - yixxas
  - HonorLt
  - rvierdiiev
---

## Vulnerability Title

M-5: PerpDepository#_rebalanceNegativePnlWithSwap fails to approve vault for quote deposit

### Overview


This bug report is about an issue with PerpDepository#_rebalanceNegativePnlWithSwap failing to approve vault for quote deposit. It was found by HonorLt, 0x52, yixxas, Bahurum, rvierdiiev, and GimelSec. The problem is that the contract grants approval to the vault before depositing either quote or asset, but in this case, there is no approval which means that the deposit call will fail causing PerpDepository#_rebalanceNegativePnlWithSwap to always revert. The impact of this issue is that PerpDepository#_rebalanceNegativePnlWithSwap won't function. The code snippet can be found at https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L478-L528. The tool used to find the issue was manual review. The recommended solution is to add the missing approve call. Lastly, it was pointed out that this is a separate issue from #339.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/372 

## Found by 
HonorLt, 0x52, yixxas, Bahurum, rvierdiiev, GimelSec

## Summary

Throughout the entirety of the contract it grants approval to the vault before depositing either quote or asset. In this case there is no approval which means that the deposit call will fail causing PerpDepository#_rebalanceNegativePnlWithSwap to always revert.

## Vulnerability Detail

See summary.

## Impact

PerpDepository#_rebalanceNegativePnlWithSwap won't function

## Code Snippet

https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L478-L528

## Tool used

Manual Review

## Recommendation

Add the missing approve call:

        } else if (shortFall < 0) {
            // we got excess tokens in the spot swap. Send them to the account paying for rebalance
            IERC20(quoteToken).transfer(
                account,
                _abs(shortFall)
            );
        }

    +   IERC20(quoteToken).approve(address(vault), quoteAmount); 
        vault.deposit(quoteToken, quoteAmount);

        emit Rebalanced(baseAmount, quoteAmount, shortFall);
        return (baseAmount, quoteAmount);

## Discussion

**WarTech9**

This is a duplicate of #339 

**0x00052**

Two separate issues here. #339 is pointing out it's not approved for the swapper. This one is pointing out it's not approved for the vault. It should be approved for both

**WarTech9**

@0x00052 good catch. You're right. This is a separate issue from #339

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | UXD Protocol |
| Report Date | N/A |
| Finders | 0x52, Bahurum, yixxas, HonorLt, rvierdiiev, GimelSec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/372
- **Contest**: https://app.sherlock.xyz/audits/contests/33

### Keywords for Search

`Allowance`

