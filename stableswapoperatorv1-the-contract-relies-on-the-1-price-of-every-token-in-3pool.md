---
# Core Classification
protocol: Fei Protocol v2 Phase 1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13306
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/09/fei-protocol-v2-phase-1/
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
  - liquid_staking
  - bridge
  - yield
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Sergii Kravchenko
  -  Bernhard Gomig

  -  Martin Ortner
  -  Eli Leers
  -  Heiko Fisch
---

## Vulnerability Title

StableSwapOperatorV1 - the contract relies on the 1$ price of every token in 3pool

### Overview

See description below for full details.

### Original Finding Content

#### Description


To evaluate the price of the 3pool lp token, the built-in `get_virtual_price` function is used. This function is supposed to be a manipulation-resistant pricing function that works under the assumption that all the tokens in the pool are worth 1$. If one of the tokens is broken and is priced less, the price is harder to calculate. For example, Chainlink uses the following function to calculate at least the lower boundary of the lp price:
<https://blog.chain.link/using-chainlink-oracles-to-securely-utilize-curve-lp-pools/>


The withdrawal and the controlled value calculation are always made in DAI instead of other stablecoins of the 3pool. So if DAI gets compromised but other tokens aren’t, there is no way to switch to them.



> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Fei Protocol v2 Phase 1 |
| Report Date | N/A |
| Finders | Sergii Kravchenko,  Bernhard Gomig
,  Martin Ortner,  Eli Leers,  Heiko Fisch |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/09/fei-protocol-v2-phase-1/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

