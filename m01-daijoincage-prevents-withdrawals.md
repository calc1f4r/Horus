---
# Core Classification
protocol: Compound Finance – MCD & DSR Integration
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11577
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-finance-mcd-dsr-integration/
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
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M01] daiJoin.cage prevents withdrawals

### Overview


This report is about a bug in the DSS system. It describes a scenario in which the Maker admins call the function [`cage` in join.sol](https://github.com/makerdao/dss/blob/870d6fddb75090eb177290b1db4e255d2c31075e/src/join.sol#L157), which sets `live = 0`. If this happens, the call to [`daiJoin.exit` within CDaiDelegate’s `doTransferOut` function](https://github.com/compound-finance/compound-protocol/blob/9ea64ddd166a78b264ba8006f688880085eeed13/contracts/CDaiDelegate.sol#L166) will revert upon reaching the [`require` statement on line 169 of join.sol](https://github.com/makerdao/dss/blob/870d6fddb75090eb177290b1db4e255d2c31075e/src/join.sol#L169). This means users would not be able to withdraw their funds.

The bug report suggests that users should be informed of the risk associated with using Compound’s DAI market. It also suggests that a course of action should be taken for the `pauseGuardian` and/or `admin` roles should the `DaiJoin` contract ever be “caged”.

### Original Finding Content

Part of the functionality of the DSS system is the ability of the Maker admins to call the function [`cage` in join.sol](https://github.com/makerdao/dss/blob/870d6fddb75090eb177290b1db4e255d2c31075e/src/join.sol#L157), which sets `live = 0`. If this happens, the call to [`daiJoin.exit` within CDaiDelegate’s `doTransferOut` function](https://github.com/compound-finance/compound-protocol/blob/9ea64ddd166a78b264ba8006f688880085eeed13/contracts/CDaiDelegate.sol#L166) will revert upon reaching the [`require` statement on line 169 of join.sol](https://github.com/makerdao/dss/blob/870d6fddb75090eb177290b1db4e255d2c31075e/src/join.sol#L169). Users would not be able to withdraw their funds.


Consider informing users of the risk associated with using Compound’s DAI market. Also consider a course of action for the `pauseGuardian` and/or `admin` roles should the `DaiJoin` contract ever be “caged”.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Finance – MCD & DSR Integration |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-finance-mcd-dsr-integration/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

