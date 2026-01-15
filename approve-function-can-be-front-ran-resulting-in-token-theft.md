---
# Core Classification
protocol: Liquid Collective
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7023
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - front-running
  - approve

protocol_categories:
  - staking_pool
  - liquid_staking
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Optimum
  - Matt Eccentricexit
  - Danyal Ellahi
  - Saw-mon and Natalie
  - Emanuele Ricci
---

## Vulnerability Title

approve() function can be front-ran resulting in token theft

### Overview


A bug was reported in the SharesManager.1.sol and WLSETH.1.sol files related to the approve() function. This bug is a race condition that can lead to token theft if a user calls the approve function a second time on a spender that was already allowed. The spender can then front-run the transaction and call transferFrom() to transfer the previous value and still receive the authorization to transfer the new value.

To prevent users from losing funds from front-running attacks, it was recommended to consider implementing functionality that allows a user to increase and decrease their allowance similar to Lido's implementation. This recommendation was implemented in SPEARBIT/9 and the _spendAllowance in both SharesManager and WLSETH should execute emit Approval(owner, spender, amount). This was fixed in PR 151.

### Original Finding Content

## Security Advisory

## Severity
**Medium Risk**

## Context
- SharesManager.1.sol#L143
- WLSETH.1.sol#L116-L120

## Description
The `approve()` function has a known race condition that can lead to token theft. If a user calls the `approve` function a second time on a spender that was already allowed, the spender can front-run the transaction and call `transferFrom()` to transfer the previous value and still receive the authorization to transfer the new value.

## Recommendation
Consider implementing functionality that allows a user to increase and decrease their allowance similar to Lido's implementation. This will help prevent users from losing funds from front-running attacks.

- **Alluvial:** Recommendation implemented in SPEARBIT/9.
- **Spearbit:** Acknowledged. Note: if you want to follow the same logic of OpenZeppelin ERC20 implementation, the `_spendAllowance` in both SharesManager and WLSETH should execute `emit Approval(owner, spender, amount);`.
- **Alluvial:** Fixed in PR 151.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Liquid Collective |
| Report Date | N/A |
| Finders | Optimum, Matt Eccentricexit, Danyal Ellahi, Saw-mon and Natalie, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf

### Keywords for Search

`Front-Running, Approve`

