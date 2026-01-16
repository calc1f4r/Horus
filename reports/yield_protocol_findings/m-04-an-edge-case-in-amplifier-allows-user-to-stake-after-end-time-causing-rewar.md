---
# Core Classification
protocol: Mute.io
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16044
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-03-mute-switch-versus-contest
source_link: https://code4rena.com/reports/2023-03-mute
github_link: https://github.com/code-423n4/2023-03-mute-findings/issues/23

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
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - HollaDieWaldfee
  - evan
  - hansfriese
  - chaduke
---

## Vulnerability Title

[M-04] An edge case in amplifier allows user to stake after end time, causing reward to be locked in the contract

### Overview


A bug report has been filed for the MuteAmplifier.sol contract, which is part of the 2023-03-mute project. The bug is that if the staking period ends and nobody has staked, a malicious user can front-run the rescueTokens call with a call to stake to lock all the rewards inside the contract indefinitely. 

The bug is caused by the code in lines 208-212 of MuteAmplifier.sol, which includes a require statement that should not be inside the else block. This statement allows a single user to stake even though the period has ended. As a result, the protocol can't withdraw the rewards with rescueToken since there is a staker, and no reward has been claimed yet.

The impact of this bug is that the rewards can be locked inside the contract indefinitely.

The bug was identified through manual review.

The recommended mitigation step is to remove the require statement from the else block in lines 208-212 of MuteAmplifier.sol.

### Original Finding Content


Observe that if nobody has staked after the period has ended, it's still possible for a single user to stake even though the period has ended.<br>
<https://github.com/code-423n4/2023-03-mute/blob/main/contracts/amplifier/MuteAmplifier.sol#L208-L212>

            if (firstStakeTime == 0) {
                firstStakeTime = block.timestamp;
            } else {
                require(block.timestamp < endTime, "MuteAmplifier::stake: staking is over");
            }

The staker can't get any of the rewards because the update modifier won't drip the rewards (since \_mostRecentValueCalcTime = firstStakeTime >= endTime).<br>
<https://github.com/code-423n4/2023-03-mute/blob/main/contracts/amplifier/MuteAmplifier.sol#L89-L95>

            if (_mostRecentValueCalcTime == 0) {
                _mostRecentValueCalcTime = firstStakeTime;
            }

            uint256 totalCurrentStake = totalStake();

            if (totalCurrentStake > 0 && _mostRecentValueCalcTime < endTime) {
                ...
            }

At the same time, the protocol can't withdraw the rewards with rescueToken either since there is a staker, and no reward has been claimed yet (so the following check fails).<br>
<https://github.com/code-423n4/2023-03-mute/blob/main/contracts/amplifier/MuteAmplifier.sol#L187>

            else if (tokenToRescue == muteToken) {
                if (totalStakers > 0) {
                    require(amount <= IERC20(muteToken).balanceOf(address(this)).sub(totalRewards.sub(totalClaimedRewards)),
                        "MuteAmplifier::rescueTokens: that muteToken belongs to stakers"
                    );
                }
            }

### Impact

Suppose the staking period ends and nobody has staked. The admin would like to withdraw the rewards. A malicious user can front-run the rescueTokens call with a call to stake to lock all the rewards inside the contract indefinitely.

### Recommended Mitigation Steps

<https://github.com/code-423n4/2023-03-mute/blob/main/contracts/amplifier/MuteAmplifier.sol#L208-L212>

The require shouldn't be inside the else block.

**[mattt21 (Mute Switch) confirmed](https://github.com/code-423n4/2023-03-mute-findings/issues/23#issuecomment-1499293162)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mute.io |
| Report Date | N/A |
| Finders | HollaDieWaldfee, evan, hansfriese, chaduke |

### Source Links

- **Source**: https://code4rena.com/reports/2023-03-mute
- **GitHub**: https://github.com/code-423n4/2023-03-mute-findings/issues/23
- **Contest**: https://code4rena.com/contests/2023-03-mute-switch-versus-contest

### Keywords for Search

`vulnerability`

