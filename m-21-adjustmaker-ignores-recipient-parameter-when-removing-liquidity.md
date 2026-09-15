---
# Core Classification
protocol: Ammplify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63200
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1054
source_link: none
github_link: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/492

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
finders_count: 15
finders:
  - panprog
  - maigadoh
  - shieldrey
  - SanketKogekar
  - glitch-Hunter
---

## Vulnerability Title

M-21: adjustMaker ignores recipient parameter when removing liquidity

### Overview


This bug report discusses an issue found in the adjustMaker function of the Ammplify protocol. The function takes a recipient parameter, which according to the NatSpec, should define who receives tokens when removing liquidity. However, the code always sends tokens to the msg.sender, even when removing liquidity, meaning the recipient parameter is not used at all. This creates a mismatch between the specification and implementation, which can cause accounting problems or failed integrations. The bug can be mitigated by updating the function to use the recipient parameter when removing liquidity. The protocol team has fixed this issue in a recent pull request.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/492 

## Found by 
0x37, 0xHexed, 5am, BoyD, Edoscoba, SanketKogekar, blockace, devAnas, glitch-Hunter, maigadoh, makarov, panprog, shieldrey, t.aksoy, theholymarvycodes

### Summary

The adjustMaker function takes a recipient parameter. The NatSpec says this should define who gets the tokens when removing liquidity.

But in the code, the function always sends tokens to msg.sender, even when removing liquidity. This means the recipient parameter is not used at all.

### Root Cause

The function adjustMaker in MakerFacet takes a recipient parameter that, according to the NatSpec, should define who receives tokens when removing liquidity.`

`/// @param recipient Who receives tokens when removing liq. Does not get used when adding liq.`

However, the implementation always uses msg.sender for settlement, regardless of whether liquidity is being added or removed:

https://github.com/sherlock-audit/2025-09-ammplify/blob/main/Ammplify/src/facets/Maker.sol#L89

```solidity
RFTLib.settle(msg.sender, tokens, balances, rftData);
```

This creates a mismatch between specification and implementation. In particular, when removing liquidity, tokens are always credited back to the position owner (msg.sender), not the intended recipient.

### Internal Pre-conditions

- The caller owns the maker position (asset.owner == msg.sender).
- The liquidity type is MAKER or MAKER_NC.


### External Pre-conditions

When calling adjustMaker specifying a recipient address expecting to receive removed liquidity.

### Attack Path

1. Alice opens a maker position.
2. Alice calls adjustMaker with recipient = Bob.
3. Liquidity is removed.
4. Tokens are sent to Alice (msg.sender) instead of Bob.
5. The system relying on recipient for accounting or further operations now behaves incorrectly.

### Impact

This breaks the function’s documented behavior and can cause accounting problems or failed integrations.

### PoC

n/a

### Mitigation

Update the function so that:

When adding liquidity → keep using msg.sender (since they are depositing).

When removing liquidity → use recipient (so the tokens go where the caller specified).

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/itos-finance/Ammplify/pull/31






### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Ammplify |
| Report Date | N/A |
| Finders | panprog, maigadoh, shieldrey, SanketKogekar, glitch-Hunter, blockace, 0xHexed, makarov, 0x37, t.aksoy, theholymarvycodes, Edoscoba, devAnas, 5am, BoyD |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/492
- **Contest**: https://app.sherlock.xyz/audits/contests/1054

### Keywords for Search

`vulnerability`

