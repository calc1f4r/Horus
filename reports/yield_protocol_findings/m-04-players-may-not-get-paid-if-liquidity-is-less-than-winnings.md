---
# Core Classification
protocol: Coinflip_2025-02-05
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55490
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-05.md
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

[M-04] Players may not get paid if liquidity is less than winnings

### Overview


The `flip()` function in the staking contract checks for available liquidity before paying out potential winnings. However, if a large amount of funds is withdrawn from the contract at the same time as a `flip()` call, the player may not be able to withdraw their winnings due to insufficient liquidity. To prevent this, the staking contract should account for the amount of locked liquidity and prevent users from unstaking if the total balance falls below this amount.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

When `flip()` is called, the function checks whether there is available liquidity to pay the potential winnings of a game:

```
        // require staked amount > maximum payout using calculatePayout
        (uint256 grossPayout, uint256 netPayout,) = calculatePayout(betAmount, numberOfCoins, headsRequired); // TODO check use grossPayout?

        uint256 stakingBalance = IERC20(token).balanceOf(address(stakingContract));
        uint256 availableLiquidity = (stakingBalance * maxLiquidityPercentage) / 10000;
        require(lockedLiquidity + netPayout <= availableLiquidity, "Not enough liquidity for new bet");

        lockedLiquidity += netPayout;
```

For example, when tested in remix, a 20 coin 20 heads game for 1 USD will yield a payout of 1048575.98 (1 million) USDC. The function checks that there is `availableLiquidity` and then checks the total `lockedLiquidity` and ensures that the staking contract can pay out that amount.

Assume a whale deposits 1.1 million USDC in the staking contract. 2 days later (the unstake cooldown duration), a player calls `flip(1e6,20,20,USDC)`. The `flip()` call is executed, and the player awaits the pyth entropy callback.

Unfortunately, the whale decides to withdraw at this exact moment, and the entropy callbacks after the withdraw. The player actually won the game yielding him 1 million+ USDC, but he cannot withdraw it since there is not enough liquidity in the staking contract anymore.

## Recommendations

The staking contract should account for the `lockedLiquidity`. When a user intends to unstake. If the total balance of the staking contract falls below `lockedLiquidity`, then the user should not be able to unstake as well.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Coinflip_2025-02-05 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-05.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

