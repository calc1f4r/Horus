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
solodit_id: 50713
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

INTEGER UNDERFLOW PSM MODULE

### Overview

See description below for full details.

### Original Finding Content

##### Description

PSM contract may revert due to an arithmetic error caused by integer underflow when `mintFee` is set to a large value.

Code Location
-------------

#### contracts/PSM.sol

```
function createDPrime(address usr, bytes32[] memory collateral, uint256[] memory collatAmount) external {
    require(collateral.length == 1 && collatAmount.length == 1 && collateral[0] == collateralName, "PSM/Incorrect setup");
    uint256 collatAmount18 = collatAmount[0] * to18ConversionFactor; // [wad]
    uint256 fee = _rmul(collatAmount18, mintFee); // rmul(wad, ray) = wad
    uint256 dPrimeAmt = collatAmount18 - fee;

    collateralJoin.join(address(this), collatAmount[0], msg.sender);
[...]

```

##### Score

Impact: 2  
Likelihood: 2

##### Recommendation

**SOLVED**: The `require` statement was added to ensure that `mintFee` is less than 100%.

Reference: [PSM.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/a4b1e5cf9d68e0f2392ac26e3867dda166e70020/contracts/lmcv/PSM.sol#L159)

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

