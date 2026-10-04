---
# Core Classification
protocol: Fei Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10996
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fei-protocol-audit/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[C04] Users can claim unreleased rewards or have their funds locked

### Overview


The FeiPool contract is used to deposit FEI/TRIBE liquidity pool (LP) tokens into the Fei Pool to accrue TRIBE tokens as a reward. After some time, users may withdraw their LP tokens and get the accrued rewards. The contract defines the `stakedBalance` and `totalStaked` variables to track users’ staked amounts and the total staked amount in the pool, respectively. These are incremented each time a user deposits liquidity pool tokens into the pool.

However, when a user withdraws their staked tokens and accrued rewards, only the user’s `stakedBalance` is updated, while the `totalStaked` variable remains the same. This leads to incorrect calculations of the amount of redeemable rewards and prevents users from claiming rewards and withdrawing their stake due to a “Redeemable underflow” require statement.

To fix this bug, the `totalStaked` variable should be decremented in the `_withdraw` function to accurately track the total stake in the pool. This has been fixed in PR#19, where the `totalStaked` amount is now being decremented in the `_withdraw` function.

### Original Finding Content

The [`FeiPool` contract](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/FeiPool.sol) allows users to [deposit](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/Pool.sol#L46) `FEI/TRIBE` liquidity pool (LP) tokens into the Fei Pool to accrue `TRIBE` tokens as a reward. After some time, users may want to [withdraw](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/Pool.sol#L52) their LP tokens and get the accrued rewards. To track users’ staked amounts and the total staked amount in the pool, the contract defines the `stakedBalance` and `totalStaked` variables, respectively. These are [incremented](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/Pool.sol#L122-L123) each time a user deposits liquidity pool tokens into the pool.


When a user withdraws their staked tokens and accrued rewards, [only the user’s `stakedBalance` is updated](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/Pool.sol#L133), while the `totalStaked` variable remains the same. Since the [`redeemableRewards` function](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/Pool.sol#L66) depends on the `totalStaked` variable to compute the amount of redeemable rewards in the [`_totalRedeemablePoolTokens` function](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/Pool.sol#L102), the total amount of redeemable tokens for the user is miscalculated, resulting in more tokens being released than what was intended.


Additionally, since the Fei Pool’s total supply of tokens decreases during [claims](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/Pool.sol#L147) and [withdrawals](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/Pool.sol#L138), while the `totalStaked` variable is unchanged, the [`balance` variable](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/Pool.sol#L102) from the `_totalRedeemablePoolTokens` function could become greater than the [`total` variable](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/Pool.sol#L108). This would prevent users from claiming rewards and withdrawing their stake due to [a “Redeemable underflow” require statement](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/Pool.sol#L110).


Consider decrementing the `totalStaked` variable in the [`_withdraw`](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/pool/Pool.sol#L131) function to accurately track the total stake in the pool and avoid these scenarios.


**Update:** *Fixed in [PR#19](https://github.com/fei-protocol/fei-protocol-core/pull/19). The `totalStaked` amount is now being decremented in the `_withdraw` function.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Fei Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/fei-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

