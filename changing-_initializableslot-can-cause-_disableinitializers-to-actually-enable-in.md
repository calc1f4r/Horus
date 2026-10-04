---
# Core Classification
protocol: Coinbase Solady
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45411
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Solady-Coinbase-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Solady-Coinbase-Spearbit-Security-Review-December-2024.pdf
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
finders_count: 4
finders:
  - Kaden
  - Riley Holterhus
  - Optimum
  - Philogy
---

## Vulnerability Title

Changing _initializableSlot() can cause _disableInitializers() to actually enable initializers

### Overview


This bug report discusses a high-risk issue with the _initializableSlot() method in the Initializable.sol file. This method is used for upgradeable contracts with initialization logic. The bug occurs when the method is overridden to return a custom storage slot, which can cause the _disableInitializers() method to enable all initializers instead of disabling them. This can be a serious problem for proxy contract implementations that use Initializable.sol. The recommendation is to ensure that _disableInitializers() works regardless of the _initializableSlot() and to thoroughly test the library with different values. The issue has been fixed in a pull request and verified by Spearbit.

### Original Finding Content

## Security Advisory

## Severity: High Risk

### Context
`Initializable.sol#L157`

### Description
The `_initializableSlot()` method of `Initializable.sol` dictates the storage slot in which the "initialize version" (a `uint64`) and "initialized flag" (`bool`) are to be stored for the purpose of an upgradeable contract with initialization logic.

The method's doc-string states:
> **@dev** Override to return a custom storage slot if required.

Implying that `_initializableSlot()` may return an arbitrary constant, however, the default `_disableInitializers()` method relies on the slot having a particular structure. Specifically, it requires that the top 8 bytes of the slot are `0xffffffffffffffff` because to disable any initializers by setting the "initialize version" to `2**64 - 1` via the `uint64max` variable which is computed from the upper 8 bytes of the slot constant.

This works perfectly fine with the default slot constant `_INITIALIZABLE_SLOT` which has a value of `0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffbf601132`. However, if `_initializableSlot()` were to be overridden to e.g.:

```solidity
function _initializableSlot() internal pure virtual returns (bytes32) {
    return bytes32(uint256(0x4a05e541)); // keccak256("INITIALIZABLE_SLOT")[-4:]
}
```

Returning a seemingly inconspicuous constant would break `_disableInitializers()`, causing it to in fact enable all initializers. This is especially grave as `_disableInitializers()` is typically invoked in the constructors of proxy contract implementations that might use `Initializable.sol` to ensure they are not used as actual contracts, thus protecting all the proxies pointing to it.

### Recommendation
Ensure that `_disableInitializers()` works regardless of `_initializableSlot()`. Generally, for contracts that rely on values that may be overridden by library consumers, the library should be tested with a wide variety of random values.

### Solady
Fixed in PR 1258.

### Spearbit
Verified. The `_disableInitializers()` function now directly declares a constant `0xffffffffffffffff` value and no longer relies on this value being derived from the top 8 bytes of the `_initializableSlot()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Coinbase Solady |
| Report Date | N/A |
| Finders | Kaden, Riley Holterhus, Optimum, Philogy |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Solady-Coinbase-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Solady-Coinbase-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

