---
# Core Classification
protocol: Ethereum Reserve Dollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51111
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/erd/ethereum-reserve-dollar-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/erd/ethereum-reserve-dollar-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

POSSIBLE DOS DUE TO COLLATERALMANAGER.COLLATERALSUPPORT SIZE

### Overview

See description below for full details.

### Original Finding Content

##### Description

The owner of the `CollateralManager.sol` contract can add new collateral tokens which will be supported by the protocol. When adding support for new collaterals, there is no limit for the current amount of collaterals supported, and as the addresses of the collaterals are pushed to an array (`collateralSupport`), the size of this array can grow considerably over time.

Hence, when the protocol calls `priceUpdate()` to update the price of all collaterals supported by the protocol, it iterates over all the collaterals fetching their price from their oracles. In the case the size of the array has grown significantly, it could be possible the price update will revert due to reaching the transaction gas limit.

Code Location
-------------

#### CollateralManager.sol

```
function addCollateral(
    address _collateral,
    address _oracle,
    address _eTokenAddress,
    uint256 _ratio
) external override onlyOwner {
    require(!getIsSupport(_collateral), Errors.CM_COLL_EXISTS);
    _requireRatioLegal(_ratio);

    collateralParams[_collateral] = DataTypes.CollateralParams(
        _ratio,
        _eTokenAddress,
        _oracle,
        DataTypes.CollStatus(1),
        collateralsCount
    );
    collateralSupport.push(_collateral);
    collateralsCount = collateralsCount.add(1);
}

```

#### CollateralManager.sol

```
function priceUpdate() public override {
    if (collateralsCount < 2) {
        return;
    }
    for (uint256 i = 1; i < collateralsCount; ) {
        IOracle(collateralParams[collateralSupport[i]].oracle).fetchPrice();
        unchecked {
            i++;
        }
    }
}

```

##### BVSS

[AO:S/AC:L/AX:L/C:N/I:N/A:C/D:N/Y:N/R:P/S:U (1.0)](/bvss?q=AO:S/AC:L/AX:L/C:N/I:N/A:C/D:N/Y:N/R:P/S:U)

##### Recommendation

**SOLVED**: The `ERD team` solved the issue with the following commit ID.

`Commit ID :` [93c803ae22a7676e05a1fa6ec884589de28fd619](https://github.com/Ethereum-ERD/dev-upgradeable/commit/93c803ae22a7676e05a1fa6ec884589de28fd619)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Ethereum Reserve Dollar |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/erd/ethereum-reserve-dollar-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/erd/ethereum-reserve-dollar-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

