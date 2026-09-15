---
# Core Classification
protocol: Cryptex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40224
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a
source_link: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cccz
  - Patrick Drotleff
---

## Vulnerability Title

Review of TokenExchangeSetIssuer 

### Overview

See description below for full details.

### Original Finding Content

## Audit Summary

## Context
(No context files were provided by the reviewer)

## Description
While this audit was mostly centered around the Cryptex's TCAPv2 repository, a single peripheral contract named **TokenExchangeSetIssuer** was also part of the scope, although part of a different repository (Cryptex's **crypdex**). 

**Crypdex** too is about the creation of Index Tokens, but while TCAPv2 is a synthetic token following the Total Crypto Market Capitalization (divided by 10 billion), this codebase uses SetTokens where a single token is backed by a basket (set) of the actual tokens it is indexing. 

To mint SetTokens, you therefore have to deposit the correct amounts of each of the underlying tokens. This operation is rather tedious to execute without automation, which is where the **TokenExchangeSetIssuer** contract comes in. The goal is for there to be a User Interface where you simply specify the amount of SetTokens you’d like to obtain and provide an allowance for a single asset with which all the tokens belonging to the index will be obtained (under the hood, the contract will make swaps on Uniswap and Paraswap).

Being a peripheral contract means that **TokenExchangeSetIssuer** does not have any special access within the system. Rather, it is a helper contract outside of the protocol that anyone could deploy for themselves, and it would work just fine. In the normal case, it should never hold any user funds for longer than a single transaction, during which a user is calling it to either buy or sell the necessary underlying tokens for obtaining or discarding some amount of SetTokens.

As such, there is practically one critical concern: there may not be any way to make unauthorized `transferFrom()` calls that move funds that **TokenExchangeSetIssuer** has been approved to use. In other words, while the contract should normally never hold funds, it is likely to end up having allowances to many users' funds, and it must not happen that another user makes use of funds that are not their own.

## Recommendations
No critical issues regarding the unauthorized transfer of user-approved funds were found. However, various suggestions around hardening, simplifying, and optimizing the code were given, such as:
- Upgrading Solidity from 0.6.10 to a newer version, preferably 0.8.26, which is the same version used in TCAPv2. While most of the contracts within the crypdex repository use 0.6.10, there shouldn’t be much of an issue using a higher version for a peripheral contract that only interacts with crypdex from "outside."
- This upgrade allows making use of various new language features and bug fixes, but was specifically suggested to avoid using inline assembly, which is notorious for introducing unexpected behavior.
- The manner by which the contract ensured only swap functions of legitimate exchanges could be called appeared unnecessarily restrictive and inefficient. A change to a simpler whitelist-based implementation, specifically restricting the addresses and function signatures being called, was suggested.
- It was noted that under some circumstances (such as using incorrect swap functions or sending funds by accident), funds could accumulate on the contract. The contract’s logic attempted to account for such "stuck" funds, prevent their usage by other users, and allow their rescue by an administrator. However, as these measures can be bypassed, it’s recommended to add appropriate warnings for developers where possible to prevent such accumulations in the first place.

## Cryptex Changes
The Cryptex team made several changes to **TokenExchangeSetIssuer** on PR 6, addressing many of the points raised during the review. The PR is split into 3 commits:

### Summary of Commit 1:
- Reverted to code from an earlier commit, enhancing contract flexibility to allow more exchanges to be whitelisted and invoked in the future.
- Updated the whitelisting logic to create unique identifiers using the target contract address and the 4-byte function selector.
- Added warnings advising users not to send tokens or ETH directly to the contract.
- Included a caution that any residual dust left from buying or selling will not be refunded.

### Summary of Commit 2:
- Added OpenZeppelin v5.0.2 to support Solidity v0.8.26, aliasing it as `@openzeppelin-contracts-5` to differentiate from the version used by core contracts.

### Summary of Commit 3:
- Introduced new interfaces compatible with Solidity v0.8.26.
- Upgraded the Solidity version to v0.8.26 for the **TokenExchangeIssuer**.
- Removed the assembly code introduced in commit 1 for converting bytes to bytesN.
- Leveraged the updated Solidity version to replace require messages with custom error handling.
- Emitted events for the following functions: `whitelistFunctions`, `revokeWhitelistedFunctions`, `addSetTokenIssuanceModules`, and `removeSetTokenIssuanceModules`.

## Suggestions Not Implemented
- Couldn’t find `ReentrancyGuardTransient` in the latest OpenZeppelin version v5.0.2. It only appears in the master branch, so replacing `ReentrancyGuard` with `ReentrancyGuardTransient` was not possible.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Cryptex |
| Report Date | N/A |
| Finders | cccz, Patrick Drotleff |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a

### Keywords for Search

`vulnerability`

