---
# Core Classification
protocol: NetMind
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59207
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html
source_link: https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html
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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Jennifer Wu
  - Cameron Biniamow
  - Jonathan Mevs
---

## Vulnerability Title

Centralization Risks

### Overview


This bug report discusses issues with centralization in a protocol that involves locking assets and distributing rewards. The report highlights specific examples of centralization and suggests that the team should make this centralization clear to users and consider putting more processes on the blockchain or providing clear documentation. The report also mentions that some roles in the system have excessive privileges and that a malicious address could compromise the system.

### Original Finding Content

**Update**
The client acknowledged the issue and provided the following explanation:

> FixedLock.sol: This contract is used for locking early cooperative users' assets. The logic of this contract includes reward-related logic, but it will never distribute any rewards.
> 
> 
> RewardContract: In this system, the calculation and distribution of rewards are carried out by the collaboration of on-chain and off-chain services. This is because the evaluation of contributions from the off-chain Netmind-GPU network (such as GPU operation status detection, network speed, and other performance checks) is involved. Since this data cannot be directly migrated to the blockchain, we introduced a consensus network maintained by multiple cooperating parties to ensure fairness based on this situation.

**File(s) affected:**`Purchase.sol`, `FixedLock.sol`, `Pledge.sol`, `LongTermPledge.sol`, `RewardContract.sol`

**Description:** This protocol contains significant centralization, as some roles in the system have excessive privileges and key protocol actions take place in undocumented off-chain processes. We include a non-exhaustive list of the most striking examples of this centralization below:

*   Depositors into `FixedLock` will only earn rewards if the team deposits enough Rewards to fund reward claims. If both Alice and Bob were to stake for the same amount of time, but the team deposited rewards that were only sufficient for Alice to claim, and Alice claimed first, Bob would have no way of claiming his rewards until the team deposits again.

*   On-chain, there is no synchronization between the stakes made in either `Pledge` or `LongTermPledge` and the rewards that can be claimed in `RewardContract`. The smart contracts enforce no guarantee of rewards for stakers, and when rewards are claimed, there is no consideration of the existing stake that was made on-chain. As a result, staked users looking to claim rewards at `RewardContract.withdrawToken()` are totally reliant on the nodes defined in `Pledge` (more specifically, `conf.Staking()`) acting honestly to grant the expected rewards to the staker. It is worth emphasizing here that the reward calculation is done in an undocumented process, off-chain.

*   Documentation from the NMT team suggests that `Purchase.swapToken()` is a method allowing users to purchase training services through USDC. During discussions during the audit, the NMT team described that a user purchasing Training Tasks with fiat will have their account managed off-chain instead of in the `AccountManage` contract. Native NMT depositors have access to increase or decrease their balance, providing significantly more account control to users who purchase using fiat. If a user were to `Purchase.swapToken()` to provide an increase to a balance for Training Tasks, this user must completely trust the NMT Team to honor their purchased amount and adequately manage the account off-chain.

*   `Conf.wards` authorized accounts have excessive privileges, and a malicious ward address can compromise the system (see [NETM-3](https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html#findings-qs3)).

**Recommendation:** Make clear this centralization to users. Looking forward, the team should consider putting more of these processes on chain, or providing clear documentation to users on the specifics of off-chain components.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | NetMind |
| Report Date | N/A |
| Finders | Jennifer Wu, Cameron Biniamow, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html

### Keywords for Search

`vulnerability`

