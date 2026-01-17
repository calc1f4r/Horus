---
# Core Classification
protocol: LEND
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58373
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/908
source_link: none
github_link: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/308

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
finders_count: 13
finders:
  - newspacexyz
  - HeckerTrieuTien
  - aman
  - future
  - 0xnegan
---

## Vulnerability Title

H-4: Cross-chain liquidation uses incorrect lToken address, preventing repayment and breaking liquidation flow

### Overview


The liquidation flow is not working properly due to a mistake in using the `lToken` address from one chain when processing on another chain. This causes the borrow position to not be found and the repayment to fail. This issue can lead to inconsistencies in the protocol and undercollateralization. To fix this, the correct `lToken` address should be used in the repayment process.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/308 

## Found by 
0xc0ffEE, 0xnegan, 37H3RN17Y2, HeckerTrieuTien, Phaethon, aman, dimah7, future, ggg\_ttt\_hhh, holtzzx, jokr, newspacexyz, rudhra1749

### Summary

The liquidation flow fails due to the incorrect use of the `lToken` address from Chain A when processing on Chain B. Specifically, after collateral is seized on Chain A, a message is sent back to Chain B using the Chain A version of the `lToken`, causing `findCrossChainCollateral()` to fail. This results in the borrow position not being found, and the repayment on Chain B does not proceed.

### Root Cause

In `CrossChainRouter.sol: 280 _executeLiquidationCore` (on Chain B), the seized collateral is sent to Chain A using:
https://github.com/sherlock-audit/2025-05-lend-audit-contest-sylvarithos/blob/551944cd87d138620b89c11674a92f1dcbe0efbe/Lend-V2/src/LayerZero/CrossChainRouter.sol#L280
```solidity
function _executeLiquidationCore(LendStorage.LiquidationParams memory params) private {
    ...
    // Send message to Chain A to execute the seize
    _send(
        params.srcEid,
        seizeTokens,
        params.storedBorrowIndex,
        0,
        params.borrower,
280     lendStorage.crossChainLTokenMap(params.lTokenToSeize, params.srcEid), // Convert to Chain A version before sending
        msg.sender,
        params.borrowedAsset,
        ContractType.CrossChainLiquidationExecute
    );
}
```

This correctly translates the collateral token into its Chain A version, since that's where the collateral exists.  
However, in `CrossChainRouter.sol: 445 _handleLiquidationSuccess` (on Chain B again), this same `destlToken` is used to find the borrow position:
https://github.com/sherlock-audit/2025-05-lend-audit-contest-sylvarithos/blob/551944cd87d138620b89c11674a92f1dcbe0efbe/Lend-V2/src/LayerZero/CrossChainRouter.sol#L445
```solidity
function _handleLiquidationSuccess(LZPayload memory payload) private {
    // Find the borrow position on Chain B to get the correct srcEid
445    address underlying = lendStorage.lTokenToUnderlying(payload.destlToken);

    // Find the specific collateral record
    (bool found, uint256 index) = lendStorage.findCrossChainCollateral(
        payload.sender,
        underlying,
        currentEid, // srcEid is current chain
        0, // We don't know destEid yet, but we can match on other fields
        payload.destlToken,
        payload.srcToken
    );
```

This fails because `payload.destlToken` refers to the Chain A token address, which does not exist in Chain B's `crossChainCollaterals` mapping.

### Internal Pre-conditions

1. Borrower has active cross-chain borrow from Chain A collateral to Chain B borrow.
2. Liquidator initiates a liquidation on Chain B.
3. Seize token execution completes on Chain A.

### External Pre-conditions

None — this issue arises from internal logic inconsistency between chains.

### Attack Path

1. Liquidator initiates a valid liquidation on Chain B.
2. Chain B sends a message to Chain A to seize collateral.
3. Chain A processes the seize and sends back success payload including `destlToken = Chain A version`.
4. Chain B attempts to finalize repayment using `payload.destlToken`.
5. Since this is not a valid `lToken` on Chain B, `findCrossChainCollateral()` fails.
6. Liquidation repayment is never applied; protocol state remains incorrect.

### Impact

- The liquidation repayment flow is broken.
- The borrower's borrow position remains active even though collateral has been seized.
- The protocol can become inconsistent and undercollateralized.
- Liquidators may receive seized tokens without corresponding debt reduction, leading to systemic accounting errors.

### Mitigation

In `_handleLiquidationSuccess`, should use `payload.srcToken`.

```solidity
- function _handleLiquidationSuccess(LZPayload memory payload) private {
+ function _handleLiquidationSuccess(LZPayload memory payload, uint32 srcEid) private {
    // Find the borrow position on Chain B to get the correct srcEid
-   address underlying = lendStorage.lTokenToUnderlying(payload.destlToken);
+   address lToken = lendStorage.underlyingTolToken(payload.srcToken);

    // Find the specific collateral record
    (bool found, uint256 index) = lendStorage.findCrossChainCollateral(
        payload.sender,
-       underlying,
+       payload.srcToken
-       currentEid, // srcEid is current chain
-       0, // We don't know destEid yet, but we can match on other fields
+       srcEid,
+       currentEid
-       payload.destlToken,
+       lToken
        payload.srcToken
    );
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | LEND |
| Report Date | N/A |
| Finders | newspacexyz, HeckerTrieuTien, aman, future, 0xnegan, Phaethon, dimah7, 0xc0ffEE, jokr, holtzzx, ggg\_ttt\_hhh, rudhra1749, 37H3RN17Y2 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/308
- **Contest**: https://app.sherlock.xyz/audits/contests/908

### Keywords for Search

`vulnerability`

