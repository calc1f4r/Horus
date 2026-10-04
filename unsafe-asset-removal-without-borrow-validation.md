---
# Core Classification
protocol: CAP Labs Covered Agent Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61529
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
github_link: none

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
finders_count: 3
finders:
  - Benjamin Samuels
  - Priyanka Bose
  - Nicolas Donboly
---

## Vulnerability Title

Unsafe asset removal without borrow validation

### Overview


The report discusses a high difficulty bug in a lending protocol's `removeAsset` function. This function allows an asset to be removed from the vault's list without checking for any active loans. This can cause problems when borrowers try to repay their loans for the removed asset, as the asset is no longer available. The report recommends adding a validation check to prevent this issue and developing thorough tests for future asset management operations.

### Original Finding Content

## Vulnerability Report

## Difficulty: High

## Type: Configuration

## Description
The `removeAsset` function in the Vault contract allows removing an asset from the vault’s asset list without checking for outstanding borrows. This can lead to potential system inconsistencies and unexpected behavior in the lending protocol.

```solidity
function removeAsset(IVault.VaultStorage storage $, address _asset) external {
    address[] memory cachedAssets = $.assets;
    uint256 length = cachedAssets.length;
    bool removed;
    for (uint256 i; i < length; ++i) {
        if (_asset == cachedAssets[i]) {
            $.assets[i] = cachedAssets[length - 1];
            $.assets.pop();
            removed = true;
            break;
        }
    }
    if (!removed) revert AssetNotSupported(_asset);
    emit RemoveAsset(_asset);
}
```

*Figure 6.1: Code snippet of the function `removeAsset` in the VaultLogic contract (contracts/vault/libraries/VaultLogic.sol#L192-L208)*

As shown in figure 6.1, the current implementation of removing an asset does not validate whether the asset has any outstanding borrows before removal. This can create an issue where an asset with active borrows is removed from the vault. As a result, subsequent operations, such as repayments for the removed asset, could become impossible since repayment functions rely on the existence of an asset in the vault system.

## Exploit Scenario
An admin mistakenly removes an asset from the vault while there are active loans. Borrowers attempt to repay their loans for this asset. Repayment fails because the asset is no longer in the vault’s asset list. As a result, borrowers’ funds become effectively locked, and they are unable to clear their debt.

## Recommendations
- **Short term:** Add a validation check to ensure that total borrows for the asset are zero before removal.
- **Long term:** Develop a comprehensive suite of unit tests that rigorously validate the asset removal process, ensuring that assets with outstanding borrows cannot be removed and that the system maintains its integrity during asset management operations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | CAP Labs Covered Agent Protocol |
| Report Date | N/A |
| Finders | Benjamin Samuels, Priyanka Bose, Nicolas Donboly |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

