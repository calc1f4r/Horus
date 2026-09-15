---
# Core Classification
protocol: Foundry DeFi Stablecoin CodeHawks Audit Contest
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34433
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cljx3b9390009liqwuedkn0m0
source_link: none
github_link: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin

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
finders_count: 3
finders:
  - 0xSwahili
  - Bauer
  - pina
---

## Vulnerability Title

Liquidators can be front-run to their loss

### Overview


This bug report discusses a potential issue with the DSC liquidators, which could result in them losing some of their expected collateral tokens. This is due to the possibility of oracle price manipulations and MEV front-run attacks. The impact of this bug is that liquidators may not receive the full amount of collateral tokens they were expecting. The report recommends adding a new input parameter to the liquidate function and implementing a check to prevent this issue from occurring. The report was created through manual review.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/DSCEngine.sol#L229">https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/DSCEngine.sol#L229</a>


## Summary
DSC liquidators are prone to oracle price manipulations and MEV front-run attacks
## Vulnerability Details
Sudden token price changes caused by oracle price manipulations and MEV front-run can cause liquidators to get less than expected collateral tokens.
## Impact
Liquidators stand to earn less than expected collateral tokens for deposited DSC
## Tools Used
Manual review
## Recommendations
Function liquidate should have an input parameter uint256 minimumOutputTokens and the function should revert at Ln 253 if 

```sh
require(totalCollateralToRedeem >= minimumOutputTokens, "Too little collateral received.");  

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Foundry DeFi Stablecoin CodeHawks Audit Contest |
| Report Date | N/A |
| Finders | 0xSwahili, Bauer, pina |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin
- **Contest**: https://codehawks.cyfrin.io/c/cljx3b9390009liqwuedkn0m0

### Keywords for Search

`vulnerability`

