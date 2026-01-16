---
# Core Classification
protocol: Mellow Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1146
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-mellow-protocol-contest
source_link: https://code4rena.com/reports/2021-12-mellow
github_link: https://github.com/code-423n4/2021-12-mellow-findings/issues/98

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - yield_aggregator
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[H-03] UniV3Vault.sol#collectEarnings() can be front run

### Overview


The bug report concerns a vulnerability of the UniV3Vault contract, which is a part of the Mellow project. This contract allows a strategy to call the collectEarnings() function to collect fees and reinvest. However, unharvested yields are not included in the tvl() function, making it vulnerable to front-run attacks. A Proof of Concept (POC) is provided to demonstrate how an attacker can exploit this vulnerability. The recommendation is to consider including fees in the tvl() function. The code to calculate fees earned is provided from the G-UNI project.

### Original Finding Content

## Handle

WatchPug


## Vulnerability details

For `UniV3Vault`, it seems that lp fees are collected through `collectEarnings()` callable by the `strategy` and reinvested (rebalanced).

However, in the current implementation, unharvested yields are not included in `tvl()`, making it vulnerable to front-run attacks that steal pending yields.

https://github.com/code-423n4/2021-12-mellow/blob/6679e2dd118b33481ee81ad013ece4ea723327b5/mellow-vaults/contracts/UniV3Vault.sol#L100-L122

https://github.com/code-423n4/2021-12-mellow/blob/6679e2dd118b33481ee81ad013ece4ea723327b5/mellow-vaults/contracts/UniV3Vault.sol#L80-L97

### POC

Given:

- Current `tvl()` is `10 ETH` and `40,000 USDC`;
- Current unclaimed yields (trading fees) is `1 ETH` and `4,000 USDC`;

1. `strategy` calls `collectEarnings()` to collect fees and reinvest;
2. The attacker sends a deposit tx with a higher gas price to deposit `10 ETH` and `40,000 USDC`, take 50% share of the pool;
3. After the transaction in step 1 is packed, the attacker calls `withdraw()` and retrieves `10.5 ETH` and `42,000 USDC`.

As a result, the attacker has stolen half of the pending yields in about 1 block of time.

### Recommendation

Consider including fees in `tvl()`.

For the code to calculate fees earned, please reference `_computeFeesEarned()` in G-UNI project:

https://github.com/gelatodigital/g-uni-v1-core/blob/master/contracts/GUniPool.sol#L762-L806

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mellow Protocol |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-mellow
- **GitHub**: https://github.com/code-423n4/2021-12-mellow-findings/issues/98
- **Contest**: https://code4rena.com/contests/2021-12-mellow-protocol-contest

### Keywords for Search

`vulnerability`

