---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7285
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
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
  - business_logic

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

Inequalities involving liquidationInitialAsk andpotentialDebt can be broken when buyoutLien is called

### Overview


The bug report is about a vulnerability in the LienToken.sol, VaultImplementation.sol, AstariaRouter.sol contracts. When a new lien is committed, it should be checked that the following inequality is true for all j 2 0,   ,n -1: onew+on -1+   +oj Lj. However, when an old lien is replaced with a new one, only the inequality for L0k is checked: L0k A0k ^L0k >0. This could lead to a situation where the auction's starting price L0would not be able to cover all the potential debts even at the beginning of the auction. The recommendation is to loop over jand check the inequalities again:   +oj+1+oj Lj.

### Original Finding Content

## High Risk Security Issue

## Severity
High Risk

## Context
- `LienToken.sol#L102`
- `VaultImplementation.sol#L305`
- `LienToken.sol#L377-L378`
- `LienToken.sol#L427`
- `AstariaRouter.sol#L542`

## Description
When we commit to a new lien, the following gets checked to be true for all \( j=0, 1, 2, \ldots, n-1 \):

\[
o_{new} + o_j + L_j
\]

where:

| Parameter                         | Description                                                 |
|-----------------------------------|-------------------------------------------------------------|
| \( o_i \)                         | `_getOwed(newStack[i], newStack[i].point.end)`            |
| \( o_{new} \)                    | `_getOwed(newSlot, newSlot.point.end)`                     |
| \( n \)                           | `stack.length`                                             |
| \( L_i \)                        | `newStack[i].lien.details.liquidationInitialAsk`          |
| \( L_0 \)                         | `kparams.encumber.lien.details.liquidationInitialAsk`      |
| \( A_0 \)                         | `kparams.position`                                         |
| \( kparams.encumber.amount \)    |                                                           |

In general, we should have:

\[
o_1 + o_j + L_j
\]

But when an old lien is replaced with a new one, we only perform the following checks for \( L_{0k} \):

\[
L_{0k} < A_{0k} \quad \text{and} \quad L_{0k} > 0
\]

Thus, we can introduce:

- \( L_{0k} \geq L_{kor} \)
- \( o_{0k} \leq o_k \) (by pushing the lien duration)

This would break the inequality regarding \( o_i \) and \( L_i \).

If the inequality is broken, for example, if we buy out the first lien in the stack, then if the lien expires and goes into a Seaport auction, the auction's starting price \( L_0 \) would not be able to cover all the potential debts even at the beginning of the auction.

## Recommendation
When `buyoutLien` is called, we need to loop over \( j \) and check the inequalities again:

\[
o_1 + o_j + L_j
\]

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

