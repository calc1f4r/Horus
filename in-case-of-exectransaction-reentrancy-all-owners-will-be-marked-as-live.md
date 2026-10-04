---
# Core Classification
protocol: OP Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40522
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/1b6a9e55-49a8-46e9-8272-a849fd60fcc4
source_link: https://cdn.cantina.xyz/reports/cantina_competition_optimism_may2024.pdf
github_link: none

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
finders_count: 8
finders:
  - 99Crits
  - Manuel Polzhofer
  - yixxas
  - 0xa5df
  - J4X98
---

## Vulnerability Title

In case of exectransaction() reentrancy all owners will be marked as live 

### Overview


The LivenessGuard.sol file has a bug on line 134. The issue occurs when a transaction is being processed. The LivenessGuard stores a list of current owners and compares it to a list of owners obtained from SAFE.getOwners(). If there are any new owners, they are marked as alive. However, if there is a reentrancy (when a transaction B is executed while transaction A is still in progress), the list of ownersBefore will be empty when the checkAfterExecution() function is called for the first transaction. This causes all owners to be marked as new and alive. To fix this, the recommendation is to either not allow reentrancy or keep a separate list of ownersBefore for each level of reentrancy.

### Original Finding Content

## LivenessGuard Vulnerability

## Context
**File:** LivenessGuard.sol  
**Line:** 134

## Description
Before a transaction starts (at `checkTransaction()`), the `LivenessGuard` stores the list of current owners in `ownersBefore` (an EnumerableMap). After the transaction is executed (at `checkAfterExecution()`), it compares the list of owners from `SAFE.getOwners()` and `ownersBefore`. Any owner present in `SAFE.getOwners()` but not in `ownersBefore` is assumed to be a new owner and is marked as alive.

The issue arises in the case of transaction reentrancy (when transaction B is executed while transaction A hasn't finished yet). In this scenario, `ownersBefore` will be empty when `checkAfterExecution()` is called for the first transaction. Therefore, the function would assume all owners are new and mark them all as alive.

### Consider the following scenario:
- The safe owners sign transaction A to send an NFT to Alice's contract.
- They also sign another transaction B (e.g., send 5K USDC to Bob).
- Alice modifies her contract so that when `onERC721Received()` is called, it executes transaction B.
- Alice executes transaction A (which then executes transaction B).
- As demonstrated above, when `checkAfterExecution()` is called for transaction A, `ownersBefore` is empty, and all owners are marked as alive.

## Recommendation
Either:
- Don't allow reentrancy (implement a reentrancy lock in `checkTransaction()`).
- Allow reentrancy but maintain a separate list of `ownersBefore` for each level of the reentrancy.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | OP Labs |
| Report Date | N/A |
| Finders | 99Crits, Manuel Polzhofer, yixxas, 0xa5df, J4X98, cyber, lukaprini, KumaCrypto |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_optimism_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/1b6a9e55-49a8-46e9-8272-a849fd60fcc4

### Keywords for Search

`vulnerability`

