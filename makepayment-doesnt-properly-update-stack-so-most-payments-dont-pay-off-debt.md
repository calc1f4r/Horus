---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7292
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
rarity_score: 5

# Context Tags
tags:
  - don't_update_state

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

makePayment doesn't properly update stack, so most payments don't pay off debt

### Overview


This bug report is about the LienToken.sol#615-635 code. The bug occurs when a loop is used to make payments. The loop calls the _payment() function with the stack argument and returns the updated stack as newStack. However, the newStack value is not used until the final loop iteration, when it is passed along to the _updateCollateralStateHash() function. This means that the new state hash will be the original state with only the final loan repaid, even though all other loans have had payments made against them.

The recommended solution is to update the loop so that it uses the newStack value instead of the stack argument. Additionally, the _payment() function should return an extra value (elementRemoved) and use that to dictate whether the loop iterates forward or remains at the same index for the next run. Finally, the code should check if newStack changed length instead of returning an elementRemoved bool because of stack too deep error.

### Original Finding Content

## Severity: High Risk

## Context
LienToken.sol#615-635

## Description
As we loop through individual payments in `_makePayment`, each is called with:

```solidity
(newStack, spent) = _payment(
    s,
    stack,
    uint8(i),
    totalCapitalAvailable,
    address(msg.sender)
);
```

This call returns the updated stack as `newStack` but then uses the function argument `stack` again in the next iteration of the loop. The `newStack` value is unused until the final iterate, when it is passed along to `_updateCollateralStateHash()`. This means that the new state hash will be the original state with only the final loan repaid, even though all other loans have actually had payments made against them.

## Recommendation
```solidity
uint256 n = stack.length;
newStack = stack;
for (uint256 i; i < n; ) {
    (newStack, spent) = _payment(
        s,
        - stack,
        newStack,
        uint8(i),
        totalCapitalAvailable,
        address(msg.sender)
    );
```

This fixes the issue above, but the solution must also take into account the fix for the loop within `_payment` outlined here in Issue 134. If you follow the suggestion in that issue, then this function should return an extra value (`elementRemoved`) and use that to dictate whether the loop iterates forward, or remains at the same index for the next run.

The final result should look like:

```solidity
function _makePayment(
    LienStorage storage s,
    Stack[] calldata stack,
    uint256 totalCapitalAvailable
) internal returns (Stack[] memory newStack, uint256 spent) {
    newStack = stack;
    bool elementRemoved = false;
    for (uint256 i; i < newStack.length; ) {
        (newStack, spent, elementRemoved) = _payment(
            s,
            newStack,
            uint8(i),
            totalCapitalAvailable,
            address(msg.sender)
        );
        totalCapitalAvailable -= spent;
        // if stack is updated, we need to stay at the current index
        // to process the new element on the same index.
        if (!elementRemoved) unchecked { ++i; }
        _updateCollateralStateHash(s, stack[0].lien.collateralId, newStack);
    }
}
```

Astaria: Checked if `newStack` changed length instead of returning an `elementRemoved` bool because of stack too deep error.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Don't update state`

