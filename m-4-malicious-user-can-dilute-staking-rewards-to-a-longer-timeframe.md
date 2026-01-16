---
# Core Classification
protocol: Symmio, Staking and Vesting
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55108
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/838
source_link: none
github_link: https://github.com/sherlock-audit/2025-03-symm-io-stacking-judging/issues/595

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
finders_count: 100
finders:
  - newspacexyz
  - Artur
  - X0sauce
  - korok
  - brgltd
---

## Vulnerability Title

M-4: Malicious User can dilute staking Rewards to a longer timeframe

### Overview


The SymmStaking contract has a vulnerability that allows a malicious user to delay staking rewards by continuously adding small amounts of rewards while existing rewards are still active. This can be exploited by repeatedly calling the notifyRewardAmount function with tiny amounts, causing the reward rate to drop significantly over time. This can prevent stakers from receiving their full rewards in a timely manner. To mitigate this, restrictions can be added on who can add new rewards or a minimum amount of reward tokens can be implemented to ensure a meaningful increase in the total reward amount. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-03-symm-io-stacking-judging/issues/595 

## Found by 
0day, 0xAristos, 0xBecket, 0xDarko, 0xc0ffEE, 0xhammadghazi, 0xkmg, 0xlucky, 0xmechanic, 0xpiken, Abhan1041, Akhuemokhan.ETH, Anirruth, Arav, Artur, Audinarey, BAdal-Sharma-09, Boy2000, Breeje, BusinessShotgun, DenTonylifer, DharkArtz, Drynooo, Edoscoba, ElmInNyc99, EmanHerawy, Flare, Fortis\_Audits, Frontrunner, HaidutiSec, KlosMitSoss, LSH.F.GJ, Limbooo, LonWof-Demon, MSK, Matin, MysteryAuditor, OpaBatyo, Opeyemi, Pablo, Pelz, Pro\_King, Ryonen, SUPERMAN\_I4G, SarveshLimaye, Silvermist, SlayerSecurity, Waydou, X0sauce, X12, Yaneca\_b, ZoA, arman, aslanbek, aswinraj94, auditism, auditmasterchef, brgltd, buggsy, copperscrewer, dimah7, dobrevaleri, durov, eta, farismaulana, future2\_22, ggbond, gkrastenov, hildingr, ihtishamsudo, ilyadruzh, jo13, komane007, korok, krot-0025, moray5554, newspacexyz, novaman33, omega, onthehunt, osuolale, oxwhite, phoenixv110, redbeans, redtrama, roccomania, santiellena, shui, silver\_eth, spdream, stuart\_the\_minion, t.aksoy, t0x1c, turvec, udo, vladi319, x0lohaclohell, y4y, yaioxy, ydlee

### Summary

The `SymmStaking` contract allows anyone to add new rewards using the `notifyRewardAmount` function. However, if new rewards are continuously added while existing rewards are still active, the total rewards get spread over a longer period. A malicious actor can exploit this by repeatedly adding tiny amounts, effectively delaying stakers from receiving their full rewards.



### Root Cause

* `notifyRewardAmount` function can be called by anyone, with any reward amount.

* Each time it's called, the reward rate is recalculated as:

    * `amount / state.duration` (if the previous reward period has ended).
    * [`(amount + leftover) / state.duration`](https://github.com/sherlock-audit/2025-03-symm-io-stacking/blob/main/token/contracts/staking/SymmStaking.sol#L374) (if the previous reward period is still ongoing).

The issue arises when an attacker keeps adding tiny amounts (e.g., 1 wei) repeatedly. While the total rewards (amount + leftover) barely change, the duration (state.duration) remains fixed at 1 week, causing the reward rate to drop significantly over time.

**Example:**

1. Alice is the only staker, and 100 USDC is added as a reward.

2. Halfway through, Alice has earned 50 USDC.

3. A malicious user then adds just 1 wei USDC as a new reward.

4. This recalculates the reward rate, cutting it in half:

    * From `100e6 / 1 week` → `50e6 / 1 week`.

5. The attacker can repeat this process multiple times, continuously lowering the rate.

This DoS-like attack prevents stakers from claiming their rewards in a reasonable timeframe.

### Internal Pre-conditions

None.

### External Pre-conditions

None.

### Attack Path

1. Users stakes in `SymmStaking`.

2. A new reward is notified via `notifyRewardAmount` for the stakers.

3. A malicious user calls `notifyRewardAmount` multiple times with dust values to dilute the reward rate.

4. User get rewards slower than what they were supposed to get.

### Impact

Time to gain the intended reward can be arbitrarily increased by malicious users.

### PoC

_No response_

### Mitigation

Consider adding restrictions on who can add new reward. Alternatively, implement a minimum amount of reward tokens that can be added to ensure that the total reward amount is meaningfully increased.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Symmio, Staking and Vesting |
| Report Date | N/A |
| Finders | newspacexyz, Artur, X0sauce, korok, brgltd, DharkArtz, udo, redbeans, future2\_22, oxwhite, vladi319, ydlee, aslanbek, Boy2000, LonWof-Demon, arman, KlosMitSoss, x0lohaclohell, SUPERMAN\_I4G, dobrevaleri, moray5554, Pablo, durov, turvec, gkrastenov, krot-0025, Opeyemi, dimah7, auditism, 0xc0ffEE, shui, DenTonylifer, silver\_eth, Ryonen, Audinarey, eta, Waydou, ggbond, Pelz, hildingr, 0xlucky, copperscrewer, t0x1c, Arav, novaman33, phoenixv110, Silvermist, jo13, MSK, Matin, roccomania, Anirruth, y4y, 0xkmg, santiellena, komane007, aswinraj94, MysteryAuditor, ilyadruzh, Limbooo, ZoA, 0xDarko, ihtishamsudo, X12, EmanHerawy, BusinessShotgun, SarveshLimaye, SlayerSecurity, Breeje, OpaBatyo, redtrama, farismaulana, Drynooo, Edoscoba, 0xAristos, Flare, stuart\_the\_minion, Pro\_King, 0xpiken, yaioxy, Abhan1041, ElmInNyc99, BAdal-Sharma-09, LSH.F.GJ, t.aksoy, onthehunt, osuolale, HaidutiSec, omega, Yaneca\_b, spdream, 0xhammadghazi, buggsy, Fortis\_Audits, 0xmechanic, Frontrunner, 0xBecket, Akhuemokhan.ETH, auditmasterchef, 0day |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-03-symm-io-stacking-judging/issues/595
- **Contest**: https://app.sherlock.xyz/audits/contests/838

### Keywords for Search

`vulnerability`

