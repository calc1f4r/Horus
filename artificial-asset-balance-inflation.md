---
# Core Classification
protocol: Opyn Bull Strategy Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10390
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/opyn-bull-strategy-contracts-audit/
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Artificial asset balance inflation

### Overview


This bug report is about the potential for an asset balance inflation attack on all contracts in scope. An attacker could send ETH or any ERC20 token directly to the protocol contracts by using an intermediate contract that uses `selfdestruct` to force funds directly into any protocol contract, bypassing the `receive` require statements in place. 

The `farm` function can recover stray ERC20 token balances, but there is no general way to withdraw ETH. The rebalancing mechanism allows `AuctionBull` to wrap the entire ETH balance into `WETH` and then transfer it out of `BullStrategy` during certain flows of a full rebalance. However, this does not solve the issue entirely. 

The team did not find any attack vector that could exploit this issue, but heavily relying on the use of `balanceOf(address(this))` in many instances across the codebase might pose some risk of an inflation attack. 

The bug was partially resolved in PR #789 by implementing a `farm` function that allows the contract owner to retrieve any asset balance from `AuctionBull`, and expanding the pre-existing `farm` function within `BullStrategy` so `ETH`, `WETH` and `USDC` can also be recovered by the owner if necessary. However, the `farm` function within `BullStrategy` should be restricted when attempting to recover `ETH` if the `Squeeth` controller is shut down, since all user funds will be sitting in `ETH` during that time.

### Original Finding Content

All the contracts in scope are susceptible to an asset balance inflation attack, where a user might send ETH or any ERC20 token directly to the protocol contracts.


For ETH specifically, the only way to do so is by making use of an intermediate contract that uses `selfdestruct` to force funds directly into any protocol contract, bypassing the `receive` require statements in place.


The [`farm`](https://github.com/opynfinance/squeeth-monorepo/blob/521203dc26e5a2c3e26c6d4ad02d513e7df63237/packages/bull-vault/src/BullStrategy.sol#L99) function can recover stray ERC20 token balances (except the [excluded ones](https://github.com/opynfinance/squeeth-monorepo/blob/521203dc26e5a2c3e26c6d4ad02d513e7df63237/packages/bull-vault/src/BullStrategy.sol#L101-L102)), but there is no general way to withdraw ETH. One interesting side effect from the rebalancing mechanism is that `AuctionBull` is capable of [wrapping](https://github.com/opynfinance/squeeth-monorepo/blob/521203dc26e5a2c3e26c6d4ad02d513e7df63237/packages/bull-vault/src/BullStrategy.sol#L215) the entire ETH balance into `WETH` and then [transferring](https://github.com/opynfinance/squeeth-monorepo/blob/521203dc26e5a2c3e26c6d4ad02d513e7df63237/packages/bull-vault/src/BullStrategy.sol#L217) it out of `BullStrategy` during certain flows of a full rebalance. However, this does not solve the issue entirely. Moreover, the `farm` function is not present everywhere. For example, it is absent in [`AuctionBull`](https://github.com/opynfinance/squeeth-monorepo/blob/521203dc26e5a2c3e26c6d4ad02d513e7df63237/packages/bull-vault/src/AuctionBull.sol).


How this can be exploited by a malicious third party is unclear, since the team did not find any attack vector that could exploit that. However, heavily relying on [the use of `balanceOf(address(this))`](https://github.com/opynfinance/squeeth-monorepo/blob/521203dc26e5a2c3e26c6d4ad02d513e7df63237/packages/bull-vault/src/AuctionBull.sol#L504) in many instances across the codebase might pose some risk of an inflation attack.


Consider whether it is safe to leave the doors open for such scenarios and whether it is relevant to include some mitigations, such as implementing a less strict `farm` function to be used across all contracts, or having a restricted function to retrieve stuck ETH.


***Update:** Partially resolved in [PR #789](https://github.com/opynfinance/squeeth-monorepo/pull/789) by implementing a `farm` function that allows the contract `owner` to retrieve any asset balance from `AuctionBull`, and expanding the pre-existing `farm` function within `BullStrategy` so `ETH`, `WETH` and `USDC` can also be recovered by the owner if necessary.*


*However, the `farm` function within `BullStrategy` should be restricted when attempting to recover `ETH` if the `Squeeth` controller is shut down, since all user funds will be sitting in `ETH` during that time.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Opyn Bull Strategy Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/opyn-bull-strategy-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

