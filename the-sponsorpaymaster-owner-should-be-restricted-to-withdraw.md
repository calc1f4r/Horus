---
# Core Classification
protocol: Kinto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30494
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Kinto/README.md#1-the-sponsorpaymaster-owner-should-be-restricted-to-withdraw
github_link: none

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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

The SponsorPaymaster owner should be restricted to withdraw

### Overview


The bug report is about an issue with the code in the SponsorPaymaster contract. The code contains lines that are causing the sum of balances to not change during UserOp execution. This means that some accounts will not be able to withdraw their funds. The bug report recommends removing a specific line of code to fix the issue.

### Original Finding Content

##### Description

`SponsorPaymaster._postOp()` has these lines:
```
balances[account] -= ethCost;
contractSpent[account] += ethCost;
balances[owner()] += ethCost;
```
- https://github.com/KintoXYZ/kinto-core/blob/f7dd98f66b9dfba1f73758703b808051196e740b/src/paymasters/SponsorPaymaster.sol#L160-L162

So, the sum of balances is not changed during UserOp execution.
The same sum of user balances is duplicated in EntryPoint.deposits[], as every SponsorPaymaster deposit and withdrawal is duplicated the same way towards the EntryPoint.
But every UserOp execution decreases the sum of balances stored in the EntryPoint (written ETH balance stored in `Entrypoint.deposits[paymaster]` is transferred to a `beneficiary`). However, the sum of balances written in Paymaster for all accounts has not changed.

It means that some of the `SponsorPaymaster` accounts will not be able to withdraw.
The owner accumulates `ethCost` on every `SponsorPaymaster` usage. If the owner withdraws using `SponsorPaymaster.withdrawTokensTo()`, some other of the `SponsorPaymaster` depositors will have less funds actually stored at `Entrypoint`. 
As a result, operations will fail - having a zero balance on EntryPoint, but a non-zero balance on `SponsorPaymaster`.

##### Recommendation

We recommend removing `balances[owner()] += ethCost;` from `SponsorPaymaster._postOp()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Kinto |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Kinto/README.md#1-the-sponsorpaymaster-owner-should-be-restricted-to-withdraw
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

