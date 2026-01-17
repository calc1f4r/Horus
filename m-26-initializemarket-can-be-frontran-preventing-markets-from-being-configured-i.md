---
# Core Classification
protocol: Notional Exponent
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62518
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1001
source_link: none
github_link: https://github.com/sherlock-audit/2025-06-notional-exponent-judging/issues/834

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
finders_count: 14
finders:
  - patitonar
  - 0xPhantom2
  - 0xpiken
  - y4y
  - X0sauce
---

## Vulnerability Title

M-26: `initializeMarket` can be frontran, preventing markets from being configured in `MorphoLendingRouter `

### Overview


This bug report discusses a potential issue with the `initializeMarket` function in the MorphoLendingRouter contract. This function is critical for storing data and is used throughout the contract. The problem is that anyone can frontrun the initialization process, creating the same market and causing the initialization to fail. This can lead to a denial of service attack, preventing the corresponding vault from being used. A possible solution is to implement a `try/catch` statement to handle this issue.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-06-notional-exponent-judging/issues/834 

## Found by 
0xBoraichoT, 0xPhantom2, 0xRstStn, 0xodus, 0xpiken, Hueber, Ragnarok, X0sauce, coffiasd, dan\_\_vinci, patitonar, underdog, xiaoming90, y4y

### Summary

`initializeMarket` can be frontran, creating the same morpho market as the expected when initializing. 

### Root Cause

In [MorphoLendingRouter.sol#L51](https://github.com/sherlock-audit/2025-06-notional-exponent/blob/main/notional-v4/src/routers/MorphoLendingRouter.sol#L51), the router will try to initialize a market for a certain market params configuration. Note that `initializeMarket` is the only way to store data for the vault in the corresponding `s_morphoParams` mapping, and it is critical that this mapping is written to, as `marketParams()` wwill [fetch some of the data from the stored mapping(https://github.com/sherlock-audit/2025-06-notional-exponent/blob/main/notional-v4/src/routers/MorphoLendingRouter.sol#L59), and this function is [used across the whole router contract](https://github.com/sherlock-audit/2025-06-notional-exponent/blob/main/notional-v4/src/routers/MorphoLendingRouter.sol#L77).

The problem is that anybody can frontrun the initialization by directly calling morpho's `createMarket()` function, creating the same market. After that, the initialization will fail because Morpho [ensures that the same market can only be created once](https://etherscan.io/address/0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb#code#F1#L154). Because of this, markets initializations will be dos'ed, and the router won't be usable for the corresponding vault with the desired market params.

### Internal Pre-conditions

None.

### External Pre-conditions

None.

### Attack Path

1. `upgradeAdmin` calls `initializeMarket`
2. Malicious user frontruns the call, calling Morpho's `createMarket` with the same market params as the initialization.
3. `initializeMarket` fails due to the [check in market creation](https://etherscan.io/address/0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb#code).

### Impact

Medium, it is possible to DoS market initialization, which will prevent storing the corresponding market for the given vault, preventing such vault from being used. 

### PoC

_No response_

### Mitigation

Consider implementing a `try/catch` statement. If the market creation fails, it will mean the market was already created, allowing configuration to still be performed




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Notional Exponent |
| Report Date | N/A |
| Finders | patitonar, 0xPhantom2, 0xpiken, y4y, X0sauce, 0xodus, dan\_\_vinci, 0xBoraichoT, xiaoming90, Ragnarok, dan\_\_vinci, 0xRstStn, Hueber, coffiasd, underdog |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-06-notional-exponent-judging/issues/834
- **Contest**: https://app.sherlock.xyz/audits/contests/1001

### Keywords for Search

`vulnerability`

