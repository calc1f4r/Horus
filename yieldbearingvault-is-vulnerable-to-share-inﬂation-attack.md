---
# Core Classification
protocol: Usual
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46654
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/98727af1-95b1-4446-b39f-465d8ac83f01
source_link: https://cdn.cantina.xyz/reports/cantina_usual_phase2_october2024.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Chinmay Farkya
  - deadrosesxyz
  - phaze
---

## Vulnerability Title

YieldBearingVault is vulnerable to share inﬂation attack 

### Overview

See description below for full details.

### Original Finding Content

## YieldBearingVault Vulnerability

## Context
`YieldBearingVault.sol#L13`

## Description
The `YieldBearingVault` accrues yield every second. If the yield mode is on when the vault is deployed, a user could weaponize it to perform the popular share inflation attack.

## Attack Path
1. Attacker makes the first deposit (let's say for `1e18`).
2. As soon as even `1 wei` of yield is accrued, the user could withdraw all but `1 share`. Due to rounding down, the remaining assets in the vault will be `2 wei`, or the rate will be increased to `2:1`.
3. Then the user can perform a deposit for `1 wei`, which would round down to `0 shares` and would increase the rate to `3:1`.
4. By repeating the previous step, the user can indefinitely inflate the share value.
5. The user continues until the share value becomes large enough that the next innocent user's deposit rounds down to `0 shares`. This would effectively be the same as a donation to the attacker.

Given that the initially accrued yield will be much more than just `1 wei`, the attack would require a really low number of loops to execute.

## Note
The Usual team is aware of this issue and is taking necessary precautions (such as being the first minter and not turning on the vault shares for some time), making this issue unlikely to occur.

## Recommendation
Do not activate the yield mode before a reasonable number of users are already in the vault.

## Usual
This attack is not possible in reality for several reasons:
1. We will be the first depositor into the vault to provide dead shares for the vault; there is no scenario in which users can do this prior to us.
2. No one has Usual to stake into the UsualX vault at the outset: Usual is not immediately distributed to users at the Token Generation Event (TGE) as rewards are set to begin in the following week.
3. There is no scenario where "the yield mode is on when the vault is deployed": we control when the distribution module begins a new yield/reward period.
4. Once users receive Usual to stake (after a 7-day challenge period), they will also have time to stake into the vault before we begin to trigger the first yield period, avoiding the opportunity for a first depositor to easily manipulate the shares to asset ratio.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Usual |
| Report Date | N/A |
| Finders | Chinmay Farkya, deadrosesxyz, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_usual_phase2_october2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/98727af1-95b1-4446-b39f-465d8ac83f01

### Keywords for Search

`vulnerability`

