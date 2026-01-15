---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7303
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
  - wrong_math
  - validation

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

The lower bound for liquidationInitialAsk for new lines needs to be stricter

### Overview


This bug report is about the LienToken.sol and AstariaRouter.sol contracts. It states that the parameter params.lien.details.liquidationInitialAsk (Lnew) is only compared to params.amount (Anew) which is not sufficient. This parameter should be compared to the aggregated sum of all potential owed amount at the end of each position/lien, which is potentialDebt. The issue is that when the borrower only takes one lien and for this lien liquidationInitialAsk is equal to amount, then at any point during the lien term (maybe very close to the end), the borrower can atomically self liquidate and settle the Seaport auction in one transaction. This way the borrower can skip paying any interest and would receive liquidation fees.

The recommendation is to use a stricter lower bound which is (1 +r(tend - tnow) * Anew = onew * Lnew). This would prevent the borrower from skipping any interest payments.

### Original Finding Content

## Severity: High Risk

## Context
- `LienToken.sol#L376-L381`
- `AstariaRouter.sol#L516`

## Description
`params.lien.details.liquidationInitialAsk` (`Lnew`) is only compared to `params.amount` (`Anew`) whereas in `_appendStack` `newStack[j].lien.details.liquidationInitialAsk` (`Lj`) is compared to `potentialDebt`. 

`potentialDebt` is the aggregated sum of all potential owed amounts at the end of each position/lien. 

So in `_appendStack` we have:

```
onew + on + ... + oj  ≤ Lj
```

Where `oj` is `getOwed(newStack[j], newStack[j].point.end)`, which is the amount for the stack slot plus the potential interest at the end of its term. 

So it would make sense to enforce a stricter inequality for `Lnew`:

```
(1 + r(tend − tnow) / 10^18) Anew = onew ≤ Lnew
```

The big issue regarding the current lower bound is when the borrower only takes one lien and for this lien `liquidationInitialAsk == amount` (or they are close). Then at any point during the lien term (maybe very close to the end), the borrower can atomically self-liquidate and settle the Seaport auction in one transaction. This way the borrower can skip paying any interest (they would need to pay OpenSea fees and potentially royalty fees) and plus they would receive liquidation fees.

## Recommendation
Make sure the following stricter lower bound is used instead:

```
(1 + r(tend − tnow) / 10^18) Anew = onew ≤ Lnew
```

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

`Wrong Math, Validation`

