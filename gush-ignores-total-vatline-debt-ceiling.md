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
solodit_id: 40971
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

gush ignores total vat.Line() debt ceiling

### Overview

See description below for full details.

### Original Finding Content

## Context
DssLitePsm.sol#L472

## Description
The `trim` function currently only considers its own ilk-specific debt ceiling `ilk.line`, ignoring the global total debt ceiling `vat.Line()`. There are cases when it should trim more DAI than it currently does if it would respect the global total bad debt `vat.debt() - vat.Line()`.

One might expect that trimming more than `gush()` would always result in being able to perform a non-zero `fill()`, but this is currently not the case because of this difference in how `fill` and `trim` handle `vat.Line()`.

## Recommendation
Consider taking into account the `vat.debt() - vat.Line()` difference when trimming, or explain why it's fine for the PSM not to help with bringing the global total system debt back in line:

```solidity
wad = _min(
  _max(
    // To avoid two extra SLOADs it assumes urn.art == ilk.Art.
    _subcap(Art, tArt),
    - _subcap(Art, line / RAY) +
    _max(
      _subcap(Art, line / RAY),
      _subcap(vat.debt(), vat.Line()) / RAY
    )
  ),
  // Cannot burn more than the current balance.
  dai.balanceOf(address(this))
);
```

## Maker DAO
Acknowledged. The global debt ceiling (`Line`) is more of a lock of last resort to prevent inflating the Dai supply indefinitely in case there’s ever a bug in the system.

Under normal conditions, `Line = sum_of_line + buffer`, where the buffer is arbitrary. It is not even an actual variable in the system, but we try to keep it around 600M Dai (I’m not sure about why). Usually, a change in an ilk debt ceiling is bundled with an equivalent change in the global one (i.e., `AutoLine`).

Even in the unlikely scenario when `vat.debt() > vat.Line()`, unwinding the `DssLitePsm` even further wouldn't solve the issue, as all other collateral types in the system don’t have the same behavior. There is no particular reason why this contract should respond differently than other vault-like structures.

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

