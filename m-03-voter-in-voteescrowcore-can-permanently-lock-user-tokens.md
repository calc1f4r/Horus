---
# Core Classification
protocol: Golom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8740
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/712

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_marketplace
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - scaraven
---

## Vulnerability Title

[M-03] Voter in `VoteEscrowCore` can permanently lock user tokens

### Overview


This bug report is about a vulnerability in the VoteEscrowCore.sol code which could allow a malicious voter to arbitrarily increase the number of attachments or set the voted status of a token to true. This would prevent the token from being withdrawn, merged or transfered thereby locking the tokens into the contract for as long as the voter would like. The malicious voter could achieve this by calling either the voting() or attach() functions. The impact of this vulnerability is high, as it could cause a user to lose their tokens. 

The vulnerability was found using the VS Code tool. The recommended mitigation steps include either removing the voting() and attach() functions from the code, or setting the voter to be a smart contract which is not malicious.

### Original Finding Content


<https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/vote-escrow/VoteEscrowCore.sol#L873-L876><br>

<https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/vote-escrow/VoteEscrowCore.sol#L883-L886><br>

<https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/vote-escrow/VoteEscrowCore.sol#L894><br>

<https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/vote-escrow/VoteEscrowCore.sol#L538><br>

<https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/vote-escrow/VoteEscrowCore.sol#L1008><br>

A malicious voter can arbitrarily increase the number of `attachments` or set the `voted` status of a token to true. This prevents the token from being withdrawn, merged or transfered thereby locking the tokens into the contract for as long as the voter would like.

I submitted this is as a medium severity because it has external circumstances (a malicious voter) however has a very high impact if it does occur.

### Proof of Concept

1.  A user creates a lock for their token and deposits it into the VoteEscrowDelegate/Core contract.
2.  The malicious voter then calls either `voting()` or `attach()` thereby preventing the user withdrawing their token after the locked time bypasses

### Tools Used

VS Code

### Recommended Mitigation Steps

I have not seen any use of `voting()` or `attach()` in any of the other contracts so it may be sensible to remove those functions altogether. On the other hand, setting voter to be smart contract which is not malicious offsets this problem.

**[zeroexdead (Golom) confirmed](https://github.com/code-423n4/2022-07-golom-findings/issues/712)**

**[zeroexdead (Golom) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/712#issuecomment-1236182159):**
 > Removed Voter: https://github.com/golom-protocol/contracts/commit/03572010ef868597310f4736c91aacf3aa044ce9

**[0xsaruman (Golom) resolved](https://github.com/code-423n4/2022-07-golom-findings/issues/712)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Golom |
| Report Date | N/A |
| Finders | scaraven |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/712
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`vulnerability`

