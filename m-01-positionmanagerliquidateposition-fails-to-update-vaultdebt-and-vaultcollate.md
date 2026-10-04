---
# Core Classification
protocol: Hyperstable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55695
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - @IAm0x52
---

## Vulnerability Title

[M-01] `PositionManager#liquidatePosition` fails to update vaultDebt and vaultCollateral

### Overview


The bug report is about a problem found in the PositionManager.sol file during an audit. The code in lines 169-185 does not update two variables, `_vaultDebtSnapshot` and `vaultCollateral`, when performing a liquidation. This can lead to incorrect interest rates and leave phantom collateral and debt in the system. The recommendation is to update these variables and the issue has been fixed in a recent commit.

### Original Finding Content

**Details**

**First discovered by Dev team during audit period**

[PositionManager.sol#L169-L185](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/core/PositionManager.sol#L169-L185)

        function liquidatePosition(address _vault, address _target, uint256 _debtToRepay, uint256 _sharesToLiquidate)
            external
        {
            if (msg.sender != liquidationManager) {
                revert OnlyLiquidatorManager();
            }
            // Debt and collateral shares are adjusted for the liquidated account
            _debtSnapshot[_target][_vault] -= _debtToRepay;
            collateralShares[_target][_vault] -= _sharesToLiquidate;


    @>      uint256 updatedVaultDebt = _vaultDebtSnapshot[_vault] - _debtToRepay;
    @>      uint256 updatedVaultCollateral = vaultCollateral[_vault] - _sharesToLiquidate;


            interestRateStrategy.updateVaultInterestRate(
                _vault, updatedVaultCollateral.mulWad(IVault(_vault).sharePrice()), updatedVaultDebt, IVault(_vault).MCR()
            );
        }

In the above lines we see that `_vaultDebtSnapshot` and `vaultCollateral` are not update when performing the liquidation. This leaves phantom collateral and debt in the system which can lead to inaccurate interest rates.

**Lines of Code**

[PositionManager.sol#L179-L180](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/core/PositionManager.sol#L179-L180)

**Recommendation**

`_vaultDebtSnapshot` and `vaultCollateral` should be updated

**Remediation**

Fixed in [1277f39](https://github.com/hyperstable/contracts/commit/1277f396dcd14f00c6258eb1f9668f43be1d311f). Updated values are now correctly written to storage.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Hyperstable |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

