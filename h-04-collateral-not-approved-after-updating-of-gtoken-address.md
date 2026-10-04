---
# Core Classification
protocol: GainsNetwork-February
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37793
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-04] Collateral not approved after updating of GToken address

### Overview


The report is about a bug in a protocol where new collateral tokens are being added. The bug occurs when updating the contract address for a specific token. This update is missing an approval call to the collateral token, which prevents the new GToken contract from being able to transfer collateral from the protocol's address. The severity of this bug is high and the likelihood is medium. The recommendation is to add an approval call to the collateral contract in the function where the update is happening.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

During adding new collateral tokens to the protocol, it's approved for corresponding `_gToken` contract address and GNS `staking` addresses:

```solidity
File: TradingStorageUtils.sol
54:     function addCollateral(address _collateral, address _gToken) internal {
...
81:         // Setup Staking and GToken approvals
82:         IERC20 collateral = IERC20(_collateral);
83:         collateral.approve(_gToken, type(uint256).max);
84:         collateral.approve(staking, type(uint256).max);
85:
86:         emit ITradingStorageUtils.CollateralAdded(_collateral, index, _gToken);
87:     }
```

Later, the `_gToken` address could be updated using the `TradingStorageUtils#updateGToken` function:

```solidity
File: TradingStorageUtils.sol
109:     function updateGToken(address _collateral, address _gToken) internal {
110:         ITradingStorage.TradingStorage storage s = _getStorage();
111:
112:         uint8 index = s.collateralIndex[_collateral];
113:
114:         if (index == 0) {
115:             revert IGeneralErrors.DoesntExist();
116:         }
117:
118:         if (_gToken == address(0)) {
119:             revert IGeneralErrors.ZeroAddress();
120:         }
121:
122:         s.gTokens[index] = _gToken;
123:
124:         emit ITradingStorageUtils.GTokenUpdated(_collateral, index, _gToken);
125:     }
```

However, this function misses the approval call to the collateral token, resulting in an inability of the new GToken contract to transfer collateral from the `GNSMultiCollatDiamond` address.

## Recommendations

Consider adding an `approve` call to the collateral contract in the `TradingStorageUtils.updateGToken()` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | GainsNetwork-February |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

