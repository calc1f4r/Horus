---
# Core Classification
protocol: Coinflip_2025-02-19
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55509
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-19.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-06] Zero share minting via token balance inflation

### Overview


This bug report discusses a high severity issue in the `Staking.finalizeStake()` function. The function uses integer division which can lead to rounding down to zero if there are large token balances. This can be exploited by an attacker through an inflation attack, where they can donate a small amount of tokens and then finalize their stake before a legitimate user, resulting in the legitimate user receiving zero shares. The report suggests implementing a minimum staking amount requirement and applying virtual shares to mitigate this issue. 

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

In `Staking.finalizeStake()`, when calculating shares for non-initial deposits (`@1>`), the function uses integer division, which can round down to zero if there are large token balances.

```solidity
function finalizeStake(address token) external nonReentrant {
    --- SNIPPED ---
    // Retrieve the pool's current balance and total shares
    uint256 totalBalance = IERC20(token).balanceOf(address(this));
    uint256 currentShares = tokenInfo[token].totalShares;

    // Use standard share-mint formula: deposit * totalShares / totalBalance
    uint256 mintedShares;
    if (currentShares == 0 || totalBalance == 0) {
        // If no one has staked yet (or balance was 0), do a 1:1 mint
        mintedShares = depositAmount;
    } else {
        // Standard: deposit's fraction of the pool => minted shares
@1>      mintedShares = (depositAmount * currentShares) / totalBalance;
    }

    --- SNIPPED ---
    emit Staked(msg.sender, token, depositAmount);
}
```

This enables a inflation attack for every accepted token where an attacker can:

1. Backrun the `addAcceptedToken()` to be the first one to request a stake for that token with a small amount, i.e. `1 wei`.
2. As the first request staker, the upcoming stakers will consequencely be able to finalize after them and after passing the cooldown periods, the attacker can wait for the right timing to finalize for the attack.
3. Alice requests the stake with `N` tokens and waits for the timing to finalize.
4. Alice sends the tx to finalize the stake, and the attacker frontruns to finalize their 1 wei stake and donates at least `N+1` amount.
5. When Alice's tx is executed, Alice receives 0 shares as the calculation rounds down from the inflated token balance, and the attacker gets that portion of Alice's stake.

This attack is repeatable for newly accepted tokens or when the staking pool of a specific token has low liquidity.

## Recommendation

The possible approaches to mitigate this issue is the following:

- Initial deposit for each staking pool (so that the first depositor attack is not possible), leaving it as dead shares. This should consider the case for the current logic of removal the accepted token restriction.
- Apply virtual shares in the share calculation.

Moreover, applying a minimum staking amount requirement can also make it more difficult to launch the attack.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Coinflip_2025-02-19 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-19.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

