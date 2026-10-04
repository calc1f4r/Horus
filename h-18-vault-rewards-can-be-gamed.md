---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3921
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-04-vader
github_link: https://github.com/code-423n4/2021-04-vader-findings/issues/222

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-18]  Vault rewards can be gamed

### Overview


This bug report is about the _deposit_ function in a codebase which can be exploited to inflate a member's weight. This is done by creating a custom token, issuing lots of tokens to the attacker, creating a synth of this token, adding liquidity to the token-base pair, minting some synths, and then depositing the fake synth. The attacker can then call the `harvest(realSynth)` function with a valuable synth to increase their synth balance and withdraw it later. This results in the attacker earning almost all vault rewards, as they are distributed pro rata to the member weight which is independent of the actual synth deposited.

The recommended mitigation steps are to make the rewards based on the actual synths deposited instead of a "global" weight tracker, whitelist certain synths, or don't let anyone create synths.

### Original Finding Content


The `_deposit` function increases the member's _weight_ by `_weight = iUTILS(UTILS()).calcValueInBase(iSYNTH(_synth).TOKEN(), _amount);` which is the swap output amount when trading the deposited underlying synth amount.

Notice that anyone can create synths of custom tokens by calling `Pools.deploySynth(customToken)`.

Therefore an attacker can deposit valueless custom tokens and inflate their member weight as follows:

1. Create a custom token and issue lots of tokens to the attacker
2. Create synth of this token
3. Add liquidity for the `TOKEN <> BASE` pair by providing a single wei of `TOKEN` and `10^18` BASE tokens. This makes the `TOKEN` price very expensive.
4. Mint some synths by paying BASE to the pool
5. Deposit the fake synth, `_weight` will be very high because the token pool price is so high.

Call `harvest(realSynth)` with a synth with actual value. This will increase the synth balance and it can be withdrawn later.

Anyone can inflate their member weight through depositing a custom synth and earn almost all vault rewards by calling `harvest(realSynth)` with a valuable "real" synth.
The rewards are distributed pro rata to the member weight which is independent of the actual synth deposited.

The `calcReward` function completely disregards the `synth` parameter which seems odd.
Recommend thinking about making the rewards based on the actual synths deposited instead of a "global" weight tracker.
Alternatively, whitelist certain synths that count toward the weight, or don't let anyone create synths.

**[strictly-scarce (vader) confirmed](https://github.com/code-423n4/2021-04-vader-findings/issues/222#issuecomment-828453323):**
 > This is a valid attack path.
>
> The counter is two fold:
>
> 1) In the vault, `require(isCurated(token))` this will only allow synths of curated tokens to be deposited for rewards. [The curation logic ](https://github.com/code-423n4/2021-04-vader/blob/main/vader-protocol/contracts/Router.sol#L234) does a check for liquidity depth, so only deep pools can become synths. Thus an attacker would need to deposit a lot of BASE.
>
> 2) In the vaults, use `_weight = iUTILS(UTILS()).calcSwapValueInBase(iSYNTH(_synth).TOKEN(), _amount);`, which computes the weight with respect to slip, so a small manipulated pool cannot be eligible. The pool would need to be deep.
>
> ---
>
> The Vault converts all synths back to common accounting asset - USDV, so member weight can be tracked.
>
**[strictly-scarce (vader) commented](https://github.com/code-423n4/2021-04-vader-findings/issues/222#issuecomment-830635200):**
 > Disagree with severity, since the daily rewards can be claimed by anyone in a fee-bidding war but no actual extra inflation occurs.
>
> Severity: 2



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-vader
- **GitHub**: https://github.com/code-423n4/2021-04-vader-findings/issues/222
- **Contest**: https://code4rena.com/contests/2021-04-vader-protocol-contest

### Keywords for Search

`vulnerability`

