---
# Core Classification
protocol: Bond Protocol
chain: everychain
category: uncategorized
vulnerability_type: ownership

# Attack Vector Details
attack_type: ownership
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3525
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/20
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-bond-judging/issues/41

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - ownership

protocol_categories:
  - liquid_staking
  - services
  - cross_chain
  - synthetics
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - xiaoming90
---

## Vulnerability Title

M-1: Transferring Ownership Might Break The Market

### Overview


This bug report is about an issue found by xiaoming90, which was identified as "Transferring Ownership Might Break The Market". The issue occurs when users call the `purchaseBond` function and the market owner transfers the market ownership to someone else. This can cause the market to stop working because the new market owner might not be on the list of whitelisted market owners (`callbackAuthorized` mapping). As such, no one can purchase any bond token, leading to a loss of sale for the market makers. 

The code snippet from BondBaseSDA.sol which is responsible for the issue is located on Lines 379 and 336. The issue is triggered when the `pushOwnership` function is called, which is located at Line 337. It checks if the sender of the message is the markets[id_].owner, and if not, the function reverts.

The recommended solution to this issue is to add an additional validation check to ensure that the new market owner has been whitelisted to use the callback before pushing the ownership. This will ensure that transferring the market ownership will not break the market due to the new market owner not being whitelisted. The code snippet for this solution is provided in the report.

The sponsor acknowledged the issue and provided a message. They added the check for the owner to be whitelisted for a callback on purchase to provide a shutdown mechanism in the event of a malicious callback. The ownership transfer functionality is meant to be used when a callback isn't being used to payout market purchases. This would also require multisig to approve the teller for the capacity in payout tokens.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-bond-judging/issues/41 

## Found by 
xiaoming90

## Summary

After the transfer of the market ownership, the market might stop working, and no one could purchase any bond token from the market leading to a loss of sale for the market makers.

## Vulnerability Detail

The `callbackAuthorized` mapping contains a list of whitelisted market owners authorized to use the callback. When the users call the `purchaseBond` function, it will check at Line 390 if the current market owner is still authorized to use a callback. Otherwise, the function will revert.

https://github.com/sherlock-audit/2022-11-bond/blob/main/src/bases/BondBaseSDA.sol#L379

```solidity
File: BondBaseSDA.sol
379:     function purchaseBond(
380:         uint256 id_,
381:         uint256 amount_,
382:         uint256 minAmountOut_
383:     ) external override returns (uint256 payout) {
384:         if (msg.sender != address(_teller)) revert Auctioneer_NotAuthorized();
385: 
386:         BondMarket storage market = markets[id_];
387:         BondTerms memory term = terms[id_];
388: 
389:         // If market uses a callback, check that owner is still callback authorized
390:         if (market.callbackAddr != address(0) && !callbackAuthorized[market.owner])
391:             revert Auctioneer_NotAuthorized();
```

However, if the market owner transfers the market ownership to someone else. The market will stop working because the new market owner might not be on the list of whitelisted market owners (`callbackAuthorized` mapping). As such, no one can purchase any bond token.

https://github.com/sherlock-audit/2022-11-bond/blob/main/src/bases/BondBaseSDA.sol#L336

```solidity
File: BondBaseSDA.sol
336:     function pushOwnership(uint256 id_, address newOwner_) external override {
337:         if (msg.sender != markets[id_].owner) revert Auctioneer_OnlyMarketOwner();
338:         newOwners[id_] = newOwner_;
339:     }
```

## Impact

After the transfer of the market ownership, the market might stop working, and no one could purchase any bond token from the market leading to a loss of sale for the market makers.

## Code Snippet

https://github.com/sherlock-audit/2022-11-bond/blob/main/src/bases/BondBaseSDA.sol#L379

https://github.com/sherlock-audit/2022-11-bond/blob/main/src/bases/BondBaseSDA.sol#L336

## Tool used

Manual Review

## Recommendation

Before pushing the ownership, if the market uses a callback, implement an additional validation check to ensure that the new market owner has been whitelisted to use the callback. This will ensure that transferring the market ownership will not break the market due to the new market owner not being whitelisted.

```diff
function pushOwnership(uint256 id_, address newOwner_) external override {
    if (msg.sender != markets[id_].owner) revert Auctioneer_OnlyMarketOwner();
+   if (markets[id_].callbackAddr != address(0) && !callbackAuthorized[newOwner_])
+   	revert newOwnerNotAuthorizedToUseCallback();
    newOwners[id_] = newOwner_;
}
```

## Discussion

**Evert0x**

Message from sponsor

----

Acknowledged. We added the check for the owner to be whitelisted for a callback on purchase to provide a shutdown mechanism in the event of a malicious callback. The ownership transfer functionality is meant to be used when a callback isn't being used to payout market purchases. E.g. create a market with an EOA from a script and transfer ownership to a multisig for payouts (would also require multisig to approve the teller for the capacity in payout tokens).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Bond Protocol |
| Report Date | N/A |
| Finders | xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-bond-judging/issues/41
- **Contest**: https://app.sherlock.xyz/audits/contests/20

### Keywords for Search

`Ownership`

