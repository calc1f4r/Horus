---
# Core Classification
protocol: Sonic Gateway Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43958
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/sonic-gateway-audit
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

Users with Account Abstraction Wallets May Lose Bridged Funds Due to Address Mismatch

### Overview


This bug report discusses an issue with using account abstraction wallets on different chains. When a user deposits tokens using the `deposit` function on one chain and then tries to claim them on the other chain using the `claim` function, the transaction fails due to a mismatch in addresses. This is because the deposit is recorded using a hash of the user's address on the first chain, but the address derived from the account abstraction wallet on the second chain could be different. This can result in a permanent loss of funds, as the only way to retrieve the tokens would be for the bridge to be marked as dead. This bug has been resolved in a recent update.

### Original Finding Content

When using account abstraction wallets, users may have different addresses across chains for the same account. If a user using account abstraction deposits tokens via the bridge and later attempts to claim them on the other chain while having a different address, the transaction will revert due to an address mismatch.


When the user deposits tokens on L1 using the [`deposit` function](https://github.com/Fantom-foundation/Bridge/blob/558465d3aba2ffae1a4436a2fc14c723b82926df/contracts/TokenDeposit.sol#L45) of the `TokenDeposit` contract, the deposit is recorded using a hash of the L1 address `msg.sender`, the token address, and the amount. On L2, when attempting to claim the tokens via the [`claim` function](https://github.com/Fantom-foundation/Bridge/blob/558465d3aba2ffae1a4436a2fc14c723b82926df/contracts/Bridge.sol#L39) of the Bridge contract, the L2 address derived from the account abstraction wallet could differ from the L1 address, causing the proof verification to fail in the [`verifyProof`](https://github.com/Fantom-foundation/Bridge/blob/558465d3aba2ffae1a4436a2fc14c723b82926df/contracts/Bridge.sol#L43). As a result, the only way to retrieve the deposited tokens would be for the bridge to be marked as dead so that the user could call `cancelDepositWhileDead`. However, this would be an extremely unlikely scenario, and the user would most likely experience a permanent loss of funds.


Consider clearly documenting the fact that the bridge requires the same user address on both networks for proper functionality, which may not be the case with account abstraction wallets.


***Update:** Resolved in [pull request \#63](https://github.com/Fantom-foundation/Bridge/pull/63). The Sonic team stated:*



> *We fixed it by including `msg.sender` in the internal unique ID.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Sonic Gateway Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/sonic-gateway-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

