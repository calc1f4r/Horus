---
# Core Classification
protocol: FactoryDAO
chain: everychain
category: uncategorized
vulnerability_type: transferfrom_vs_safetransferfrom

# Attack Vector Details
attack_type: transferfrom_vs_safetransferfrom
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2246
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-factorydao-contest
source_link: https://code4rena.com/reports/2022-05-factorydao
github_link: https://github.com/code-423n4/2022-05-factorydao-findings/issues/22

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
  - transferfrom_vs_safetransferfrom

protocol_categories:
  - dexes
  - cdp
  - yield
  - rwa
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 15
finders:
  - danb
  - VAD37
  - wuwe1
  - CertoraInc
  - MaratCerby
---

## Vulnerability Title

[M-03] safeTransferFrom is recommended instead of transfer (1)

### Overview


This bug report is about a vulnerability in the ERC20 standard, which allows transferF functions of some contracts to return either bool or nothing. This could lead to funds stuck in the contract without the possibility to retrieve them. A proof of concept is provided in the report.

The recommended mitigation step is to use the safeTransferFrom of SafeERC20.sol instead. This is a contract from the OpenZeppelin library which provides a secure way to transfer tokens. This library is available on Github and can be used to replace the vulnerable transferF function.

### Original Finding Content

_Submitted by MaratCerby, also found by berndartmueller, broccolirob, CertoraInc, cryptphi, danb, gzeon, horsefacts, hyh, joestakey, leastwood, throttle, VAD37, wuwe1, and z3s_

ERC20 standard allows transferF function of some contracts to return bool or return nothing.<br>
Some tokens such as USDT return nothing.<br>
This could lead to funds stuck in the contract without possibility to retrieve them.<br>
Using safeTransferFrom of SafeERC20.sol is recommended instead.<br>

### Proof of Concept

<https://github.com/OpenZeppelin/openzeppelin-contracts/blob/4a9cc8b4918ef3736229a5cc5a310bdc17bf759f/contracts/token/ERC20/utils/SafeERC20.sol>

**[illuzen (FactoryDAO) commented](https://github.com/code-423n4/2022-05-factorydao-findings/issues/22#issuecomment-1121974704):**
 > We support ERC20 contracts, not SafeERC20. Contracts that do not conform to the standard are not supported.

**[illuzen (FactoryDAO) confirmed and resolved](https://github.com/code-423n4/2022-05-factorydao-findings/issues/22#issuecomment-1145530282):**
 > https://github.com/code-423n4/2022-05-factorydao/pull/2



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | FactoryDAO |
| Report Date | N/A |
| Finders | danb, VAD37, wuwe1, CertoraInc, MaratCerby, leastwood, joestakey, throttle, gzeon, berndartmueller, broccolirob, z3s, cryptphi, hyh, horsefacts |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-factorydao
- **GitHub**: https://github.com/code-423n4/2022-05-factorydao-findings/issues/22
- **Contest**: https://code4rena.com/contests/2022-05-factorydao-contest

### Keywords for Search

`transferFrom vs safeTransferFrom`

