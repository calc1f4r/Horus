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
solodit_id: 34432
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
finders_count: 5
finders:
  - Kose
  - t0x1c
  - Madalad
  - rvierdiiev
  - 33audits
---

## Vulnerability Title

Protocol can break for a token with a proxy and implementation contract (like `TUSD`)

### Overview


This bug report discusses a potential issue with tokens that can have their code and logic changed in the future, such as TUSD. If the code behind the token is changed, it could introduce features that break the protocol and lock user funds. This could also lead to bad loans with no way to liquidate them. The recommended solutions are to either introduce logic that freezes interactions with the token if an upgrade is detected, or to have a token whitelist that does not allow for these types of tokens.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/main/src/DSCEngine.sol#L112">https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/main/src/DSCEngine.sol#L112</a>


## Summary
Tokens whose code and logic can be changed in future can break the protocol and lock user funds.

## Vulnerability Details
For a token like `TUSD` (supported by Chainlink TUSD/USD price feed), which has a proxy and implementation contract, if the implementation behind the proxy is changed, it can introduce features which break the protocol, like choosing to not return a bool on transfer(), or changing the balance over time like a rebasing token.

## Impact
Protocol may break in future for this collateral and block user funds deposited as collateral. Also can cause bad loans to be present with no way to liquidate them.

## Tools Used
Manual review

## Recommendations
- Developers integrating with upgradable tokens should consider introducing logic that will freeze interactions with the token in question if an upgrade is detected. (e.g. the [TUSD adapter](https://github.com/makerdao/dss-deploy/blob/7394f6555daf5747686a1b29b2f46c6b2c64b061/src/join.sol#L322) used by MakerDAO).
- OR have a token whitelist which does not allow such tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Foundry DeFi Stablecoin CodeHawks Audit Contest |
| Report Date | N/A |
| Finders | Kose, t0x1c, Madalad, rvierdiiev, 33audits |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin
- **Contest**: https://codehawks.cyfrin.io/c/cljx3b9390009liqwuedkn0m0

### Keywords for Search

`vulnerability`

