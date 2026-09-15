---
# Core Classification
protocol: LMCV part 1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50709
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/damfinance/lmcv-part-1-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/damfinance/lmcv-part-1-smart-contract-security-assessment
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

CONTRACTS MIGHT LOSE ADMIN FUNCTIONALITY

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `deny` function is not checking if there are any other active `wards` before setting `wards[usr] = 0`. If the user denies himself, when they are the only `ward`, the contract will lose admin functionality.

Code Location
-------------

[`LMCV`](https://github.com/DecentralizedAssetManagement/lmcv/blob/3391f49ca23e67b2dbb39d35ff7d665dc5769661/contracts/LMCVProxy.sol#L97) module:

#### contracts/LMCVProxy.sol

```
function deny(address usr) external auth {
    wards[usr] = 0;
    emit Deny(usr);
}

```

[`PSM`](https://github.com/DecentralizedAssetManagement/lmcv/blob/3391f49ca23e67b2dbb39d35ff7d665dc5769661/contracts/PSM.sol#L69) module:

#### contracts/PSM.sol

```
function deny(address usr) external auth {
    wards[usr] = 0;
    emit Deny(usr);
}

```

[`dPrime`](https://github.com/DecentralizedAssetManagement/lmcv/blob/3391f49ca23e67b2dbb39d35ff7d665dc5769661/contracts/dPrime.sol#L68) module:

#### contracts/dPrime.sol

```
function deny(address usr) external auth {
    admins[usr] = 0;
    emit Deny(usr);
}

```

[`CollateralJoin`](https://github.com/DecentralizedAssetManagement/lmcv/blob/3391f49ca23e67b2dbb39d35ff7d665dc5769661/contracts/CollateralJoin.sol#L53) module:

#### contracts/CollateralJoin.sol

```
function deny(address usr) external auth {
    wards[usr] = 0;
    emit Deny(usr);
}

```

[`CollateralJoinDecimals`](https://github.com/DecentralizedAssetManagement/lmcv/blob/3391f49ca23e67b2dbb39d35ff7d665dc5769661/contracts/CollateralJoinDecimals.sol#L36) module:

#### contracts/CollateralJoinDecimals.sol

```
function deny(address usr) external auth {
    wards[usr] = 0;
    emit Deny(usr);
}

```

##### Score

Impact: 3  
Likelihood: 1

##### Recommendation

**SOLVED**: The `ArchAdmin` variable was added to the contract. The address assigned to this field cannot be removed from `wards`/`admins` mapping via `administrate` or `deny` functions, ensuring there is at least one administrator on the contract. To update this address, a new `ArchAdmin` must be set; then the address can be removed from admins mapping.

Reference:

* [LMCV.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/a4b1e5cf9d68e0f2392ac26e3867dda166e70020/contracts/lmcv/LMCV.sol#L134)
* [LMCVProxy.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/a4b1e5cf9d68e0f2392ac26e3867dda166e70020/contracts/lmcv/LMCVProxy.sol#L114)
* [PSM.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/a4b1e5cf9d68e0f2392ac26e3867dda166e70020/contracts/lmcv/PSM.sol#L76)
* [dPrime.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/a4b1e5cf9d68e0f2392ac26e3867dda166e70020/contracts/lmcv/dPrime.sol#L77)
* [CollateralJoin.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/a4b1e5cf9d68e0f2392ac26e3867dda166e70020/contracts/lmcv/CollateralJoin.sol#L60)
* [CollateralJoinDecimals.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/a4b1e5cf9d68e0f2392ac26e3867dda166e70020/contracts/lmcv/CollateralJoinDecimals.sol#L43)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | LMCV part 1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/damfinance/lmcv-part-1-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/damfinance/lmcv-part-1-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

