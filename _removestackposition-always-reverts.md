---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: broken_loop

# Attack Vector Details
attack_type: broken_loop
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7293
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
rarity_score: 3

# Context Tags
tags:
  - broken_loop

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

_removeStackPosition() always reverts

### Overview


This bug report is about the function removeStackPosition() in the LienToken.sol file. It has a high risk severity. The problem is that the function calls for an index beyond its length, which causes it to always revert. Additionally, the intention of the function is to delete the element from the stack at the given index position and shift the other elements to the left, however, the loop index is incremented which results in newStack[position] being empty and the shift of other elements not happening.

The recommendation is to apply a diff to the code to fix the issue. The diff removes the unchecked statement and changes the loop index to length-1 instead of length. The issue should also be considered in conjunction with another issue that makePayment doesn't properly update the stack, which causes most payments not to pay off debt. This issue has been fixed in Pull Requests 202 and 265 and has been verified.

### Original Finding Content

## Security Report

## Severity
**High Risk**

## Context
`LienToken.sol#L823-L828`

## Description
The function `removeStackPosition()` always reverts since it calls the stack array for an index beyond its length:

```solidity
for (i; i < length; ) {
unchecked {
newStack[i] = stack[i + 1];
++i;
}
}
```

Notice that for `i == length - 1`, `stack[length]` is called. This reverts since length is the length of the stack array.

Additionally, the intention is to delete the element from the stack at `indexPosition` and shift left the elements appearing after this index. However, an additional increment to the loop index `i` results in `newStack[position]` being empty, and the shift of other elements doesn't happen.

## Recommendation
Apply the following diff to `LienToken.sol#L823-L831`:

```diff
- unchecked {
- ++i;
- }
- for (i; i < length; ) {
+ for (i; i < length - 1; ) {
unchecked {
newStack[i] = stack[i + 1];
++i;
}
}
```

## Note
This issue has to be considered in conjunction with the following issue:
- `makePayment` doesn't properly update stack, so most payments don't pay off debt.

### Astaria
Fixed in PRs 202 and 265.

### Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Broken Loop`

