---
# Core Classification
protocol: Maple Finance
chain: everychain
category: logic
vulnerability_type: vault

# Attack Vector Details
attack_type: vault
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6950
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MapleV2.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MapleV2.pdf
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
  - vault
  - front-running
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Devtooligan
  - Riley Holterhus
  - Jonatas Martins
  - Christoph Michel
  - 0xleastwood
---

## Vulnerability Title

Users depositing to a pool with unrealized losses will take on the losses

### Overview


This bug report is about a vulnerability in the Pool.sol contract. The issue is that when users deposit to the pool, they use the totalAssets() / totalSupply share price, while when they redeem, the totalAssets() - unrealizedLosses() / totalSupply share price is used. This can lead to a situation where deposits use a much higher share price than current redemptions and future deposits, which can cause users to make losses when the unrealized losses are realized. 

The recommendation is to make it very clear to users when there are unrealized losses, and to consider adding an expectedMinimumShares parameter to the Pool.deposit function to ensure that users don't accidentally lose shares when front-run. The Pool.mint function has a similar issue, and the Pool.mintWithPermit function already accepts a maxAssets_ parameter. The team is aware of the issue and plans to make it clear to users through the front end and documentation that it is not recommended to deposit when there are unrealized losses.

### Original Finding Content

## Severity: Medium Risk

## Context
- `pool-v2::Pool.sol#L278`
- `pool-v2::Pool.sol#L275`

## Description
The pool share price used for deposits is always the `totalAssets() / totalSupply`. However, the pool share price when redeeming is `totalAssets() - unrealizedLosses() / totalSupply`. The `unrealizedLosses` value is increased by loan impairments (`LM.impairLoan`) or when starting to trigger a default with a liquidation (`LM.triggerDefault`). The `totalAssets` are only reduced by this value when the loss is realized in `LM.removeLoanImpairment` or `LM.finishCollateralLiquidation`.

This leads to a time window where deposits use a much higher share price than current redemptions and future deposits. Users depositing to the pool during this time window are almost guaranteed to incur losses when they are realized. In the worst case, a `Pool.deposit` might even be (accidentally) front-run by a loan impairment or liquidation.

## Recommendation
Make it very clear to the users when there are unrealized losses and communicate that it is a bad time to deposit. Furthermore, consider adding an `expectedMinimumShares` parameter that is checked against the actual minted shares. This ensures that users don't accidentally lose shares when front-run. Note that this would need to be a new `deposit(uint256 assets_, address receiver_, uint256 expectedMinimumShares_)` function to not break the ERC4626 compatibility. 

The `Pool.mint` function has a similar issue, whereas the `Pool.mintWithPermit` function already accepts a `maxAssets_` parameter.

## Maple
Yes, our team is aware of this issue and plans on making it very clear to users through our front end and documentation that it is not recommended to deposit while there are unrealized losses. The alternative of not using two exchange rates introduces another vulnerability, which is that users could front-run a payment or reversion of an impairment and make a large amount off of the exchange rate change.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Maple Finance |
| Report Date | N/A |
| Finders | Devtooligan, Riley Holterhus, Jonatas Martins, Christoph Michel, 0xleastwood |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/MapleV2.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/MapleV2.pdf

### Keywords for Search

`Vault, Front-Running, Business Logic`

