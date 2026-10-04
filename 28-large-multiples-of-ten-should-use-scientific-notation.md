---
# Core Classification
protocol: Tigris Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43193
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-12-tigris
source_link: https://code4rena.com/reports/2022-12-tigris
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

protocol_categories:
  - dexes
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[28] Large multiples of ten should use scientific notation.

### Overview

See description below for full details.

### Original Finding Content


Using scientific notation for large multiples of ten will improve code readability.

https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/TradingExtension.sol#L26

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-12-tigris-findings/issues/657#issuecomment-1366191229):**
> [01] Use `.call` instead of `.transfer` to send ether
>
> Low
> 
> [02] Unbounded loop
>
> Low
> 
> [03] Use the safe variant and `ERC721.mint`
>
> Low
> 
> [04] Usage of deprecated chainlink API
>
> Low
> 
> [05] Lack of checks-effects-interactions
>
> Low
> 
> [06] Lack of zero address checks for `Trading.sol` constructor for the variables `_position`, `_gov` and `_pairsContract`
>
> Low
> 
> [07] Add an event for critical parameter changes
>
> Non-Critical
> 
> [08] Missing unit tests
>
> Refactoring
> 
> [09] Pragma float
>
> Non-Critical
> 
> [10] Contract layout and order of functions
>
> Non-Critical
> 
> [11] Use time units directly
>
> Refactoring
> 
> [12] Declare interfaces on separate files
>
> Refactoring
> 
> [13] Constants should be upper case
>
> Refactoring
> 
> [14] Use `private constant` consistently
>
> Non-Critical
> 
> [15] Add a limit for the maximum number of characters per line
>
> Non-Critical
> 
> [16] Declaring a `return named variable` and returning a manual value for the same function
>
> Refactoring
> 
> [17] Lack of spacing in comment
>
> Non-Critical
> 
> [18] Critical changes should use two-step procedure
>
> Non-Critical
> 
> [19] Missing NATSPEC
>
> Non-Critical
> 
> [20] Interchangeable usage of uint and uint256
>
> Non-Critical
> 
> [21] Move require/validation statements to the top of the function when validating input parameters
>
> Refactoring
> 
> [22] Remove console.log import in `Lock.sol`
>
> Non-Critical
> 
> [23] Draft openzeppelin dependencies
>
> Refactoring
> 
> [24] Named imports can be used
>
> Non-Critical
> 
> [25] Imports can be grouped together
>
> Non-Critical
> 
> [26] Constant redefined elsewhere
>
> Refactoring
> 
> [27] Convert repeated validation statements into a function modifier to improve code reusability
>
> Refactoring
> 
> [28] Large multiples of ten should use scientific notation.
>
> Refactoring

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-12-tigris

### Keywords for Search

`vulnerability`

