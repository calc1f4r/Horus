---
# Core Classification
protocol: Pantheonecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44098
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PantheonEcosystem-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-02] Methods `mint()` and `redeem()` are Not Following The `Checks-Effects-Interactions` Pattern

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

In `mint()`& `redeem()` functions, even though there is a `nonReentrant` modifier, the `CEI` pattern is not followed. The `totalEth` state in the both function is executed after the ether transfers.
It is recommended to always first change the state before doing external calls - while the code is not vulnerable right now due to the `nonReentrant` modifier, it is still a best practice to be followed.

## Location of Affected Code

File: [`PANTHEON.sol#L62`](https://github.com/MikeDamiani/PANTHEON/blob/55f4902535cdbb038b21e8c1c9cfb4582cbf354d/PANTHEON.sol#L62)

```solidity
function mint(address reciever) external payable nonReentrant {
```

File: [`PANTHEON.sol#L40`](https://github.com/MikeDamiani/PANTHEON/blob/55f4902535cdbb038b21e8c1c9cfb4582cbf354d/PANTHEON.sol#L40)

```solidity
function redeem(uint256 pantheon) external nonReentrant {
```

## Recommendation

Apply the `Checks-Effects-Interactions` Pattern for both the `mint()` and `redeem()` functions.

## Team Response

Acknowledged, CEI Pattern will implemented.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Pantheonecosystem |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PantheonEcosystem-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

