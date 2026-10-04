---
# Core Classification
protocol: MakerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54356
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/53e12fbd-182a-45f9-a115-55fdea33c5c4
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_dss-lite-psm_oct2023.pdf
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
finders_count: 3
finders:
  - m4rio
  - shung
  - Christoph Michel
---

## Vulnerability Title

Fees can be trim med 

### Overview

See description below for full details.

### Original Finding Content

## DssLitePsm Explanation

## Context
**File:** DssLitePsm.sol#L478

## Description
The accrued fees that haven't been sent to vow (chugged) yet are tracked in `cut()` as `cash` where `cash` is the sum of the swapped Gem balance and the DAI balance (minted DAI + accrued DAI fees). The `trim` function allows removing excess DAI (gush) when the balance exceeds the debt limits. This excess DAI can include the accrued fees, which will then be temporarily unavailable to be chugged.

Note that calling `trim()` (and `fill()`) never changes the `cash + gem.balanceOf(pocket) * to18ConversionFactor - art` part of `cut()`, as the DAI cash and art are decreased (increased) in tandem by the same `wad` amount. Therefore, the fees are only temporarily lost but can be retrieved once the liquidity crunch has recovered (for example, if Gem is swapped back to DAI, or changes in debt ceilings allow calling `fill` again).

## Example
- **buf:** 1M DAI
- **urn.Art:** 2M DAI
- **GEM balance:** 1M GEM
- **DAI balance:** 1.1M DAI = 1M (as 1M of 2M Art was swapped to GEM) + 0.1M fees.

Setting `ilk.line` to 0.5M, `gush()` will return `min(_subcap(Art, line / RAY), daiBalance) = min(1.5M, 1.1M) = 1.1M`. The entire DAI balance, including the 0.1M fees, will be trimmed.

## Recommendation
Consider always performing a `chug()` if necessary before `trim()` such that adding to the surplus buffer takes priority over decreasing `art`.

## Maker DAO
Acknowledged. This is yet another case we did not want to keep track of the fees to save gas on storage. The bookkeeping functions will be under automation through the keeper network. We'll make sure that the `chug()` job has higher priority than the `trim()` one.

## Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | m4rio, shung, Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_dss-lite-psm_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/53e12fbd-182a-45f9-a115-55fdea33c5c4

### Keywords for Search

`vulnerability`

