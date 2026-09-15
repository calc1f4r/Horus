---
# Core Classification
protocol: Carapace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6616
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/40
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/116

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - clems4ever
  - 0x52
  - mahdikarimi
  - libratus
  - ck
---

## Vulnerability Title

H-7: Sybil on withdrawal requests can allow leverage factor manipulation with flashloans

### Overview


This bug report is about the vulnerability found in the ProtectionPool contract of the Carapace protocol. It was found by a team of five people and is referred to as Issue H-7. This vulnerability allows a malicious user to manipulate the leverage factor by requesting multiple withdrawals with the same tokens from different addresses. This allows them to deposit new funds and withdraw them in the same block, thus manipulating the premium prices. It also allows them to overprotect their lending positions, DOS the protocol, and take advantage of protection sellers. The bug was found through manual review and the recommended solution is to freeze STokens for a depositor once they requested a withdrawal.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/116 

## Found by 
libratus, ck, clems4ever, 0x52, mahdikarimi

## Summary
To be able to withdraw, a user has to request a withdraw first. The only requirement to be able to request a withdraw is to have a balance of SToken upon requesting. By requesting withdraws with the same tokens but from different addresses, a malicious user can create the option to withdraw during one cycle more than what is deposited in the protocol. They cannot drain the protocol since they only have a limited amount of SToken to burn (required to call `withdraw()`), but they acquire the ability to deposit new funds and withdraw them in the same block, thus manipulating premium prices.

## Vulnerability Detail
Consider the following scenario:
A malicious user wants to manipulate `leverageRatio` (to get a cheaper premium for example).

They deposit 10k USDC into the protocol, and get 10k STokens.
They request immediately a withdraw, and transfer STokens to another address and request a withdraw there, repeating the process 10 times.

This works since balance is checked on requesting withdrawal but not locked or committed:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L992-L995

2 cycles later (actually ~1 cycle if the timing is optimized), they have the ability to take a flashloan for 100k USDC, deposit through the 10 addresses used, enjoy the cheaper premium as a protection buyer due to `leverageFactor` being high and withdraw all in the same transaction. 

They can safely repay the flash loan.

## Impact
Protection buyers can use this to: 
- game premium prices, meaning that protection sellers get rugged.
- overprotect their lending positions (used in conjunction with HIGH-02, it can drain the whole protection pool if lending pool defaults).
- DOS the protocol by sending the leverage factor very high.

## Code Snippet

## Tool used
Manual Review

## Recommendation
Freeze STokens for a depositor once they requested a withdrawal.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Carapace |
| Report Date | N/A |
| Finders | clems4ever, 0x52, mahdikarimi, libratus, ck |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/116
- **Contest**: https://app.sherlock.xyz/audits/contests/40

### Keywords for Search

`vulnerability`

