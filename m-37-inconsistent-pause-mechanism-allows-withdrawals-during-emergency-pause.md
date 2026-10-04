---
# Core Classification
protocol: ZetaChain Cross-Chain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58672
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/857
source_link: none
github_link: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/410

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
finders_count: 8
finders:
  - Al-Qa-qa
  - 0xC2939291
  - Goran
  - Alpha
  - zerbyte
---

## Vulnerability Title

M-37: Inconsistent Pause Mechanism Allows Withdrawals During Emergency Pause

### Overview


The bug report is about a potential security issue in the `withdraw_impl` function of the `gateway.move` code. This function does not have a pause mechanism, unlike the deposit functionality, which could allow withdrawals to continue even when the system should be paused. This creates an inconsistency in the security controls and could be exploited by attackers. The root cause of this issue is that the `withdraw_impl` function does not have a pause flag, while the deposit functions do. This could be exploited by attackers with WithdrawCap to withdraw funds from the gateway vaults while legitimate deposits are blocked. The impact of this bug is that withdrawals can continue even when the system should be completely paused, and it creates confusion and potential vulnerabilities due to different security controls for deposits and withdrawals. To mitigate this issue, a `paused` variable should be added to the Gateway struct and used to check both deposits and withdrawals. This will ensure that withdrawals are properly paused when the system is in a paused state.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/410 

## Found by 
0xC2939291, Al-Qa-qa, Alpha, Goran, Laksmana, ifeco445, pks\_, zanderbyte

### Summary

The `withdraw_impl` function in `gateway.move` lacks a pause mechanism, unlike the deposit functionality which has proper pause checks. This creates an inconsistency in the security controls and could allow withdrawals to continue even when the system should be paused.

### Root Cause

The `withdraw_impl` function does not have a pause flag, while the deposit functions (`check_receiver_and_deposit_to_vault`) have the flag. This creates a security gap where withdrawals can continue even when deposits are paused.

https://github.com/sherlock-audit/2025-04-zetachain-cross-chain/blob/main/protocol-contracts-sui/sources/gateway.move#L271-L282

### Internal Pre-conditions

- The caller must have a valid WithdrawCap
- The coin type must be whitelisted
- The nonce must match the current gateway nonce


### External Pre-conditions

- The caller must have permission to call the function
- The system(gateway vault) must have sufficient balance for the withdrawal

### Attack Path

1. An attacker with WithdrawCap can continue to withdraw funds even when the system is in a paused state
2. This could be exploited during emergency situations when the system should be completely paused
3. The attacker could withdraw funds from gateway vaults while legitimate deposits are blocked

### Impact

1. Withdrawals can continue even when the system should be completely paused
2. Different security controls for deposits and withdrawals create confusion and potential vulnerabilities

### PoC

_No response_

### Mitigation

Add a `paused` variable to Gateway struct and use this check in both deposits and withdrawals.
```move
assert!(!gateway.paused, EPaused);
```
This will ensure that withdrawals are properly paused when the system is in a paused state.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | ZetaChain Cross-Chain |
| Report Date | N/A |
| Finders | Al-Qa-qa, 0xC2939291, Goran, Alpha, zerbyte, pks\_, ifeco445, Laksmana |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/410
- **Contest**: https://app.sherlock.xyz/audits/contests/857

### Keywords for Search

`vulnerability`

