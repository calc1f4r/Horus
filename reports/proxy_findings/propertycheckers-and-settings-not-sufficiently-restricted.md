---
# Core Classification
protocol: Sudoswap LSSVM2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18302
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
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
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

PropertyCheckers and Settings not sufficiently restricted

### Overview


This bug report is about a vulnerability in the LSSVMPairFactory.sol contract. The vulnerability is that the contract accepts any address for external contracts which contain critical logic, but there are no checks done on them. This means that the contracts could be updated later, making it difficult to rely on them. The recommendation is to enforce that only contracts created by the factories PropertyCheckerFactory and StandardSettingsFactory can be used. This can be done by keeping a mapping in these contracts which stores all the generated contracts and can then be queried by the factories to verify their origin. This requires that the LSSVMPairFactory is aware of the address of the factories. Both Spearbit and Sudorandom Labs have acknowledged the intended behavior of the factories being open-ended for other types of property checkers or settings.

### Original Finding Content

## Severity: Medium Risk

## Context 
- `LSSVMPairFactory.sol#L120-L201`
- `LSSVMPairFactory.sol#L430-L433`
- `LSSVMPairFactory.sol#L485-L492`
- `StandardSettingsFactory.sol`
- `PropertyCheckerFactory.sol`

## Description
The `LSSVMPairFactory` accepts any address for external contracts that contain critical logic but there are no sanity checks performed on them. The relevant contracts are `_bondingCurve`, `_propertyChecker`, and settings contracts. These contracts could potentially be updated later via a proxy pattern or a `create2/selfdestruct` pattern, making it difficult to fully rely on them.

Both `_propertyChecker` and settings contracts have associated factories: `PropertyCheckerFactory` and `StandardSettingsFactory`. It is straightforward to enforce that only contracts created by the factory can be used. For the `_bondingCurve`s, there is a whitelist that mitigates the risk.

Example functions:

```solidity
function createPairERC721ETH(..., ICurve _bondingCurve, ..., address _propertyChecker, ...) {
    ... // no checks on _bondingCurve and _propertyChecker
}

function toggleSettingsForCollection(address settings, address collectionAddress, bool enable) public {
    ... // no checks on settings
}

function setBondingCurveAllowed(ICurve bondingCurve, bool isAllowed) external onlyOwner {
    bondingCurveAllowed[bondingCurve] = isAllowed;
    emit BondingCurveStatusUpdate(bondingCurve, isAllowed);
}
```

## Recommendation
Enforce that only contracts created by the factories `PropertyCheckerFactory` and `StandardSettingsFactory` can be used. This can be achieved by maintaining a mapping in these contracts that stores all the generated contracts, which can then be queried by the factories to verify their origin.

**Note:** This requires that the `LSSVMPairFactory` is aware of the addresses of the factories.

## Sudorandom Labs
Acknowledged, this is intended behavior. The factories for property checking and settings are designed to be open-ended for future types of property checkers or settings. The property checker factory and settings factory included in the audit are intended to be the recommended ones at the start, but not the only options available (clients may choose to filter pairs to display only those created from the factories).

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap LSSVM2 |
| Report Date | N/A |
| Finders | Gerard Persoon, Shodan, Rajeev, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

