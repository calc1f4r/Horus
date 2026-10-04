---
# Core Classification
protocol: Harpie
chain: everychain
category: uncategorized
vulnerability_type: replay_attack

# Attack Vector Details
attack_type: replay_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3374
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/3
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-harpie-judging/tree/main/004-M

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - replay_attack
  - cross_chain

protocol_categories:
  - staking_pool
  - oracle

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - minhquanym
  - IllIllI
  - JohnSmith
---

## Vulnerability Title

M-2: Cross-chain replay attacks are possible with `changeRecipientAddress()`

### Overview


This bug report is about a vulnerability found in the `changeRecipientAddress()` function of the Harpie Vault smart contract. It was found by minhquanym, JohnSmith, and IllIllI, and was tested using manual review. 

The vulnerability is that there is no `chain.id` in the signed data, which means that mistakes made on one chain can be re-applied to a new chain. This could lead to a cross-chain replay attack, where an attacker could create the same address that the user tried to, and steal the funds from there. 

The Harpie Team fixed the vulnerability by adding the `chain.id` to the signature and signature validation, and this fix was confirmed by Lead Senior Watson. The fix can be found in the link provided in the report.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-harpie-judging/tree/main/004-M 

## Found by 
minhquanym, JohnSmith, IllIllI

## Summary
Mistakes made on one chain can be re-applied to a new chain

## Vulnerability Detail
There is no `chain.id` in the signed data

## Impact
If a user does a `changeRecipientAddress()` using the wrong network, an attacker can replay the action on the correct chain, and steal the funds a-la the wintermute gnosis safe attack, where the attacker can create the same address that the user tried to, and steal the funds from there

## Code Snippet
https://github.com/Harpieio/contracts/blob/97083d7ce8ae9d85e29a139b1e981464ff92b89e/contracts/Vault.sol#L60-L73

## Tool used

Manual Review

## Recommendation
Include the `chain.id` in what's hashed

## Harpie Team
Added chainId to signature and signature validation. Fix [here](https://github.com/Harpieio/contracts/pull/4/commits/de24a50349ec014163180ba60b5305098f42eb14).

## Lead Senior Watson
This is true assuming the contract address is the same across other chains. Confirmed fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Harpie |
| Report Date | N/A |
| Finders | minhquanym, IllIllI, JohnSmith |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-harpie-judging/tree/main/004-M
- **Contest**: https://app.sherlock.xyz/audits/contests/3

### Keywords for Search

`Replay Attack, Cross Chain`

