---
# Core Classification
protocol: Duality Focus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42545
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-04-dualityfocus
source_link: https://code4rena.com/reports/2022-04-dualityfocus
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
  - cdp
  - services
  - yield_aggregator
  - synthetics

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-02] Missing zero-address check in constructors and the setter functions

### Overview

See description below for full details.

### Original Finding Content


Missing checks for zero-addresses may lead to infunctional protocol, if the variable addresses are updated incorrectly.

### Proof of Concept

Navigate to the following all contract functions.

[UniV3LpVault.sol#L59](https://github.com/code-423n4/2022-04-dualityfocus/blob/f21ef7708c9335ee1996142e2581cb8714a525c9/contracts/vault_and_oracles/UniV3LpVault.sol#L59)<br>
[MasterPriceOracle.sol#L37](https://github.com/code-423n4/2022-04-dualityfocus/blob/f21ef7708c9335ee1996142e2581cb8714a525c9/contracts/vault_and_oracles/MasterPriceOracle.sol#L37)<br>
[FlashLoan.sol#L24](https://github.com/code-423n4/2022-04-dualityfocus/blob/f21ef7708c9335ee1996142e2581cb8714a525c9/contracts/vault_and_oracles/FlashLoan.sol#L24)<br>
[UniV3LpVault.sol#L59](https://github.com/code-423n4/2022-04-dualityfocus/blob/f21ef7708c9335ee1996142e2581cb8714a525c9/contracts/vault_and_oracles/UniV3LpVault.sol#L59)<br>

### Recommended Mitigation Steps

Consider adding zero-address checks in the discussed constructors:<br>
require(newAddr != address(0));.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Duality Focus |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-dualityfocus
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-04-dualityfocus

### Keywords for Search

`vulnerability`

