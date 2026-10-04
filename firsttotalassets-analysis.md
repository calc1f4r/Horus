---
# Core Classification
protocol: Morpho Vaults v2 Fix Review
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62942
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Vaults-v2-fixes-Spearbit-Security-Review-August-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Vaults-v2-fixes-Spearbit-Security-Review-August-2025.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 1.00
financial_impact: low

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Saw-mon and Natalie
  - MiloTruck
---

## Vulnerability Title

firstTotalAssets analysis

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
- `VaultV2.sol#L30-L34`
- `VaultV2.sol#L179`
- `VaultV2.sol#L563-L571`
- `VaultV2.sol#L578`

## Description
In the NatSpec comments we have:
```solidity
/// FIRST TOTAL ASSETS
/// @dev The variable firstTotalAssets tracks the total assets after the first interest accrual of the
/// transaction.
/// @dev Used to implement a mechanism that prevents bypassing relative caps with flashloans.
/// @dev This mechanism can generate false positives on relative cap breach when such a cap is nearly
/// reached, for big deposits that go through the liquidity adapter.
```
The comment is not quite accurate. We have:

```solidity
function accrueInterest() public {
    (uint256 newTotalAssets, ...) = accrueInterestView();
    // ...
    _totalAssets = newTotalAssets.toUint128();
    if (firstTotalAssets == 0) firstTotalAssets = newTotalAssets;
    // ...
    lastUpdate = uint64(block.timestamp);
}

function accrueInterestView() {
    if (firstTotalAssets != 0) return (_totalAssets, 0, 0);
    //...
    return (newTotalAssets, ...);
}
```

And so the transient storage parameter `firstTotalAssets` at any specific point in the call frame tree of a root transaction is either 0 or the first non-zero `newTotalAssets` in the ordered call-tree frame. Thus it could be 0 for a few frames and then as soon as it becomes non-zero it would stay the same value and the calls to `accrueInterestView()` would return early from this point on.

### Example 1
Assume `A0` is a non-zero value. Initially in the beginning of the root tx `T`, one starts with `A0` as the `_totalAssets`, then maybe due to some losses, `newTotalAssets` becomes 0 and thus for all the following call frames if we enter back into `accrueInterestView()` and `accrueInterest()` both `_totalAssets` and `newTotalAssets` stay 0, except somehow we increase `_totalAssets` to a non-zero value. This would only be possible through mint or deposit at this point. After this `firstTotalAssets` would be set to a non-zero value:

```
Atot = A0 → 0 → · · · → 0 → A1 = A1st tot
```

### Example 2
This is like example 1 but at a state where there are no total assets in the vault due to perhaps using a vault that is freshly deployed or perhaps due to the fact that all previous shareholders have exited the vault.

As one can see in both examples, the value of `firstTotalAssets` is not the value new total assets calculated in the first visit of `accrueInterestView()` in the whole call-frame tree of a root transaction. Moreover, until this value is set to a non-zero value the flow in `accrueInterestView()` performs all the operations without exiting early.

```solidity
function allocateInternal(/*...*/) internal {
    // ...
    accrueInterest();
    // ...
    for (...) {
        // ...
        require(/*...*/ ||
            _caps.allocation <= firstTotalAssets.mulDivDown(_caps.relativeCap, WAD),
        // ...);
    }
}
```

The value of `firstTotalAssets` is used to limit the relative cap during an allocation process. Thus due to the above, the correct value is not used in the above examples. The value that should have been used must have been 0.
But currently, the last non-zero value is used.

## Recommendation
One can store a flag in `firstTotalAssets` to indicate that the call-tree flow has gone through the `accrueInterest()` process even though the new total assets could be 0. In all cases, we can set `firstTotalAssets` to store the returned value from `accrueInterestView()` in its [1:255] bits and the first bit would be a flag bit indicating that `accrueInterest()` was called. 

Here is a rough patch:

```diff
diff --git a/src/VaultV2.sol b/src/VaultV2.sol
index c86ec7f..90e68a4 100644
--- a/src/VaultV2.sol
+++ b/src/VaultV2.sol
@@ -518,8 +518,10 @@ contract VaultV2 is IVaultV2 {
 require(_caps.absoluteCap > 0, ErrorsLib.ZeroAbsoluteCap());
 require(_caps.allocation <= _caps.absoluteCap, ErrorsLib.AbsoluteCapExceeded());
 
+ uint256 cleanedFirstTotalAssets = firstTotalAssets » 1;
 require(
- _caps.relativeCap == WAD || _caps.allocation <=
 firstTotalAssets.mulDivDown(_caps.relativeCap, WAD),
- _caps.relativeCap == WAD || _caps.allocation <=
 cleanedFirstTotalAssets.mulDivDown(_caps.relativeCap, WAD),
 ErrorsLib.RelativeCapExceeded()
 );
 }
@@ -561,10 +563,11 @@ contract VaultV2 is IVaultV2 {
/* EXCHANGE RATE FUNCTIONS */
 function accrueInterest() public {
+ if (firstTotalAssets != 0) return;
 (uint256 newTotalAssets, uint256 performanceFeeShares, uint256 managementFeeShares) =
 accrueInterestView();
 emit EventsLib.AccrueInterest(_totalAssets, newTotalAssets, performanceFeeShares,
 managementFeeShares);
 _totalAssets = newTotalAssets.toUint128();
- if (firstTotalAssets == 0) firstTotalAssets = newTotalAssets;
+ if (firstTotalAssets == 0) firstTotalAssets = (newTotalAssets « 1) + 1;
 if (performanceFeeShares != 0) createShares(performanceFeeRecipient, performanceFeeShares);
 if (managementFeeShares != 0) createShares(managementFeeRecipient, managementFeeShares);
 lastUpdate = uint64(block.timestamp);
```

