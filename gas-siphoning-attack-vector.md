---
# Core Classification
protocol: UNCX UniswapV3 Liquidity Locker Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32623
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uncx-uniswapv3-liquidity-locker-audit
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Gas Siphoning Attack Vector

### Overview


This bug report is about a vulnerability in a codebase that allows a malicious user to exploit the free gas provided by the protocol. This can happen because the auto-collector role in the codebase allows anyone to call `collect` on behalf of lock owners, and the tokens and position manager used for the transfer are chosen by the user. This can lead to attacks similar to ones seen in the past with other protocols. Possible solutions include creating a whitelist for tokens and a blacklist for locks, or monitoring the gas usage of the auto-collector to prevent it from calling `collect` on problematic positions. The UNCX team has acknowledged the issue but it has not been resolved yet. They plan to only allow certain clients to use the auto-collector and will make sure the tokens used fit their specifications before adding them to the bot.

### Original Finding Content

In the [codebase](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/blob/342c621cc93a13882601b30e547907877f3e3f86/), there is an auto-collector role ([`AUTO_COLLECT_ACCOUNT`](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/blob/342c621cc93a13882601b30e547907877f3e3f86/contracts/UNCX_ProofOfReservesV2_UniV3.sol#L52)) that can call `collect` on behalf of the lock owners to collect their underlying market position fees. However, the tokens being transferred and the position manager being called by the contract are arbitrary and provided by users.


A malicious user can supply the address of a smart contract tailored to take advantage of the free gas. Such attacks have been seen in the past with [FTX's withdrawal mechanism](https://twitter.com/BeosinAlert/status/1580426718711463937) or [dYdX's metatransaction mechanism](https://medium.com/@hacxyk/stealing-gas-from-dydx-0-5-eth-a-day-712c5fdc43a3). Mitigations could include a whitelist for tokens and an auto-collect blacklist for locks, but both of these would stop the protocol from providing its core service.


Consider monitoring the `AUTO_COLLECT_ACCOUNT`'s gas consumption in order to stop it from calling `collect` on problematic positions.


***Update**: Acknowledged, not resolved. The UNCX team stated:*



> *The auto-collector bot is called manually at the moment and only for certain clients. We will make sure tokens fit our spec before adding them to the bot.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UNCX UniswapV3 Liquidity Locker Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uncx-uniswapv3-liquidity-locker-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

