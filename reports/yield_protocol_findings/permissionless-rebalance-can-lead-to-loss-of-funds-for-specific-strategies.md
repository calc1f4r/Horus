---
# Core Classification
protocol: Euler Earn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41980
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-October-2024.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - M4rio.eth
  - Christoph Michel
---

## Vulnerability Title

Permissionless rebalance can lead to loss of funds for specific strategies

### Overview


The report describes a bug in the code for a financial platform called EulerEarn, which allows users to invest in different strategies to earn money. The bug allows anyone to perform a rebalance action, which moves money from over-allocated strategies to under-allocated ones. However, this can result in losses due to fees if the rebalance is combined with other actions. The bug has been fixed in a code update.

### Original Finding Content

## Severity: Medium Risk

## Context
- EulerEarn.sol#L245-L249
- EulerEarnVault.sol#L754-L764

## Description
The rebalance action is permissionless and can be executed by anyone. It will withdraw from strategies that are over-allocated and deposit into strategies that are under-allocated (according to the allocation points for each strategy). The strategies and the rebalance order can be defined as a parameter to rebalance. 

Note that the value allocated to a vault with a deposit can be less than what is received by withdrawing from the vault again, for example, if the vault takes fees. The differences may be small (like if due to rounding error), or very significant (like if a Vault implements withdrawal or deposit fees, etc). EIP-4626.

Note that the loss due to fees is not immediately booked in the `rebalance()` as the `strategy.allocated` value increased/decreased by the deposited/withdrawn value. It gets booked in a subsequent harvest operation when the value of the shares is computed:

```
strategy.allocated = strategy.previewRedeem(strategy.balanceOf(this))
```

### An attacker can:
1. Rebalance the strategies.
2. Harvest to book the fee loss, decreasing the strategy's `strategy.allocated` and the overall `totalAllocated`, resulting in the allocation percentage `strategy.allocated / totalAllocated` for that vault to drop below its desired share again.
3. Repeat the rebalance.

The rebalance step can be combined with finding a Flash deposit and withdraw, which can be used to off-balance assets to rebalance almost the entire total assets to a specific strategy, increasing the loss for each iteration. 

The impact is that the vault's funds can be lost entirely to fees by continuous rebalancing.

## Recommendation
- All strategies should have the invariant that depositing/withdrawing assets amount should increase/decrease `previewRedeem(strategy.balanceOf(this))` by this same assets amount. Otherwise, rebalance will incur losses.
- Consider restricting the permissionless rebalances that can be performed by implementing a cooldown for permissionless calls (always rebalancing all strategies), whereas a privileged role for rebalance can rebalance at any time. This can lead to delayed withdrawals for users if the cash reserve cannot be rebalanced right now, and rely on keepers/trusted roles to rebalance if the cash reserve is low, but the trust assumption is already that users have to trust privileged roles to correctly allocate their funds to non-malicious vaults.

## Additional Information
- **Euler**: Fixed in PR 105.
- **Spearbit**: Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Euler Earn |
| Report Date | N/A |
| Finders | M4rio.eth, Christoph Michel |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

