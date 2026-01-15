---
# Core Classification
protocol: Index Fun Order Book
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63705
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1197
source_link: none
github_link: https://github.com/sherlock-audit/2025-10-index-fun-order-book-contest-judging/issues/366

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
finders_count: 5
finders:
  - typicalHuman
  - 0xeix
  - desaperh
  - PUSH0
  - al0x23
---

## Vulnerability Title

M-5: Lack of Emergency Market Invalidation Mechanism

### Overview


The report discusses a bug in the 2025-10-index-fun-order-book-contest-judging project, where the Protocol Owner or Emergency Resolver is unable to invalidate an active market. This can lead to a permanent loss of collateral for all market participants if the market outcome cannot be determined due to factors such as source API failure or real-world event cancellation. The root cause of the bug is identified as a design choice that does not account for scenarios where a valid outcome cannot be determined. The bug can be exploited by canceling a real-world event associated with the market, causing the market to remain unresolved and resulting in a loss of all locked collateral for market participants. The report suggests adding a mechanism to mark a market as "invalid" or "canceled" and allowing users to reclaim their collateral in such cases. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-10-index-fun-order-book-contest-judging/issues/366 

This issue has been acknowledged by the team but won't be fixed at this time.

## Found by 
0xeix, PUSH0, al0x23, desaperh, typicalHuman

### Summary

The Protocol Owner or Emergency Resolver cannot unilaterally invalidate an active market, which will cause a permanent lock of collateral for all market participants if the market outcome is impossible to determine (e.g., source API failure, question ambiguity, or real-world event cancellation).

### Root Cause

https://github.com/sherlock-audit/2025-10-index-fun-order-book-contest/blob/main/orderbook-solidity/src/Market/MarketController.sol#L745

The design choice to only allow resolution via MarketResolver.resolveMarketEpoch (or MarketController.emergencyResolveMarket) is a mistake as it does not account for scenarios where a valid outcome or merkle root cannot be determined.
In MarketResolver.sol:116, the _resolveMarketEpochInternal function only accepts a merkleRoot as input, requiring a definitive outcome.
In MarketController.sol:413, the emergencyResolveMarket function similarly requires a merkleRoot.
There is no function to set a state variable that designates a market as "invalid" or "canceled," which would allow users to reclaim their collateral.

### Internal Pre-conditions

MarketResolver needs to set oracle and emergencyResolver to be addresses other than address(0).

Market needs to be created by MarketController via Market.createMarket() in Market.sol:98.

Collateral needs to be locked in the Vault via Vault.lockCollateral() from user interactions.

### External Pre-conditions

The real-world event associated with the questionId is canceled, or the data source (off-chain service providing the Merkle Root) fails permanently.

### Attack Path

A real-world event associated with questionId is canceled, permanently delaying, or deemed unresolvable.

The Oracle cannot provide a valid merkleRoot because no outcome has occurred.

The Emergency Resolver calls MarketController.emergencyResolveMarket() but cannot provide a valid merkleRoot (if they submit a bytes32(0) root, the transaction reverts due to require(merkleRoot != bytes32(0), "Invalid merkle root"); in MarketResolver.sol:123).

Without a valid merkleRoot or an invalidation flag, the Condition ID remains unresolved (isResolved[conditionId] is false).

Market Participants call MarketController.claimWinnings() in MarketController.sol:349.

The transaction reverts due to require(marketResolver.getResolutionStatus(conditionId), "Market not resolved"); in MarketController.sol:357.

### Impact

The Market Participants suffer an indefinite, potentially permanent loss of all locked collateral in the Vault for that specific conditionId. This could equate to a 100% loss of all staked funds for that market if the resolution source becomes permanently unavailable.

### PoC

Non Applicable ( Lack of mechanism)

### Mitigation

Add a bool isInvalidated mapping in MarketResolver.sol and a corresponding invalidateMarket(bytes32 questionId, uint256 epoch) function callable by onlyEmergencyResolver.

Modify the claimWinnings and batchClaimWinnings functions in MarketController.sol to allow users to burn their position tokens (all outcomes) and reclaim 100% of their proportional locked collateral from the Vault if the market is marked as invalidated.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Index Fun Order Book |
| Report Date | N/A |
| Finders | typicalHuman, 0xeix, desaperh, PUSH0, al0x23 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-10-index-fun-order-book-contest-judging/issues/366
- **Contest**: https://app.sherlock.xyz/audits/contests/1197

### Keywords for Search

`vulnerability`

