---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40868
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/b695ccbb-9d8b-4cac-be69-706f8c3684e5
source_link: https://cdn.cantina.xyz/reports/cantina_competition_morpho_blue_dec2023.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - sorryNotsorry
  - MiloTruck
  - neumo
  - kankodu
  - pep7siup
---

## Vulnerability Title

Insuﬃcient non existent token check can be weaponised 

### Overview


The bug in SafeTransferLib.sol allows an attacker to withdraw tokens by exploiting the lack of code check for the token address. This can be achieved by frontrunning the token deployment transaction and supplying infinite tokens, which will update the attacker's internal balance. The attacker can then withdraw these tokens when the actual deployment occurs. This bug poses a medium risk and can also be exploited for collateralToken. 

### Original Finding Content

## Context: SafeTransferLib.sol

In `SafeTransferLib.sol`, it doesn't check if the token address provided has code or not. This means calling `SafeTransferFrom` with a token address that does not have any code does not revert.

There are multiple ways of knowing the address where a token will be deployed before it is actually deployed. The easiest way is to frontrun the token deployment transaction. Some tokens use `CREATE2` to deploy the token, which makes it possible as well.

- An attacker can frontrun a token deployment transaction with the following:
  - **CreateMarket** with a legitimate oracle, IRM, and `collateralToken`. Creating a legitimate oracle is not harder before token deployment, as the oracle providers usually take token addresses as input, and it is okay if it doesn't return the correct price before the `loanToken` is added in that oracle provider.
  - Supply infinite tokens, which will succeed and update the internal balance of the attacker because of insufficient non-existent token checks.
  
- Now, the token gets actually deployed and victims deposit actual `loanTokens`. An attacker can withdraw these tokens since, according to internal accounting, they have supplied infinite tokens.

- An attacker can do the same for `collateralToken` if they want to, as `supplyCollateral` is susceptible to the same attack.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | sorryNotsorry, MiloTruck, neumo, kankodu, pep7siup, 3doc, sashik-eth, rvierdiiev, darkbit |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_morpho_blue_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b695ccbb-9d8b-4cac-be69-706f8c3684e5

### Keywords for Search

`vulnerability`

