---
# Core Classification
protocol: Aave Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11613
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/aave-protocol-audit/
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
  - indexes
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M08] Interest may compound unpredictably

### Overview


A bug report has been filed regarding the Aave protocol's loan interest accrual system. Currently, the system uses a simple interest rate model to accrue interest between two relevant transactions. This requirement expands the responsibility of accruing interest into unrelated functions, and the discrepancy between the computed and theoretical interest rates may change unpredictably. To improve predictability and functional encapsulation, it is suggested that the compound interest formula be used instead, or that users be informed that the protocol's interest rates are merely estimations. The Aave team has acknowledged this issue and will evaluate the cost and benefits of switching to a compounded interest rate formula before the mainnet release.

### Original Finding Content

In the Aave protocol, loans’ interest is compounded after relevant “interest accruing” transactions occur (with a difference between fixed-rate and variable-rate loans, reported in [**“[N02] Fixed-rate loans may never compound”**](#n02)). Between two such transactions, the system uses a simple interest rate model.


The code is designed to accrue interest as frequently as possible, but this requirement expands the responsibility of accruing interest into otherwise unrelated functions. Additionally, the size of the discrepancy between the computed and theoretical interest will depend on the volume of transactions being handled by the Aave protocol, which may change unpredictably.


To improve predictability and functional encapsulation, consider calculating interest with the compound interest formula, rather than simulating it through repeated transactions. The [`modexp` precompile](https://medium.com/@rbkhmrcr/precompiles-solidity-e5d29bd428c4) may assist in lowering gas fees. Alternatively, consider informing users that the protocol’s interest rates are merely *estimations* rather than exact rates.


**Update**: *The Aave team acknowledges this issue:*



> 
>  “We acknowledge this issue, as also strictly correlated with N02. As a result, we will evaluate before the mainnet release what will be the implementation cost and the benefits of switching to a compounded interest rate formula, and eventually modify the implementation accordingly.”
> 
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Aave Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/aave-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

