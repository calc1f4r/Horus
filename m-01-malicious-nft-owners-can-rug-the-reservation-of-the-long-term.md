---
# Core Classification
protocol: Coded Estate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45197
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-10-coded-estate
source_link: https://code4rena.com/reports/2024-10-coded-estate
github_link: https://github.com/code-423n4/2024-10-coded-estate-findings/issues/37

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
finders_count: 2
finders:
  - nnez
  - Ch\_301
---

## Vulnerability Title

[M-01]  Malicious NFT owners can rug the reservation of the long-term

### Overview


The bug report is about a vulnerability in the `execute.rs` code of the Coded Estate project. The bug allows a malicious homeowner to steal a user's funds by taking advantage of the `withdrawtolandlord()` and `rejectreservationforlongterm()` functions. This can be done by waiting for the reservation to start, withdrawing most of the funds, and then rejecting the reservation to only refund a small portion of the initial deposit. The recommended mitigation step is to not allow homeowners to reject active reservations. The project owner has acknowledged the issue and stated that the platform will work with a monthly deposit system, so this vulnerability may not be an issue.

### Original Finding Content


<https://github.com/code-423n4/2024-10-coded-estate/blob/main/contracts/codedestate/src/execute.rs#L1490-L1541>

<https://github.com/code-423n4/2024-10-coded-estate/blob/main/contracts/codedestate/src/execute.rs#L1786-L1854>

### Description

Due to the long period of the long-term rent, the Homeowner has an advantage in that type of reservation, which is the ability to withdraw a part from the deposited amount by the tenant. This applies only to reservations made more than one month in advance. This could be done by using `execute.rs#withdrawtolandlord()` function.

```rust
if item.deposit_amount - Uint128::from(token.longterm_rental.price_per_month) < Uint128::from(amount)  {
```

The withdrawn amount will be subtracted from the user's `deposit_amount` state:

```rust
token.rentals[position as usize].deposit_amount -= Uint128::from(amount);
```

On the other side, the NFT owner can trigger `execute.rs#rejectreservationforlongterm()` to reject any reservation at any time even if it currently running, it will send back `.deposit_amount` as a refundable amount to the user.

However, a malicious homeowner can the advantages of `execute.rs#rejectreservationforlongterm()` and `execute.rs#withdrawtolandlord()` to steal a user's funds and reject them in two simple steps:

1. Wait for the reservation to start and call `execute.rs#withdrawtolandlord()`. this will transfer most of the funds out.
2. Now, invoke `execute.rs#rejectreservationforlongterm()` to kick the user out, this will transfer back to the user only a small presenting of his initial deposit.

Note: The homeowner has the power to reject any reservation even if it is currently active by triggering `rejectreservationforlongterm()` and refunding user money; however, using this function, the refundable amount is the same initial deposit.

### Recommended Mitigation Steps

Don't allow to reject active reservations.

**[blockchainstar12 (Coded Estate) acknowledged and commented](https://github.com/code-423n4/2024-10-coded-estate-findings/issues/37#issuecomment-2421001521):**
 > Actually, the platform will work as monthly deposit logic and this won't be issue.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Coded Estate |
| Report Date | N/A |
| Finders | nnez, Ch\_301 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-10-coded-estate
- **GitHub**: https://github.com/code-423n4/2024-10-coded-estate-findings/issues/37
- **Contest**: https://code4rena.com/reports/2024-10-coded-estate

### Keywords for Search

`vulnerability`

