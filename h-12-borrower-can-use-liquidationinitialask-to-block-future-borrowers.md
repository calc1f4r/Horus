---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25807
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/289

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - obront
---

## Vulnerability Title

[H-12] Borrower can use liquidationInitialAsk to block future borrowers

### Overview


This bug report is about a flaw in the code of the Astaria project, a blockchain-based lending platform. The code has a validation to ensure that the potential debt of each borrower on the stack is less than or equal to their liquidationInitialAsk. This is done by iterating through the stack backwards, totaling up the potential debt, and comparing it to each lien's liquidationInitialAsk. However, this validation only applies to the first item on the stack, which means that any future borrows will not be able to pass the validation. This leaves borrowers open to a Denial of Service (DoS) attack, as they will not be able to take out any loans.

The recommended mitigation steps for this bug are to remove all checks on liquidationInitialAsk except for comparing the total potential debt of the entire stack to the liquidationInitialAsk of the lien at position 0. This will ensure that all future borrows can pass the validation, and will protect borrowers from DoS attacks.

### Original Finding Content


<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/LienToken.sol#L471-L489><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/LienToken.sol#L153-L174>

When a new lien is taken (or bought out), one of the validations is to ensure that the `potentialDebt` of each borrower on the stack is less than or equal to their `liquidationInitialAsk`.

    if (potentialDebt > newStack[j].lien.details.liquidationInitialAsk) {
        revert InvalidState(InvalidStates.INITIAL_ASK_EXCEEDED);
      }

In `_appendStack()` and `_buyoutLien()`, this is performed by iterating through the stack backwards, totaling up the `potentialDebt`, and comparing it to each lien's `liquidationInitialAsk`:

    for (uint256 i = stack.length; i > 0; ) {
          uint256 j = i - 1;
          newStack[j] = stack[j];
          if (block.timestamp >= newStack[j].point.end) {
            revert InvalidState(InvalidStates.EXPIRED_LIEN);
          }
          unchecked {
            potentialDebt += _getOwed(newStack[j], newStack[j].point.end);
          }
          if (potentialDebt > newStack[j].lien.details.liquidationInitialAsk) {
            revert InvalidState(InvalidStates.INITIAL_ASK_EXCEEDED);
          }

          unchecked {
            --i;
          }
        }

However, only the first item on the stack has a `liquidationInitialAsk` that matters. When a new auction is started on Seaport, `Router#liquidate()` uses `stack[0].lien.details.liquidationInitialAsk` as the starting price. The other values are meaningless, except in their ability to DOS future borrowers.

### Proof of Concept

*   I set my `liquidationInitialAsk` to be exactly the value of my loan
*   A borrower has already borrowed on their collateral, and the first loan on the stack will determine the auction price
*   When they borrow from me, my `liquidationInitialAsk` is recorded
*   Any future borrows will check that `futureBorrow + myBorrow <= myLiquidationInitialAsk`, which is not possible for any `futureBorrow > 0`
*   The result is that the borrower will be DOS'd from all future borrows

This is made worse by the fact that `liquidationInitialAsk` is not a variable that can justify a refinance, so they'll need to either pay back the loan or find a refinancier who will beat one of the other terms (rate or duration) in order to get rid of this burden.

### Recommended Mitigation Steps

Get rid of all checks on `liquidationInitialAsk` except for comparing the total potential debt of the entire stack to the `liquidationInitialAsk` of the lien at position 0.

**[Picodes (judge) commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/289#issuecomment-1405635921):**
 > The scenario is correct but I don't think it is of high severity at first sight, considering setting `liquidationInitialAsk` too low only exposes the lender to a potential bad debt if the dutch auction settles below its debt

**[Picodes (judge) commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/289#issuecomment-1405638218):**
 > However, it seems from this and other findings that leaving the `liquidationInitialAsk` at the `lien` level has multiple unintended side effects.

**[SantiagoGregory (Astaria) confirmed](https://github.com/code-423n4/2023-01-astaria-findings/issues/289)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | obront |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/289
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

