---
# Core Classification
protocol: BarnBridge Smart Yield Bonds Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10973
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/barnbridge-smart-yield-bonds-audit/
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
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M05] Rounding errors in compound and compound2

### Overview


This bug report highlights an issue with Solidity's truncation when dividing, which can lead to large errors in calculations. The `MathUtils` contract has two functions, `compound` and `compound2`, which both perform truncated divisions in the middle of calculations. As an example, the correct answer for a calculation of compound interest with 100 principal, 1.02e18 rate, and 100 periods is 724.46, but `compound` gives the result 584 and `compound2` gives the result 720.

The BarnBridge team has not addressed this issue, but has stated that they consider the `compound2` function to have a good tradeoff between accuracy, gas cost, and complexity. They will update the `BondModelV1` if they decide this is no longer the case. It is recommended to always perform divisions as late as possible, while also ensuring intermediate results do not overflow.

### Original Finding Content

Due to the fact that Solidity truncates when dividing, performing a division in the middle of a calculation can result in truncated amounts being amplified and these amplifications leading to large errors. In the `MathUtils` contract, the [`compound` function](https://github.com/BarnBridge/BarnBridge-SmartYieldBonds/blob/943df3a8fcd8dd128af3beb0c85a0480c0e95ead/contracts/lib/math/MathUtils.sol#L32) [divides at the end](https://github.com/BarnBridge/BarnBridge-SmartYieldBonds/blob/943df3a8fcd8dd128af3beb0c85a0480c0e95ead/contracts/lib/math/MathUtils.sol#L41) of every iteration of the `while` loop. The more iterations of the `while` loop, the more the result diverges from the true value. While the [`compound2` function](https://github.com/BarnBridge/BarnBridge-SmartYieldBonds/blob/943df3a8fcd8dd128af3beb0c85a0480c0e95ead/contracts/lib/math/MathUtils.sol#L47) is generally more accurate, it also performs this truncated division in the [`odd` case](https://github.com/BarnBridge/BarnBridge-SmartYieldBonds/blob/943df3a8fcd8dd128af3beb0c85a0480c0e95ead/contracts/lib/math/MathUtils.sol#L53) of the while loop.


As an example of how significant these errors can be, consider the calculation of compound interest with 100 principal, 1.02e18 rate, and 100 periods. The correct answer for this calculation is `724.46`. [`compound`](https://github.com/BarnBridge/BarnBridge-SmartYieldBonds/blob/943df3a8fcd8dd128af3beb0c85a0480c0e95ead/contracts/lib/math/MathUtils.sol#L32) gives the result `584`, and [`compound2`](https://github.com/BarnBridge/BarnBridge-SmartYieldBonds/blob/943df3a8fcd8dd128af3beb0c85a0480c0e95ead/contracts/lib/math/MathUtils.sol#L47) gives the result `720`.


Consider updating the calculations to always perform divisions as late as possible, while also ensuring the intermediate results do not overflow.


**Update**: *The BarnBridge team did not address this issue. They stated: “The code uses only the `compound2` function, which we consider to have a good tradeoff between accuracy/gas cost/complexity. Should we decide this is no longer the case, we’ll update the `BondModelV1` which uses the `compound2` function.”*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | BarnBridge Smart Yield Bonds Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/barnbridge-smart-yield-bonds-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

