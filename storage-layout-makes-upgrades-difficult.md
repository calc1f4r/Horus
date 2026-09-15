---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19485
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Storage Layout Makes Upgrades Difficult

### Overview

See description below for full details.

### Original Finding Content

## Description

The current layout of state variables defined in `Lido.sol` and `StETH.sol` greatly increases the complexity of any upgrades to the resulting contract. Because (as of lido-dao v0.2.1-rc.0) the Lido contract inherits from StETH, any changes to the type or number of state variables in StETH can break the layout of any conventionally defined state variables in `Lido.sol`. 

This provides no security risk to the current Lido platform, but the increased upgrade complexity can greatly increase the risk of vulnerabilities unintentionally introduced by future updates.

## Recommendations

For any state variables whose definition could change in future updates (particularly those in `StETH.sol`), heavily consider changing them to make use of the unstructured storage pattern.

In v0.2.0, the following state variables were of note:

- `Lido.sol`:75 `withdrawalCredentials`
- `StETH.sol`:38 `lido`
- `StETH.sol`:44 `_shares`
- `StETH.sol`:45 `_totalShares`
- `StETH.sol`:47 `_allowed`

In v0.2.1-rc.0, the following state variables are of note:

- `StETH.sol`:62 `shares`
- `StETH.sol`:67 `allowances`

Also be careful to ensure consistent storage layout across both contract definitions in future updates.

## Resolution

This has been partially resolved in v0.2.1-rc.0 where, although the StETH inheritance increased complexity, the conventionally defined `Lido.withdrawalCredentials` was moved to unstructured storage.

As Lido now defines no (non-constant) conventionally stored state variables, changes to variables defined in StETH will only need to be internally consistent to preserve the storage layout. Similarly, v0.2.1-rc.0 removed the `lido` and `_totalShares` state variables defined in `StETH.sol`.

The Lido team will need to ensure future upgrades retain a consistent storage layout. If an upgraded version of the Lido contract were to define conventional state variables, no new state variables could be defined in an upgraded version of StETH while retaining the same inheritance relationship.

Although more cumbersome to code with, the unstructured storage pattern allows upgrades to the token and management logic to remain encapsulated even with Lido inheriting from StETH. The testing team also acknowledges that it is more complicated to implement the unstructured storage pattern for more complicated reference types, like the shares and allowances mappings, and this complexity can introduce its own security risk.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf

### Keywords for Search

`vulnerability`

