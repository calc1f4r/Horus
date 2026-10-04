---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: uncategorized
vulnerability_type: ownership

# Attack Vector Details
attack_type: ownership
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5915
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/99

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - ownership

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - aphak5010
---

## Vulnerability Title

[M-07] OwnableSmartWallet: Multiple approvals can lead to unwanted ownership transfers

### Overview


This bug report is about the OwnableSmartWallet contract. This contract allows an owner to approve addresses that can then claim ownership of the contract. However, when ownership is transferred from one user to another, the existing code does not revoke all approvals that the previous owner has given. This can lead to unwanted transfers of ownership. 

To demonstrate this, User A can approve both User B and User C to claim ownership. User B will then be able to claim ownership, but only User A's approval for User B will be revoked, not User A's approval for User C. If User B then transfers ownership back to User A, User C will still be able to claim ownership even though this time User A has not approved User C.

The recommended mitigation steps are to invalidate all approvals the previous owner has given when another User becomes the owner of the OwnableSmartWallet. Unfortunately, a statement like `delete _isTransferApproved[owner()]` cannot be used, so an array that keeps track of approvals should be used as suggested in a StackExchange question.

### Original Finding Content


<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/smart-wallet/OwnableSmartWallet.sol#L94><br>
<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/smart-wallet/OwnableSmartWallet.sol#L105-L106>

The `OwnableSmartWallet` contract employs a mechanism for the owner to approve addresses that can then claim ownership (<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/smart-wallet/OwnableSmartWallet.sol#L94>) of the contract.

The source code has a comment included which states that "Approval is revoked, in order to avoid unintended transfer allowance if this wallet ever returns to the previous owner" (<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/smart-wallet/OwnableSmartWallet.sol#L105-L106>).

This means that when ownership is transferred from User A to User B, the approvals that User A has given should be revoked.

The existing code does not however revoke all approvals that User A has given. It only revokes one approval.

This can lead to unwanted transfers of ownership.

### Proof of Concept

1.  User A approves User B and User C to claim ownership
2.  User B claims ownership first
3.  Only User A's approval for User B is revoked, not however User A's approval for User C
4.  User B transfers ownerhsip back to User A
5.  Now User C can claim ownership even though this time User A has not approved User C

### Tools Used

VSCode

### Recommended Mitigation Steps

You should invalidate all approvals User A has given when another User becomes the owner of the OwnableSmartWallet.

Unfortunately you cannot use a statement like `delete _isTransferApproved[owner()]`.

So you would need an array that keeps track of approvals as pointed out in this StackExchange question: <https://ethereum.stackexchange.com/questions/15553/how-to-delete-a-mapping>

**[vince0656 (Stakehouse) confirmed](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/99#issuecomment-1329517472)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | aphak5010 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/99
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Ownership`

