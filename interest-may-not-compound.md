---
# Core Classification
protocol: Compound Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11826
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-audit/
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
  - liquidity_manager
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Interest May Not Compound

### Overview


The bug report is about the function `CToken.accrueInterest()` in the Compound Protocol, which currently applies simple interest over the blocks since the last update. This may underestimate the amount of interest that would be calculated if it were compounded every block. To improve predictability and functional encapsulation, the report suggests calculating interest with the compound interest formula and measuring the time between calls to `accrueInterest()` using seconds rather than blocks. This will help keep the interest rate calculation robust against changes to the average blocktime. Additionally, the size of the discrepancy between the computed and theoretical interest will depend on the volume of transactions being handled by the Compound protocol, which may change unpredictably. Finally, the report suggests using the `modexp` precompile to reduce the additional gas requirements.

### Original Finding Content

When calculating interest in [`CToken.accrueInterest()`](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/CToken.sol#L597), simple interest is applied over the blocks since the last update. This will underestimate the amount of interest that would be calculated if it were compounded every block.


The code is designed to accrue interest as frequently as possible, but this requirement expands the responsibility of accruing interest into otherwise unrelated functions. Additionally, the size of the discrepancy between the computed and theoretical interest will depend on the volume of transactions being handled by the Compound protocol, which may change unpredictably.


To improve predictability and functional encapsulation, consider calculating interest with the compound interest formula, rather than simulating it through repeated transactions. Note that the additional gas requirements may be reduced using the [`modexp` precompile](https://medium.com/@rbkhmrcr/precompiles-solidity-e5d29bd428c4). Separately, consider measuring the time between calls to `accrueInterest()` using *seconds* rather than *blocks*. This will help keep the interest rate calculation robust against changes to the average blocktime.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

