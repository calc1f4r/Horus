---
# Core Classification
protocol: Securitize Redemptions
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64238
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
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
  - Hans
---

## Vulnerability Title

Missing input validation in `CollateralLiquidityProvider::setExternalCollateralRedemption`

### Overview

See description below for full details.

### Original Finding Content

**Description:** _Note that this finding assumes the other finding about access control is mitigated_.
The contract `CollateralLiquidityProvider` relies on `externalCollateralRedemption` to process redemption.
The function `supplyTo()`  is the core function of this contract.
```solidity
CollateralLiquidityProvider.sol
61:     function supplyTo(address _redeemer, uint256 _amount) whenNotPaused onlySecuritizeRedemption public override {
62:         //take collateral funds from collateral provider
63:         IERC20(externalCollateralRedemption.asset()).transferFrom(collateralProvider, address(this), _amount);
64:
65:         //approve external redemption
66:         IERC20(externalCollateralRedemption.asset()).approve(address(externalCollateralRedemption), _amount);
67:
68:         //get liquidity
69:         externalCollateralRedemption.redeem(_amount);
70:
71:         //supply _redeemer
72:         liquidityToken.transfer(_redeemer, _amount);
73:     }
```
Looking at the L69 with L72, the function is assuming that `liquidityToken = externalCollateralRedemption.liquidity`.
But this is not validated in the function `setExternalCollateralRedemption` and there is a risk to cause an inconsistency.

**Impact:** We evaluate the impact to be LOW assuming the function will be protected by a proper access control mitigating the other finding.

**Recommended Mitigation:** Validate that `liquidityToken = externalCollateralRedemption.liquidity` in the function `setExternalCollateralRedemption()`.

**Securitize:** Fixed in commit [3977ca](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/3977ca8ffb259a01e8dab894745751cf2150abf4)

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Redemptions |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

