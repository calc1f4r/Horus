---
# Core Classification
protocol: Orderly Solana Vault Contract
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43629
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/524
source_link: none
github_link: https://github.com/sherlock-audit/2024-09-orderly-network-solana-contract-judging/issues/99

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
finders_count: 13
finders:
  - dod4ufn
  - Silvermist
  - shaflow01
  - g
  - S3v3ru5
---

## Vulnerability Title

H-2: A malicious user can withdrawals another user's money

### Overview


This bug report discusses an issue where a malicious user can withdraw money from another user's account. The root cause of this issue is a shared vault authority signing mechanism, which allows any user to use the same authority to withdraw funds. Additionally, there is no check to ensure that the wallet receiving the funds belongs to the same user who initiated the withdrawal request. This allows the attacker to steal the entire withdrawn amount from the victim's account without any corresponding loss. A possible attack path is described, but there is no response regarding internal or external pre-conditions, a proof of concept, or mitigation steps. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-09-orderly-network-solana-contract-judging/issues/99 

## Found by 
0rpse, 0xBoboShanti, Q7, S3v3ru5, Silvermist, Tendency, chinepun, dod4ufn, g, infect3d, krikolkk, shaflow01, ubermensch
### Summary

A shared vault authority signing mechanism will cause unauthorized withdrawals for users, as User A can withdraw funds belonging to User B.

### Root Cause
In the [OAppLzReceive](https://github.com/sherlock-audit/2024-09-orderly-network-solana-contract/blob/a40ed80ce4a196bc81bfa6dfb749c19b92c623b0/solana-vault/packages/solana/contracts/programs/solana-vault/src/instructions/oapp_instr/oapp_lz_receive.rs#L113-L114), the `vault_authority_seeds` are shared across all users, allowing any user with valid withdrawal parameters to use the same PDA signing authority. As a result, any valid withdrawal request can be signed by the vault without distinguishing which user is performing the withdrawal. 

Also, there is no check that the wallet receiving the funds belongs to the same user for whom the withdrawal request was initiated. The system only checks that the withdrawal message comes from a valid sender (peer.address == params.sender), but does not verify that the user account corresponds to the sender.

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

1. User B initiates a withdrawal on the Ethereum side and a valid withdraw message is sent to the Solana. 
2. User A accesses the valid withdrawal messages corresponding to User B's account and calls the function before User B.
3. Since there is no check to ensure the User A uses a withdrawal message corresponding to his account, the withdraw is successfully executed and User A steals User B's money.

### Impact

The attacker steals the entire withdrawn amount from User B's account without any corresponding loss.

### PoC

_No response_

### Mitigation

_No response_

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Orderly Solana Vault Contract |
| Report Date | N/A |
| Finders | dod4ufn, Silvermist, shaflow01, g, S3v3ru5, 0rpse, krikolkk, Tendency, infect3d, ubermensch, 0xBoboShanti, chinepun, Q7 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-09-orderly-network-solana-contract-judging/issues/99
- **Contest**: https://app.sherlock.xyz/audits/contests/524

### Keywords for Search

`vulnerability`

