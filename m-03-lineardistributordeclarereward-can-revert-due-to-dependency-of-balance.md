---
# Core Classification
protocol: Malt Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16081
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-02-malt-protocol-versus-contest
source_link: https://code4rena.com/reports/2023-02-malt
github_link: https://github.com/code-423n4/2023-02-malt-findings/issues/35

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
  - algo-stables
  - reserve_currency
  - liquid_staking
  - cdp
  - services

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hansfriese
---

## Vulnerability Title

[M-03] `LinearDistributor.declareReward` can revert due to dependency of balance

### Overview


This bug report is about a vulnerability in the LinearDistributor contract of the RewardSystem. It can cause a permanent Denial of Service (DOS) attack. The attack works by sending some collateral tokens to the LinearDistributor contract which increases the balance, and then calling the declareReward function. This will cause a revert in the _forfeit function, as the balance is greater than the bufferRequirement. The _forfeit function requires that the amount forfeited is less than or equal to the declaredBalance. Since the declareReward function sends vested amount before calling the _forfeit function, and the vested amount will increase over time, this DOS attack will be temporary. However, if the attacker increases the balance enough to cover all reward amount in vesting, the declareReward function will always revert and cause a permanent DOS. The decrementRewards function updates the declaredBalance, but it only decreases it, so it can't mitigate the DOS.

The recommended mitigation step is to track the collateral token balance and add a sweep logic for unused collateral tokens in the LinearDistributor contract.

### Original Finding Content


<https://github.com/code-423n4/2023-02-malt/blob/main/contracts/RewardSystem/LinearDistributor.sol#L147-L151> 

<https://github.com/code-423n4/2023-02-malt/blob/main/contracts/RewardSystem/LinearDistributor.sol#L185-L186> 

<https://github.com/code-423n4/2023-02-malt/blob/main/contracts/RewardSystem/LinearDistributor.sol#L123-L136>

### Impact

`LinearDistributor.declareReward` will revert and it can cause permanent DOS.

### Proof of Concept

In `LinearDistributor.declareReward`, if the balance is greater than the bufferRequirement, the rest will be forfeited.

        if (balance > bufferRequirement) {
          // We have more than the buffer required. Forfeit the rest
          uint256 net = balance - bufferRequirement;
          _forfeit(net);
        }

And in `_forfeit`, it requires forfeited (= balance - bufferRequirement) <= declaredBalance.

      function _forfeit(uint256 forfeited) internal {
        require(forfeited <= declaredBalance, "Cannot forfeit more than declared");

So when an attacker sends some collateral tokens to `LinearDistributor`, the balance will be increased and it can cause revert in `_forfeit` and `declareReward`.

Since `declareReward` sends vested amount before `_forfeit` and the vested amount will be increased by time, so this DOS will be temporary.

        uint256 distributed = (linearBondedValue * netVest) / vestingBondedValue;
        uint256 balance = collateralToken.balanceOf(address(this));

        if (distributed > balance) {
          distributed = balance;
        } 

        if (distributed > 0) {
          // Send vested amount to liquidity mine
          collateralToken.safeTransfer(address(rewardMine), distributed);
          rewardMine.releaseReward(distributed);
        }

        balance = collateralToken.balanceOf(address(this));

But if the attacker increases the balance enough to cover all reward amount in vesting, `declareReward` will always revert and it can cause permanent DOS.

`decrementRewards` updates `declaredBalance`, but it only decreases `declaredBalance`, so it can't mitigate the DOS.

### Recommended Mitigation Steps

Track collateral token balance and add sweep logic for unused collateral tokens in `LinearDistributor`.

**[Picodes (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2023-02-malt-findings/issues/35#issuecomment-1443598496):**
 > As this is a DOS scenario where funds are not at risk and the chances that rewards are lost forever are low, downgrading to Medium.

**[0xScotch (Malt) confirmed and commented](https://github.com/code-423n4/2023-02-malt-findings/issues/35#issuecomment-1446998892):**
 > I agree this is a DOS vector but a continued attack would require the attacker to spend more and more capital. Should be fixed but doesn't pose any risk of material loss.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Malt Protocol |
| Report Date | N/A |
| Finders | hansfriese |

### Source Links

- **Source**: https://code4rena.com/reports/2023-02-malt
- **GitHub**: https://github.com/code-423n4/2023-02-malt-findings/issues/35
- **Contest**: https://code4rena.com/contests/2023-02-malt-protocol-versus-contest

### Keywords for Search

`vulnerability`

