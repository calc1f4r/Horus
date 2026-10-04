---
# Core Classification
protocol: Paladin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24717
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-paladin
source_link: https://code4rena.com/reports/2022-03-paladin
github_link: https://github.com/code-423n4/2022-03-paladin-findings/issues/7

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
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] Users at `UNSTAKE_PERIOD` can assist other users in unstaking tokens.

### Overview


This bug report concerns a scenario where user A can assist user B in unstaking tokens in a smart contract deployed by user A. User A has a cooldown of Day 0 and user B has a cooldown of Day 15. When user B transfers 100 tokens to user A, the latest cooldown of user A is calculated as (100 * Day 15 + 200 * Day 0)/(100+200) = Day 5. This means that user A can unstake tokens even though they are still in the UNSTAKE_PERIOD. The bug is found in the _getNewReceiverCooldown function in the HolyPaladinToken.sol#L1131.

The recommended mitigation steps for this bug are to adjust the UNSTAKE_PERIOD. This can be done to reduce the possibility of such a scenario occurring. Kogaroshi (Paladin) has already reduced the Unstake Period to 2 days to reduce the possibility of such a scenario. This change is found in the PaladinFinance/Paladin-Tokenomics#4 pull request.

### Original Finding Content

_Submitted by cccz, also found by JC and gzeon_

Consider the following scenario:
Day 0: User A stakes 200 tokens and calls the cooldown function. At this time, user A's cooldown is Day 0.
Day 15: User B stakes 100 tokens, but then wants to unstake tokens. So user A said that he could assist user B in unstaking tokens, and this could be done by deploying a smart contract.
In the smart contract deployed by user A, user B first needs to transfer 100 tokens to user A. In the \_getNewReceiverCooldown function, \_senderCooldown is Day 15 and receiverCooldown is Day 0, so the latest cooldown of user A is (100 \* Day 15 + 200 \* Day 0)/(100+200) = Day 5.

        function _getNewReceiverCooldown(
            uint256 senderCooldown,
            uint256 amount,
            address receiver,
            uint256 receiverBalance
        ) internal view returns(uint256) {
            uint256 receiverCooldown = cooldowns[receiver];

            // If receiver has no cooldown, no need to set a new one
            if(receiverCooldown == 0) return 0;

            uint256 minValidCooldown = block.timestamp - (COOLDOWN_PERIOD + UNSTAKE_PERIOD);

            // If last receiver cooldown is expired, set it back to 0
            if(receiverCooldown < minValidCooldown) return 0;

            // In case the given senderCooldown is 0 (sender has no cooldown, or minting)
            uint256 _senderCooldown = senderCooldown < minValidCooldown ? block.timestamp : senderCooldown;

            // If the sender cooldown is better, we keep the receiver cooldown
            if(_senderCooldown < receiverCooldown) return receiverCooldown;

            // Default new cooldown, weighted average based on the amount and the previous balance
            return ((amount * _senderCooldown) + (receiverBalance * receiverCooldown)) / (amount + receiverBalance);

        }

Since User A is still at UNSTAKE_PERIOD after receiving the tokens, User A unstakes 100 tokens and sends it to User B.

After calculation, we found that when user A has a balance of X and is at the edge of UNSTAKE_PERIOD, user A can assist in unstaking the X/2 amount of tokens just staked.

### Proof of Concept

[HolyPaladinToken.sol#L1131](https://github.com/code-423n4/2022-03-paladin/blob/main/contracts/HolyPaladinToken.sol#L1131)

### Recommended Mitigation Steps

After calculation, we found that the number of tokens that users at the edge of UNSTAKE_PERIOD can assist in unstaking conforms to the following equation
UNSTAKE_PERIOD/COOLDOWN_PERIOD = UNSTAKE_AMOUNT/USER_BALANCE, when COOLDOWN_PERIOD remains unchanged, the smaller the UNSTAKE_PERIOD, the less tokens the user can assist in unstaking, so UNSTAKE_PERIOD can be adjusted to alleviate this situation.

**[Kogaroshi (Paladin) confirmed, resolved, and commented](https://github.com/code-423n4/2022-03-paladin-findings/issues/7#issuecomment-1084951519):**
 > Reduced the Unstake Period to 2 days to reduce the possibility of such scenario.<br>
> [PaladinFinance/Paladin-Tokenomics#4](https://github.com/PaladinFinance/Paladin-Tokenomics/pull/4)



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Paladin |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-paladin
- **GitHub**: https://github.com/code-423n4/2022-03-paladin-findings/issues/7
- **Contest**: https://code4rena.com/reports/2022-03-paladin

### Keywords for Search

`vulnerability`

