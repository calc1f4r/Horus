---
# Core Classification
protocol: Trader Joe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42466
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-trader-joe
source_link: https://code4rena.com/reports/2022-01-trader-joe
github_link: https://github.com/code-423n4/2022-01-trader-joe-findings/issues/32

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
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-07] withdrawAVAX() function has call to sender without reentrancy protection

### Overview


The bug report is about a potential issue in a contract called LauchEvent.sol, which allows the caller to reenter the function and potentially other functions in the protocol. This can lead to reentrancy and cross-function reentrancy, which can be exploited by hackers. The recommended solution is to add a reentrancy guard modifier to the withdrawAVAX() function to prevent this issue. The issue has been confirmed and resolved by the Trader Joe team.

### Original Finding Content

_Submitted by jayjonah8_

In LauchEvent.sol the withdrawAVAX() function makes an external call to the msg.sender by way of \_safeTransferAVAX.  This allows the caller to reenter this and other functions in this and other protocol files.  To prevent reentrancy and cross function reentrancy there should be reentrancy guard modifiers placed on the withdrawAVAX() function and any other function that makes external calls to the caller.

#### Proof of Concept

<https://github.com/code-423n4/2022-01-trader-joe/blob/main/contracts/LaunchEvent.sol#L368>

<https://github.com/code-423n4/2022-01-trader-joe/blob/main/contracts/LaunchEvent.sol#L370>

#### Recommended Mitigation Steps

Add reentrancy guard modifier to withdrawAVAX() function.

**[cryptofish7 (Trader Joe) confirmed and commented](https://github.com/code-423n4/2022-01-trader-joe-findings/issues/32#issuecomment-1026347427):**
 > Resolved using CEI: https://github.com/traderjoe-xyz/rocket-joe/commit/dbd19cc400abb5863edfc0443dd408ba5ae3e99a



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Trader Joe |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-trader-joe
- **GitHub**: https://github.com/code-423n4/2022-01-trader-joe-findings/issues/32
- **Contest**: https://code4rena.com/reports/2022-01-trader-joe

### Keywords for Search

`vulnerability`

