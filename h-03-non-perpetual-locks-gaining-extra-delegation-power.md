---
# Core Classification
protocol: Hyperstable_2025-03-19
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57824
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-03-19.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-03] Non-perpetual locks gaining extra delegation power

### Overview


This report is about a bug in the `vePeg._delegate()` function. This function requires that the source token (`_from`) is locked before allowing delegation. However, the `_moveAllDelegates()` function ignores this restriction and moves all tokens owned by the user to the new delegate, including non-perpetual locks. This bypasses the intention of only allowing perpetual locks to have delegation power. The recommendation is to either update the `_delegate()` function to accept a delegatee address or to clarify that address-level delegation is the intended design.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The `vePeg._delegate()` function requires that the source token (`_from`) must be perpetually locked before allowing delegation. However, the `_moveAllDelegates()` function ignores this restriction and moves ALL tokens owned by the user to the new delegate, including non-perpetual locks.

This completely bypasses the intention where only perpetual locks should have delegation power.

```solidity
function _delegate(uint256 _from, uint256 _to) internal {
    LockedBalance memory currentLock = locked[_from];
    require(currentLock.perpetuallyLocked == true, "Lock is not perpetual");
    --- SNIPPED ---
    _moveAllDelegates(delegator, currentDelegate, delegatee);
}
```

The `_moveAllDelegates()` function adds ALL tokens owned by the user to the delegation, not just perpetual ones.

```solidity
//File: src/governance/vePeg.sol

function _moveAllDelegates(address owner, address srcRep, address dstRep) internal {
    --- SNIPPED ---

    if (dstRep != address(0)) {
        --- SNIPPED ---

        // Plus all that's owned
        for (uint256 i = 0; i < ownerTokenCount; i++) {
@>          uint256 tId = ownerToNFTokenIdList[owner][i];   //@audit This contains all locks, including non-perpetual locks
            dstRepNew.push(tId);
        }

        --- SNIPPED ---
    }
}
```

## Recommendation

The `_moveTokenDelegates()` function could be used to delegate a specific token to a target user.

However, the `_delegate()` function currently takes token IDs but performs delegation at the address level, creating inconsistency and making the to token ID redundant. If the intended behavior is to delegate a single token’s voting power, it would be clearer to update `_delegate()` to accept a delegatee address and use `_moveTokenDelegates()` accordingly. Otherwise, if address-level delegation is the intended design, the function interface should reflect that to avoid confusion.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperstable_2025-03-19 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-03-19.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

