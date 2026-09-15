---
# Core Classification
protocol: Overlay Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42322
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-11-overlay
source_link: https://code4rena.com/reports/2021-11-overlay
github_link: https://github.com/code-423n4/2021-11-overlay-findings/issues/55

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
  - liquid_staking
  - dexes
  - yield
  - payments
  - oracle

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] Can't enableCollateral after a disableCollateral

### Overview


The function `disableCollateral` in the code for OverlayV1Mothership.sol is not working properly. It does not set `collateralActive[_collateral]` to false, but it does revoke certain roles. This means that the function `enableCollateral` cannot be used because `collateralActive[_collateral]` will always be true and the second requirement will never be met. This also means that the roles cannot be granted again. To fix this, the code needs to be updated in both the `enableCollateral` and `disableCollateral` functions to properly set `collateralActive[_collateral]` to true and false, respectively. This issue has been confirmed by another user.

### Original Finding Content

_Submitted by gpersoon_

#### Impact

The function `disableCollateral` of OverlayV1Mothership.sol doesn't set `collateralActive\[\_collateral] = false;`
But it does revoke the roles.

Now `enableCollateral`  can never be used because `collateralActive\[\_collateral] ==true`  and it will never pass the second require.
So you can never grant the roles again.

Note: `enableCollateral` also doesn't set `collateralActive\[\_collateral] = true`

#### Proof of Concept

<https://github.com/code-423n4/2021-11-overlay/blob/914bed22f190ebe7088194453bab08c424c3f70c/contracts/mothership/OverlayV1Mothership.sol#L133-L153>

```JS
function enableCollateral (address _collateral) external onlyGovernor {
    require(collateralExists[_collateral], "OVLV1:!exists");
    require(!collateralActive[_collateral], "OVLV1:!disabled");
    OverlayToken(ovl).grantRole(OverlayToken(ovl).MINTER_ROLE(), _collateral);
    OverlayToken(ovl).grantRole(OverlayToken(ovl).BURNER_ROLE(), _collateral);
}

function disableCollateral (address _collateral) external onlyGovernor {
    require(collateralActive[_collateral], "OVLV1:!enabled");
    OverlayToken(ovl).revokeRole(OverlayToken(ovl).MINTER_ROLE(), _collateral);
    OverlayToken(ovl).revokeRole(OverlayToken(ovl).BURNER_ROLE(), _collateral);
}
```

#### Recommended Mitigation Steps

In function `enableCollateral()` add the following (after the require):
`collateralActive\[\_collateral] = true;`

In function `disableCollateral` add the following (after the require):
`collateralActive\[\_collateral] = false;`

**[mikeyrf (Overlay) confirmed](https://github.com/code-423n4/2021-11-overlay-findings/issues/55)** 



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Overlay Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-overlay
- **GitHub**: https://github.com/code-423n4/2021-11-overlay-findings/issues/55
- **Contest**: https://code4rena.com/reports/2021-11-overlay

### Keywords for Search

`vulnerability`

