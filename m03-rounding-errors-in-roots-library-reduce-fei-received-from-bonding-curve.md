---
# Core Classification
protocol: Fei Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11003
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fei-protocol-audit/
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

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M03] Rounding errors in Roots library reduce FEI received from bonding curve

### Overview


The Fei Protocol Core library has a bug in its `Roots` library, which implements a `cubeRoot` and `twoThirdsRoot` function. The `twoThirdsRoot` function can have large rounding errors due to the order of operations, resulting in incorrect values. The `threeHalfsRoot` function, which calls the `sqrt` function, also suffers from the same downward bias. This bug is propagated to the `BondingCurve` test for the `Pre Scale` scenario, which checks for the correct amount of FEI sent. The test was written to expect a value of `51529`, but the correct value is `51977`, so the test fails after increasing the accuracy of the `twoThirdsRoot` and `threeHalfsRoot` functions.

The Fei team suggested combining the arithmetic functions and changing the order of operations such that truncating steps are performed last while being mindful of potential overflows. This change reduced the error by 1-2 orders of magnitude on the number ranges in this test class. The bug was fixed in PR#31.

### Original Finding Content

The [`Roots` library](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/utils/Roots.sol#L5) implements a [`cubeRoot` function](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/utils/Roots.sol#L7-L18). It then implements a [`twoThirdsRoot` function](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/utils/Roots.sol#L26-L28) which calls `cubeRoot`. This `twoThirdsRoot` function can have large rounding errors due to the order of operations. The `cubeRoot` function returns a truncated integer, which is then squared in the `twoThirdsRoot` function. The effect is that the `twoThirdsRoot` function is biased downwards, potentially significantly depending on the scale. For example, `twoThirdsRoot(124)` returns 16, whereas the true value is approximately 24.87.


The `Roots` library also implements a [`threeHalfsRoot` function](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/utils/Roots.sol#L21-L23) which suffers the same downward bias caused by incorrect order of operations. This `threeHalfsRoot` function calls the [`sqrt` function](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/utils/Roots.sol#L30-L32) which returns a truncated value. The `threeHalfsRoot` function then raises the truncated value to the power of three. Again, results may significantly deviate from expected values. For example, `threeHalfsRoot(8)` returns 8, whereas the true value is approximately 22.63.


The `threeHalfsRoot` and `twoThirdsRoot` functions are called from the [`_getBondingCurveAmountOut` function](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/bondingcurve/EthBondingCurve.sol#L36-L37), which is used to calculate the `amountOut` for every purchase made before the protocol reaches scale via the [`getAmountOut` function](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/bondingcurve/BondingCurve.sol#L84-L90).


As is, the `twoThirdsRoot` and `threeHalfsRoot` functions scale well, with relatively small percentage errors on big numbers. By changing the order of operations in the [`twoThirdsRoot`](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/utils/Roots.sol#L27) and [`threeHalfsRoot`](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/contracts/utils/Roots.sol#L22) functions, we observed a decrease in the propagated discrepancy in the `BondingCurve` test for the `Pre Scale` scenario which checks for the [`Correct`FEI`sent`](https://github.com/fei-protocol/fei-protocol-core/blob/29aeefddd97f31c7f2a598fb3dca3ef24dc0beb4/test/bondingcurve/EthBondingCurve.test.js#L52-L54). Do note, the test was written to expect a value of `51529`, but the correct value is `51977`, so the test fails after increasing the accuracy of the `twoThirdsRoot` and `threeHalfsRoot` functions.


Consider combining the arithmetic functions and changing the order of operations such that truncating steps are performed last while being mindful of potential overflows.


**Update:** *Fixed in [PR#31](https://github.com/fei-protocol/fei-protocol-core/pull/31). In the words of the Fei team: “This change reduced the error by 1-2 orders of magnitude on the number ranges in this test class”.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Fei Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/fei-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

