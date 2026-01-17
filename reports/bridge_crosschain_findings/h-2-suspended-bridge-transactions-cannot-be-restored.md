---
# Core Classification
protocol: SYMMIO v0.83 Update Contest
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34715
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/427
source_link: none
github_link: https://github.com/sherlock-audit/2024-06-symmetrical-update-2-judging/issues/9

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
finders_count: 2
finders:
  - slowfi
  - xiaoming90
---

## Vulnerability Title

H-2: Suspended bridge transactions cannot be restored

### Overview


The report identifies a vulnerability in the code of a bridge transaction system where suspended transactions cannot be restored. This results in assets being stuck and unable to be reclaimed by the bridge service providers. The vulnerability lies in the code that deposits invalid assets into an account that cannot be updated, causing the restoration transaction to always fail. This can lead to loss of assets. The recommended solution is to implement a setter function for the affected variable. The issue has been fixed by the protocol team in a recent update. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-06-symmetrical-update-2-judging/issues/9 

## Found by 
slowfi, xiaoming90
## Summary

Suspended bridge transactions cannot be restored. As a result, the assets will be stuck, and bridge service providers cannot reclaim the assets they have transferred to the users from the protocol. 

## Vulnerability Detail

In Line 90 below, when restoring the bridge transaction, the invalid assets will be deposited into the account of `bridgeLayout.invalidBridgedAmountsPool`. These invalid assets can be withdrawn from this account/pool at a later time.

Per Line 88 below, if the ``bridgeLayout.invalidBridgedAmountsPool`` is zero, the `restoreBridgeTransaction` transaction will revert.

However, within the codebase, there is no way to update the `bridgeLayout.invalidBridgedAmountsPool` value. Thus, the `bridgeLayout.invalidBridgedAmountsPool` will always be zero. The `restoreBridgeTransaction` transaction will always revert and there is no way to restore a suspended bridge transaction. As a result, the assets will be stuck, and bridge service providers will not be able to reclaim the assets they have transferred to the users from the protocol.

https://github.com/sherlock-audit/2024-06-symmetrical-update-2/blob/main/protocol-core/contracts/facets/Bridge/BridgeFacetImpl.sol#L88

```solidity
File: BridgeFacetImpl.sol
83: 	function restoreBridgeTransaction(uint256 transactionId, uint256 validAmount) internal {
84: 		BridgeStorage.Layout storage bridgeLayout = BridgeStorage.layout();
85: 		BridgeTransaction storage bridgeTransaction = bridgeLayout.bridgeTransactions[transactionId];
86: 
87: 		require(bridgeTransaction.status == BridgeTransactionStatus.SUSPENDED, "BridgeFacet: Invalid status");
88: 		require(bridgeLayout.invalidBridgedAmountsPool != address(0), "BridgeFacet: Zero address");
89: 
90: 		AccountStorage.layout().balances[bridgeLayout.invalidBridgedAmountsPool] += (bridgeTransaction.amount - validAmount);
91: 		bridgeTransaction.status = BridgeTransactionStatus.RECEIVED;
92: 		bridgeTransaction.amount = validAmount;
93: 	}
```

## Impact

Loss of assets. The assets will be stuck, and bridge service providers cannot reclaim the assets they have transferred to the users from the protocol. 

## Code Snippet

https://github.com/sherlock-audit/2024-06-symmetrical-update-2/blob/main/protocol-core/contracts/facets/Bridge/BridgeFacetImpl.sol#L88

## Tool used

Manual Review

## Recommendation

Implement a setter function for the `invalidBridgedAmountsPool` variable.

```diff
+ function updateInvalidBridgedAmountsPool(address poolAddress) external onlyRole(LibAccessibility.DEFAULT_ADMIN_ROLE) {
+  BridgeStorage.layout().invalidBridgedAmountsPool = poolAddress;
+ }
```



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/SYMM-IO/protocol-core/pull/46


**sherlock-admin2**

The Lead Senior Watson signed off on the fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | SYMMIO v0.83 Update Contest |
| Report Date | N/A |
| Finders | slowfi, xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-06-symmetrical-update-2-judging/issues/9
- **Contest**: https://app.sherlock.xyz/audits/contests/427

### Keywords for Search

`vulnerability`

