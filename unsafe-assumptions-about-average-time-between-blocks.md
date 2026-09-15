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
solodit_id: 11831
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

Unsafe Assumptions About Average Time Between Blocks

### Overview


This bug report concerns the current implementation of the protocol, which uses blocks rather than seconds to measure time between interest accruals. This makes the protocol highly sensitive to changes in the average time between Ethereum blocks, which can change significantly due to the difficulty bomb or the transition to Serenity. This difference between the actual time between blocks and the assumed time causes proportional differences between the intended interest rates and the actual interest rates. The bug report suggests refactoring the implementation to use seconds rather than blocks to measure the time between accruals. This would decouple the interest rate model from Ethereum’s average blocktime, and errors would not be cumulative.

### Original Finding Content

The current implementation of the protocol uses *blocks* rather than *seconds* to measure time between interest accruals. This makes the implementation highly sensitive to changes in the average time between Ethereum blocks.


On [line 30 of `WhitePaperInterestRateModel.sol`](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/WhitePaperInterestRateModel.sol#L30) it is implicitly assumed that the time between blocks is 15 seconds. However, the average time between blocks can change dramatically.


For example, the average time between blocks may increase by significant factors due to the difficulty bomb or decrease by significant factors during the transition to Serenity.


The difference between the actual time between blocks and the assumed time between blocks causes proportional differences between the intended interest rates and the actual interest rates.


While it is possible for the admin to combat this by adjusting the interest rate model when the average time between blocks changes, such adjustments are manual and happen only after-the-fact. Errors in blocktime assumptions are cumulative, and fixing the model after-the-fact does not make users whole – it only prevents incorrect interest calculations moving forward (until the next change in blocktime).


Consider refactoring the implementation to use *seconds* rather than *blocks* to measure the time between accruals. While `block.timestamp` can be manipulated by miners within a narrow window, these errors are small and, importantly, are not cumulative. This would decouple the interest rate model from Ethereum’s average blocktime.

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

