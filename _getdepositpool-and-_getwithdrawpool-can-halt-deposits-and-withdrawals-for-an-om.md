---
# Core Classification
protocol: OpalProtocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54315
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007
source_link: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
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
finders_count: 2
finders:
  - 0xJaeger
  - zigtur
---

## Vulnerability Title

_getdepositpool() and _getwithdrawpool() can halt deposits and withdrawals for an om- nipool 

### Overview


The bug report describes an issue with the `_getDepositPool()` and `_getWithdrawPool()` functions in the Omnipool.sol code. These functions are responsible for managing the allocation between pools. However, if all pools reach their target allocation, the functions fail to select a pool for depositing or withdrawing funds. This can result in deposits and withdrawals being halted for a minimum of two weeks. The report recommends removing equality checks in the code to allow for deposits and withdrawals to be distributed equally among all pools.

### Original Finding Content

## Context
- Omnipool.sol#L522
- Omnipool.sol#L620

## Description
The `_getDepositPool()` and `_getWithdrawPool()` functions are responsible for managing the allocation between pools. However, if all pools reach their target allocation, both functions will fail to select a pool for depositing/withdrawing funds, effectively halting all withdrawals and deposits until the target weight of an underlying pool is adjusted.

## Proof of Concept
1. An omnipool is set up with two underlying balancer pools, each with a target weight of 50/50 (for sake of simplicity).
2. User1 deposits 500 tokens, allocated to pool 1.
3. User2 deposits 500 tokens, allocated to pool 2 as pool 1 has reached its target weight.
4. Both pools are now at their target allocations.
5. User3 attempts to deposit funds but encounters an error message from `_getDepositPool()` due to the inability to select a deposit pool index.
6. User4 attempts to withdraw funds but encounters an error message from `_getWithdrawPool()` due to the inability to select a withdrawal pool index.

## Impact
Deposits and withdrawals in an omnipool can be halted for a minimum of two weeks, as this is the official designated period for Liquidity Allocation Votes (LAV) for an omnipool (per documentation). Omnipools are most vulnerable when freshly deployed and beginning to accept deposits, as attackers can easily manipulate pool balances with minimal funds. However, as more time passes and more funds are locked in the omnipool, executing such an attack becomes increasingly difficult.

## Recommendation
Remove the equality checks in both cases to allow users to deposit/withdraw funds within the permitted deviation. This adjustment will enable deposits/withdrawals to be distributed equally among all pools.

### Adjustments
```solidity
// _getDepositPool()
- if (currentAlloc >= targetAllocation_) continue;
+ if (currentAlloc > targetAllocation_) continue;

// _getWithdrawPool()
- if (currentAlloc <= targetAllocation_) continue;
+ if (currentAlloc < targetAllocation_) continue;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | OpalProtocol |
| Report Date | N/A |
| Finders | 0xJaeger, zigtur |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007

### Keywords for Search

`vulnerability`

