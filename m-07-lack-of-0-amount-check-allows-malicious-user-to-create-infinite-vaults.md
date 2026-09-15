---
# Core Classification
protocol: Cally
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2296
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-cally-contest
source_link: https://code4rena.com/reports/2022-05-cally
github_link: https://github.com/code-423n4/2022-05-cally-findings/issues/91

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
  - services
  - synthetics
  - liquidity_manager
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xDjango
---

## Vulnerability Title

[M-07] Lack of 0 amount check allows malicious user to create infinite vaults

### Overview


This bug report is about a vulnerability in the Cally protocol which allows a griefer to create an unlimited number of malicious vaults by simply calling `createVault()` with `tokenIdOrAmount = 0`. This will cause a ridiculously high number of malicious vaults to be displayed to actual users, which can lead to users accidently buying a call on this vault which provides 0 value in return. This is damaging to Cally's product image and functionality.

The bug was discovered through manual review and the recommended mitigation step is to add a simple check `require(tokenIdOrAmount > 0, "Amount must be greater than 0");` to the code. This will ensure that the amount of the vault is greater than 0, thus preventing the malicious vaults from being created.

### Original Finding Content

_Submitted by 0xDjango_

A griefer is able to create as many vaults as they want by simply calling `createVault()` with `tokenIdOrAmount = 0`. This will most likely pose problems on the front-end of the Cally protocol because there will be a ridiculously high number of malicious vaults displayed to actual users.

I define these vaults as malicious because it is possible that a user accidently buys a call on this vault which provides 0 value in return. Overall, the presence of zero-amount vaults is damaging to Cally's product image and functionality.

### Proof of Concept

*   User calls `createVault(0,,,,);` with an ERC20 type.
*   There is no validation that `amount > 0`
*   Function will complete successfully, granting the new vault NFT to the caller.
*   Cally protocol is filled with unwanted 0 amount vaults.

### Recommended Mitigation Steps

Add the simple check `require(tokenIdOrAmount > 0, "Amount must be greater than 0");`

**[outdoteth (Cally) confirmed and commented](https://github.com/code-423n4/2022-05-cally-findings/issues/91#issuecomment-1126912009):**
 > This check should only be applied on ERC20 tokens because ERC721 tokens can still have tokenIds that have ID's with a value of 0.

**[outdoteth (Cally) resolved](https://github.com/code-423n4/2022-05-cally-findings/issues/91#issuecomment-1129154306):**
 > this issue is fixed here: https://github.com/outdoteth/cally/pull/12



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Cally |
| Report Date | N/A |
| Finders | 0xDjango |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-cally
- **GitHub**: https://github.com/code-423n4/2022-05-cally-findings/issues/91
- **Contest**: https://code4rena.com/contests/2022-05-cally-contest

### Keywords for Search

`vulnerability`

