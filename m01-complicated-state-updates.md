---
# Core Classification
protocol: Audius Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11324
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/audius-contracts-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M01] Complicated state updates

### Overview


This bug report is about a critical issue that arises when stake balances are modified. It was found that when multiple operations are executed to increase or decrease the values of the state variables related to the updated stake status, the system becomes error prone and can lead to a malicious delegator permanently locking all stake and rewards for a victim service provider and all of its honest delegators. The report also mentions that a similar pattern is implemented to track the number of votes for Governance proposals.

The report suggests encapsulating these operations into separate functions, one for each type of state update. This way it will be easier to review that the operations are complete, consistent, and complementary. It also suggests formal verification to prove that these critical state variables will always behave as expected and keep the system in a consistent state.

The issue was fixed in pull request #539. Most of the logic was encapsulated in new internal functions. These functions were thoroughly tested in isolation and the issue was resolved.

### Original Finding Content

When stake balances are modified (through [`delegateStake`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/DelegateManager.sol#L116), [`requestUndelegateStake`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/DelegateManager.sol#L183), [`cancelUndelegateStake`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/DelegateManager.sol#L222), [`undelegateStake`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/DelegateManager.sol#L239), and [`slash`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/DelegateManager.sol#L432)), multiple operations are executed to increase or decrease the values of the state variables related to the updated stake status. This is error prone, as shown by the critical issue *“A malicious delegator can permanently lock all stake and rewards for a victim service provider and all of its honest delegators”* where one of the values was not correctly updated.


A similar pattern is implemented to track the number of votes for [`Governance`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol) proposals.


Consider encapsulating these operations into separate functions, one for each type of state update. This way it will be clearer to review that the operations are complete, consistent, and complementary. Some duplication can be removed, and these functions can be thoroughly tested in isolation.


Consider [formal verification](https://en.wikipedia.org/wiki/Formal_verification) to prove that these critical state variables will always behave as expected and keep the system in a consistent state.


***Update:** Fixed in [pull request #539](https://github.com/AudiusProject/audius-protocol/pull/539). Most of the logic was encapsulated in new internal functions, such as the [`_updateDelegatorStake`](https://github.com/AudiusProject/audius-protocol/blob/e16dd3e8af4587bacad902bb66a718b60658b972/eth-contracts/contracts/DelegateManager.sol#L150) and the [`_updateServiceProviderLockupAmount`](https://github.com/AudiusProject/audius-protocol/blob/e16dd3e8af4587bacad902bb66a718b60658b972/eth-contracts/contracts/DelegateManager.sol#L813) functions of the `DelegateManager` contract, and the [`_decreaseVoteMagnitudeNo`](https://github.com/AudiusProject/audius-protocol/blob/e16dd3e8af4587bacad902bb66a718b60658b972/eth-contracts/contracts/Governance.sol#L689) and the [`_increaseVoteMagnitudeYes`](https://github.com/AudiusProject/audius-protocol/blob/e16dd3e8af4587bacad902bb66a718b60658b972/eth-contracts/contracts/Governance.sol#L671) functions of the `Governance` contract.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Audius Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/audius-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

