---
# Core Classification
protocol: Optimism Interop
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50079
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/OptimismInterop-Spearbit-Security-Review-February-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/OptimismInterop-Spearbit-Security-Review-February-2025.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Phaze
  - Rvierdiiev
  - RustyRabbit
---

## Vulnerability Title

Transaction prevention through invalid message validation

### Overview


The bug report describes a medium risk issue in the CrossL2Inbox.sol code, specifically on line 49. The problem is that any contract with flow control privileges can use an invalid message hash to invoke the validateMessage function. This causes the Supervisor to mark the transaction as invalid and exclude it from being included in a block. This can allow contracts to block transactions, which is not intended. This can also cause contracts that are safe on other chains to become unsafe on Superchain, which can break EVM equivalence. An example of this issue is during liquidation or cancellation events, where a try/catch callback mechanism is used to notify users, but can also be exploited to prevent liquidations. The report recommends addressing this issue carefully, possibly by adding suspension functionality for message validation, but ensuring it cannot be abused. The report has been acknowledged by OP Labs and Cantina Managed, and will be addressed before the release of CrossL2Inbox.

### Original Finding Content

## Medium Risk Report

## Severity
Medium Risk

## Context
CrossL2Inbox.sol#L49

## Description
Any contract with flow control privileges can invoke the `validateMessage` function using an invalid message hash. Since the Supervisor cannot include such messages on the source chain, it marks these transactions as invalid and excludes them from block inclusion. This allows any contract that receives control flow to block a transaction from occurring. This is typically not the case. If there is a low-level call (or a try/catch block) with a specified amount of gas, it is safe to pass control flow to an unsafe contract and be sure they cannot cause the function to revert.

This can make contracts that are safe on other chains unsafe on Superchain chains, breaking EVM equivalence. For example, this can be problematic during liquidation or cancellation events, where systems sometimes notify users through a try/catch callback mechanism, allowing them to handle this event without the ability to cause transaction reversion. However, this also enables the user to deliberately prevent liquidations by exploiting the message validation process.

## Proof of Concept
1. A liquidator initiates a liquidation against a user's loan position.
2. The lending contract notifies the user's designated contract through a try/catch mechanism.
3. The user's contract responds by calling `validateMessage` with either:
   - A non-existent message hash.
   - An identifier outside the permitted dependency set.
4. The Supervisor flags the transaction as invalid, preventing its inclusion in the block, and permanently avoiding liquidation.

## Recommendation
Addressing this issue requires careful consideration. While providing message validation suspension functionality could provide a solution for contracts that need it, this approach must be carefully designed to prevent abuse. It should also ensure that the suspension mechanism cannot be exploited to bypass validation for genuinely invalid transactions.

## OP Labs
Acknowledged. This will be addressed in a redesign of CrossL2Inbox prior to release.

## Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Optimism Interop |
| Report Date | N/A |
| Finders | Zach Obront, Phaze, Rvierdiiev, RustyRabbit |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/OptimismInterop-Spearbit-Security-Review-February-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/OptimismInterop-Spearbit-Security-Review-February-2025.pdf

### Keywords for Search

`vulnerability`

