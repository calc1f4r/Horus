---
# Core Classification
protocol: Tracer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6741
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Tracer-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Tracer-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - derivatives

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Emanuele Ricci
  - Christoph Michel
  - Rusty (f7dd60e9cfad19996d73)
  - Gerard Persoon
---

## Vulnerability Title

Duplicate user payments for long commits when paid from balance

### Overview


This bug report is about an issue in the PoolCommitter.sol file, which is a part of a system that supports ERC20 tokens. The problem is that when minting pool tokens in commit(), the fromAggregateBalance parameter indicates if the user wants to pay from their internal balances or by transferring the tokens. The second if condition is wrong and leads to users having to pay twice when calling commit() with CommitType.LongMint and fromAggregateBalance = true. 

The recommendation is to change the second if condition to only perform the transfer for pool token mints if they have not been already paid from internal balances. The tracer has already fixed the issue in commit 4f2d38f. Spearbit commented that the token transfer was done after the applyCommitment() probably to avoid re-entrancy issues. This behavior is different for non-ERC20 tokens such as ERC777 tokens that give control to the sender and recipient. Tracer responded that their system only needs to support ERC20 tokens and their threat model encompasses this invariant. Spearbit acknowledged this.

### Original Finding Content

## Security Report

## Severity
**High Risk**

## Context
`PoolCommitter.sol#L299-L306`

## Description
When minting pool tokens in `commit()`, the `fromAggregateBalance` parameter indicates if the user wants to pay from their internal balances or by transferring the tokens. The second `if` condition is wrong and leads to users having to pay twice when calling `commit()` with `CommitType.LongMint` and `fromAggregateBalance = true`.

## Recommendation
The second `if` condition should be changed to only perform the transfer for pool token mints if they have not been already paid from internal balances.

```solidity
-if (commitType == CommitType.LongMint || (commitType == CommitType.ShortMint && !fromAggregateBalance)) {
+if ((commitType == CommitType.LongMint || commitType == CommitType.ShortMint) && !fromAggregateBalance) {
    // minting: pull in the quote token from the committer
    // Do not need to transfer if minting using aggregate balance tokens, since the leveraged pool
    // already owns these tokens.
    pool.quoteTokenTransferFrom(msg.sender, leveragedPool, amount);
}
```

## Tracer
Already fixed in commit `4f2d38f`.

## Spearbit
Previously the token transfer was done after the `applyCommitment()` probably to avoid re-entrancy issues. This behavior is different for non-ERC20 tokens such as ERC777 tokens that give control to the sender and recipient. Is the system intended to support these other token standards? Other than that, it is a valid fix.

## Tracer
Our system only needs to support ERC20 tokens and our threat model encompasses this invariant.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | Emanuele Ricci, Christoph Michel, Rusty (f7dd60e9cfad19996d73), Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Tracer-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Tracer-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

