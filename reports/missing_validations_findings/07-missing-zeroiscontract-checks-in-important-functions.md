---
# Core Classification
protocol: Venus Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28844
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-09-venus
source_link: https://code4rena.com/reports/2023-09-venus
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[07] Missing zero/isContract checks in important functions

### Overview

See description below for full details.

### Original Finding Content


Low impact, since this requires a bit of an admin error, but some functions which could be more secure using the `_ensureZeroAddress()` currently do not implement this and could lead to issues.

### Proof of Concept

Using the `PrimeLiquidityProvider.sol` in scope as acase study.
Below is the implementation of `_ensureZeroAddress()`

```solidity
function _ensureZeroAddress(address address_) internal pure {
  if (address_ == address(0)) {
    revert InvalidArguments();
  }
}
```

As seen the above is used within protocol as a modifier/function to revert whenever addresses are being passed, this can be seen to be implemented in the `setPrime()` function and others, but that's not always the case and in some instances addresses are not ensured to not be zero.

Additionally, as a security measure an `isContract()` function could be added and used to check for instances where the provided addresses must be valid contracts with code.

### Recommended Mitigation Steps

Make use of `_ensureZeroAddress()` in all instances where addresses could be passed.

If the `isContract()` is going to be implemented then the functionality to be added could look something like this:

```solidity
function isContract(address addr) internal view returns (bool) {
  uint256 size;
  assembly {
    size := extcodesize(addr)
  }
  return size > 0;
}
```

And then, this could be applied to instances where addreses must have byte code.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Venus Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-09-venus
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-09-venus

### Keywords for Search

`vulnerability`

