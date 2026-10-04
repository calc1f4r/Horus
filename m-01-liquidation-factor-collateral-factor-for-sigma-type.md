---
# Core Classification
protocol: Mochi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 935
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-mochi-contest
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/126

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

protocol_categories:
  - dexes
  - cdp
  - cross_chain
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel
  - gzeon
---

## Vulnerability Title

[M-01] liquidation factor < collateral factor for Sigma type

### Overview


This bug report is about the `MochiProfileV0` smart contract which defines liquidation and collateral factors for different asset types. The bug is that for the `AssetClass.Sigma` type, the liquidation factor is _less_ than the collateral factor, meaning that a user can take a loan of up to 45% of their collateral but then immediately gets liquidated as the liquidation factor is only 40%. This goes against the safety buffer that should be maintained between max CF and LF to protect users against liquidations due to normal volatility. The recommended mitigation step for this bug is to increase the max collateral factor for the Sigma type so that it is higher than its liquidation factor.

### Original Finding Content

_Submitted by cmichel, also found by gzeon_

The `MochiProfileV0` defines liquidation and collateral factors for different asset types.
For the `AssetClass.Sigma` type, the liquidation factor is *less* than the collateral factor:

```solidity
function liquidationFactor(address _asset)
    public
    view
    override
    returns (float memory)
{
    AssetClass class = assetClass(_asset);
    if (class == AssetClass.Sigma) { // } else if (class == AssetClass.Sigma) {
        return float({numerator: 40, denominator: 100});
    }
}

function maxCollateralFactor(address _asset)
    public
    view
    override
    returns (float memory)
{
    AssetClass class = assetClass(_asset);
    if (class == AssetClass.Sigma) {
        return float({numerator: 45, denominator: 100});
    }
}
```

This means that one can take a loan of up to 45% of their collateral but then immediately gets liquidated as the liquidation factor is only 40%.
There should always be a buffer between these such that taking the max loan does not immediately lead to liquidations:

> A safety buffer is maintained between max CF and LF to protect users against liquidations due to normal volatility. [Docs](https://hackmd.io/@az-/mochi-whitepaper#Collateral-Factor-CF)

#### Recommended Mitigation Steps
The max collateral factor for the Sigma type should be higher than its liquidation factor.


**[ryuheimat (Mochi) confirmed](https://github.com/code-423n4/2021-10-mochi-findings/issues/126)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | cmichel, gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/126
- **Contest**: https://code4rena.com/contests/2021-10-mochi-contest

### Keywords for Search

`vulnerability`

