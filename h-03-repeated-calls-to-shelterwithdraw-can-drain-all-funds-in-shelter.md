---
# Core Classification
protocol: Concur Finance
chain: everychain
category: reentrancy
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1402
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-concur-finance-contest
source_link: https://code4rena.com/reports/2022-02-concur
github_link: https://github.com/code-423n4/2022-02-concur-findings/issues/246

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - wrong_math
  - reentrancy
  - business_logic

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 19
finders:
  - Czar102
  - mtz
  - Ryyy
  - danb
  - cmichel
---

## Vulnerability Title

[H-03] Repeated Calls to Shelter.withdraw Can Drain All Funds in Shelter

### Overview


A bug was discovered in the shelter contract code that allows users to withdraw tokens from the shelter without properly checking if they have already withdrawn them. This means that a user that can call the `withdraw` function can call it repeatedly to steal the funds of other users.

To demonstrate this, an example was given where Mallory deposits 1 wETH into the ConvexStakingWrapper contract. Then, the owner of ConvexStakingWrapper calls setShelter and enterShelter to activate the shelter for wETH, which now has 3 wETH. Mallory calls withdraw once, rightfully receiving 1 wETH, and then calls it again, receiving 2/3 wETH, which does not belong to her.

The recommended mitigation steps are to add a line to the beginning of the `withdraw` function to check that the sender has not already withdrawn the token, and then replace line 55 with a line that records that the sender has withdrawn the token.

### Original Finding Content

_Submitted by mtz, also found by 0x1f8b, 0xliumin, bitbopper, cccz, cmichel, csanuragjain, Czar102, danb, Alex the Entreprenerd, GeekyLumberjack, gzeon, hickuphh3, hyh, leastwood, Randyyy, Rhynorater, Ruhum, and ShadowyNoobDev_

[Shelter.sol#L52-L57](https://github.com/code-423n4/2022-02-concur/blob/main/contracts/Shelter.sol#L52-L57)<br>

tl;dr Anyone who can call `withdraw` to withdraw their own funds can call it repeatedly to withdraw the funds of others. `withdraw` should only succeed if the user hasn't withdrawn the token already.

The shelter can be used for users to withdraw funds in the event of an emergency. The `withdraw` function allows callers to withdraw tokens based on the tokens they have deposited into the shelter client: ConvexStakingWrapper. However, `withdraw` does not check if a user has already withdrawn their tokens. Thus a user that can `withdraw` tokens, can call withdraw repeatedly to steal the tokens of others.

### Proof of Concept

tl;dr an attacker that can successfully call `withdraw` once on a shelter, can call it repeatedly to steal the funds of others. Below is a detailed scenario where this situation can be exploited.

1.  Mallory deposits 1 `wETH` into `ConvexStakingWrapper` using [`deposit`](https://github.com/code-423n4/2022-02-concur/blob/shelter-client/contracts/ConvexStakingWrapper.sol#L280). Let's also assume that other users have deposited 2 `wETH` into the same contract.
2.  An emergency happens and the owner of `ConvexStakingWrapper` calls `setShelter(shelter)` and `enterShelter([pidOfWETHToken, ...])`. Now `shelter` has 3 `wETH` and is activated for `wETH`.
3.  Mallory calls `shelter.withdraw(wETHAddr, MalloryAddr)`, Mallory will rightfully receive 1 wETH because her share of wETH in the shelter is 1/3.
4.  Mallory calls `shelter.withdraw(wETHAddr, MalloryAddr)` again, receiving 1/3\*2 = 2/3 wETH. `withdraw` does not check that she has already withdrawn. This time, the wETH does not belong to her, she has stolen the wETH of the other users. She can continue calling `withdraw` to steal the rest of the funds

### Recommended Mitigation Steps

To mitigate this, `withdraw` must first check that `msg.sender` has not withdrawn this token before and `withdraw` must also record that `msg.sender` has withdrawn the token.
The exact steps for this are below:

1.  Add the following line to the beginning of `withdraw` (line 53):

<!---->

    require(!claimed[_token][msg.sender], "already claimed")

2.  Replace [line 55](https://github.com/code-423n4/2022-02-concur/blob/main/contracts/Shelter.sol#L55) with the following:

<!---->

    claimed[_token][msg.sender] = true;

This replacement is necessary because we want to record who is withdrawing, not where they are sending the token which isn't really useful info.

**[ryuheimat (Concur) confirmed](https://github.com/code-423n4/2022-02-concur-findings/issues/246)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-02-concur-findings/issues/246#issuecomment-1092877228):**
 > The warden has identified a logical fallacy in the `Shelter` contract.
> 
> This would allow a caller to claim their tokens multiple times, as long as they send them to a new address.
> 
> Mitigation is as simple as checking claims against `msg.sender`, however because all funds can be drained, this finding is of High Severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Concur Finance |
| Report Date | N/A |
| Finders | Czar102, mtz, Ryyy, danb, cmichel, Rhynorater, 0x1f8b, GeekyLumberjack, csanuragjain, cccz, leastwood, hickuphh3, Ruhum, 0xliumin, ShadowyNoobDev, bitbopper, gzeon, Alex the Entreprenerd, hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-concur
- **GitHub**: https://github.com/code-423n4/2022-02-concur-findings/issues/246
- **Contest**: https://code4rena.com/contests/2022-02-concur-finance-contest

### Keywords for Search

`Wrong Math, Reentrancy, Business Logic`