Moreover, one can modify the accrue interest flow even further by strategically returning early if the last timestamp has not changed:

```diff
diff --git a/src/VaultV2.sol b/src/VaultV2.sol
index c86ec7f..12aefde 100644
--- a/src/VaultV2.sol
+++ b/src/VaultV2.sol
@@ -518,8 +518,10 @@ contract VaultV2 is IVaultV2 {
 require(_caps.absoluteCap > 0, ErrorsLib.ZeroAbsoluteCap());
 require(_caps.allocation <= _caps.absoluteCap, ErrorsLib.AbsoluteCapExceeded());
 
+ uint256 cleanedFirstTotalAssets = firstTotalAssets » 1;
 require(
- _caps.relativeCap == WAD || _caps.allocation <=
 firstTotalAssets.mulDivDown(_caps.relativeCap, WAD),
- _caps.relativeCap == WAD || _caps.allocation <=
 cleanedFirstTotalAssets.mulDivDown(_caps.relativeCap, WAD),
 ErrorsLib.RelativeCapExceeded()
 );
 }
@@ -561,10 +563,15 @@ contract VaultV2 is IVaultV2 {
/* EXCHANGE RATE FUNCTIONS */
 function accrueInterest() public {
+ if (firstTotalAssets != 0) return;
+ if (lastUpdate == block.timestamp) {
+ firstTotalAssets = (_totalAssets « 1) + 1;
+ return;
+ }
 (uint256 newTotalAssets, uint256 performanceFeeShares, uint256 managementFeeShares) =
 accrueInterestView();
 emit EventsLib.AccrueInterest(_totalAssets, newTotalAssets, performanceFeeShares,
 managementFeeShares);
 _totalAssets = newTotalAssets.toUint128();
- if (firstTotalAssets == 0) firstTotalAssets = newTotalAssets;
+ if (firstTotalAssets == 0) firstTotalAssets = (newTotalAssets « 1) + 1;
 if (performanceFeeShares != 0) createShares(performanceFeeRecipient, performanceFeeShares);
 if (managementFeeShares != 0) createShares(managementFeeRecipient, managementFeeShares);
 lastUpdate = uint64(block.timestamp);
 @@ -575,8 +582,12 @@ contract VaultV2 is IVaultV2 {
 /// @dev The performance and management fees are taken even if the vault incurs some losses.
 /// @dev Both fees are rounded down, so fee recipients could receive less than expected.
 function accrueInterestView() public view returns (uint256, uint256, uint256) {
- if (firstTotalAssets != 0) return (_totalAssets, 0, 0);
 uint256 elapsed = block.timestamp - lastUpdate;
+
+ if (elapsed == 0 || firstTotalAssets != 0) {
+ return (_totalAssets, 0, 0);
+ }
+ 
 uint256 realAssets = IERC20(asset).balanceOf(address(this));
 for (uint256 i = 0; i < adapters.length; i++) {
 realAssets += IAdapter(adapters[i]).realAssets();
```

## Related Competition Findings:
| Finding # | Title | Notes |
|-----------|-------|-------|
| #770 | Allocators can bypass the relative cap check |  |
| #53 | Malicious allocator can manipulate firstTotalAssets to bypass relative cap policies | and many other dups |
| #817 | Batch deposit calls will fail on a Vaults with Liquidity Adapter |  |
| #855 | FirstTotalAssets Stale Value Enables Relative Cap Bypass in Same-Transaction Deposits |  |
| #847 | Fund Loss via Relative Cap Validation Bypass in allocate() Function of VaultV2 Contract. Concern regarding the specs for relative caps being at WAD | X |
| #803 | Morpho Vault V2: Missing accrueInterest() in deallocateInternal Leads to Potential Accounting Inconsistencies | X |
| #790 | Relative Cap Bypass Through Rounding Error in VaultV2 | Incorrect, should be rejected |
|  | And a few other ones that are not completely related. Search is based on looking for firstTotalAssets when on the finding page and pressing CMD + K. |  |

### Related Test
- `testRelativeCapManipulationProtection`

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho Vaults v2 Fix Review |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, MiloTruck |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Vaults-v2-fixes-Spearbit-Security-Review-August-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Vaults-v2-fixes-Spearbit-Security-Review-August-2025.pdf

### Keywords for Search

`vulnerability`

