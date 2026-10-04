---
# Core Classification
protocol: Knox Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3394
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/4
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-knox-judging/issues/26

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

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - ctf\_sec
---

## Vulnerability Title

M-7: processAuction() in VaultAdmin.sol can be called multiple times by keeper if the auction is canceled.

### Overview


This bug report is about an issue with processAuction() in VaultAdmin.sol, which is a part of the Knox protocol. It was found by ctf_sec and it states that the processAuction() function can be called multiple times by the keeper if the auction is canceled. This could lead to the withdrawal lock being released multiple times, allowing users to withdraw funds multiple times, and the total assets held in the vault could be reduced. It also allows for performance fees to be collected multiple times. Manual review was used to find the issue.

The recommendation is to add a guard to prevent multiple calls of the processAuction() function. This was discussed by 0xCourtney and Evert0x, with 0xCourtney stating that the Keeper is an EOA owned/controlled by the protocol team and therefore considered trusted, and Evert0x asking if it is a valid use case for the processAuction() function to be called multiple times. 0xCourtney then stated that the function should only be called once, and they would add a guard to prevent multiple calls.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-knox-judging/issues/26 

## Found by 
ctf\_sec

## Summary

processAuction() in VaultAdmin.sol can be called multiple times by keeper if the auction is canceled.

## Vulnerability Detail

processAuction() in VaultAdmin.sol can be called multiple times by keeper, the code below would execute more than one times
if the auction is canceled.

https://github.com/sherlock-audit/2022-09-knox/blob/main/knox-contracts/contracts/vault/VaultAdmin.sol#L259-L280

because it is the line of code inside the function processAuction in VaultAdmin.sol below that can change the auction status to PROCESSED. 

https://github.com/sherlock-audit/2022-09-knox/blob/main/knox-contracts/contracts/vault/VaultAdmin.sol#L326

this code only runs when the auction is finalized, it not finalized, the auction is in Canceled State and 

```solidity
   bool cancelled = l.Auction.isCancelled(lastEpoch);
        bool finalized = l.Auction.isFinalized(lastEpoch);

        require(
            (!finalized && cancelled) || (finalized && !cancelled),
            "auction is not finalized nor cancelled"
        );
```

would always pass because the auction is in cancel state.

## Impact

Why the processAuction should not be called multiple times?

In the first time it is called, the withdrawal lock is released so user can withdraw fund,

```solidity
 // deactivates withdrawal lock
  l.auctionProcessed = true;
```

then if we called again, the lastTotalAssets can be updated multiple times.

```solidity
        // stores the last total asset amount, this is effectively the amount of assets held
        // in the vault at the start of the auction
        l.lastTotalAssets = _totalAssets();
```

the total asset can be lower and lower because people are withdrawing their fund.

then when _collectPerformanceFee is called, the performance may still be collected

https://github.com/sherlock-audit/2022-09-knox/blob/main/knox-contracts/contracts/vault/VaultInternal.sol#L513-L530

## Code Snippet

## Tool used

Manual Review

## Recommendation

We recommend the project lock the epoch and make it impossible for keeper to call the processAuction again. 

## Discussion

**0xCourtney**

The `Keeper` is an EOA owned/controlled by the protocol team and therefore considered trusted.

**Evert0x**

@0xCourtney as there are require statements based on the auction state, is it a valid use case that `processAuction()` get's called multiple times (by the keeper)? If not I can see the argument for the missing check.

**0xCourtney**

No, this function should only be called once. We'll add a guard to prevent multiple calls.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Knox Finance |
| Report Date | N/A |
| Finders | ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-knox-judging/issues/26
- **Contest**: https://app.sherlock.xyz/audits/contests/4

### Keywords for Search

`vulnerability`

