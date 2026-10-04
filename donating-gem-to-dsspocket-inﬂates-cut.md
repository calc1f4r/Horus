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
solodit_id: 54357
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

Donating gem to DssPocket inﬂates cut() 

### Overview

See description below for full details.

### Original Finding Content

## Context
DssLitePsm.sol#L490-L495

## Description
The collected protocol fee is returned by `DssLitePsm.cut()`, which calculates the fees dynamically. The dynamic fee calculation is used because there is no fee storage variable that gets updated during `buyGem()` and `sellGem()` executions. 

Below is the `cut()` function which shows the returned value is linearly correlated to Psm's dai balance and Pocket's gem balance:

```solidity
function cut() public view returns (uint256 wad) {
    (, uint256 art) = vat.urns(ilk, address(this));
    uint256 cash = dai.balanceOf(address(this));
    wad = _min(cash, cash + gem.balanceOf(pocket) * to18ConversionFactor - art);
}
```

This makes `cut()` manipulable by way of token donations. Donating dai to Psm is not an issue, because fees are denominated and collected in dai. During a dai donation, `cut()` will increase equal to the donation amount, and that can be moved to vow on the next `chug()`. This has no significant effect on the rest of the system.

Donating gem to Pocket can be an issue. Because it increases the `chug()` gable `cut()` without increasing dai. When `chug()` is called, an equivalent amount of dai to the donated gem is moved to vow as a fee.

## Recommendation
If the Maker team desires that donated gem goes to vow as dai, then no change is required. However, if they believe the donated gem should not leave the system as dai as a fee, then tracking the fees in a storage variable that gets updated with each buy and sell appears to be the best solution.

## Maker DAO
Acknowledged. We want to keep gas usage as low as possible, that's why there is no storage variable tracking the amount of gem ever deposited.

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

