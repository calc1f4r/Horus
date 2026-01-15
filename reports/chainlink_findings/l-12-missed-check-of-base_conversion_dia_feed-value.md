---
# Core Classification
protocol: Peapods_2024-11-16
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46019
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-12] Missed check of `BASE_CONVERSION_DIA_FEED` value

### Overview

See description below for full details.

### Original Finding Content

The `spTKNMinimalOracle.constructor` checks that `only one (or neither) of the base conversion config should be populated`. At the same time the check of `BASE_CONVERSION_DIA_FEED` variable is missed. This can cause misconfiguration of the contract. Consider adding the corresponding check.

```solidity
    constructor(bytes memory _requiredImmutables, bytes memory _optionalImmutables) {
<...>
        (
            BASE_CONVERSION_CHAINLINK_FEED,
            BASE_CONVERSION_CL_POOL,
>>          BASE_CONVERSION_DIA_FEED,
            CHAINLINK_BASE_PRICE_FEED,
            CHAINLINK_QUOTE_PRICE_FEED,
            _v2Reserves
        ) = abi.decode(_optionalImmutables, (address, address, address, address, address, address));
        V2_RESERVES = IV2Reserves(_v2Reserves);

        // only one (or neither) of the base conversion config should be populated
>>      require(BASE_CONVERSION_CHAINLINK_FEED == address(0) || BASE_CONVERSION_CL_POOL == address(0), "CONV");
<...>
    function _getDefaultPrice18() internal view returns (bool _isBadData, uint256 _price18) {
        (_isBadData, _price18) = IMinimalSinglePriceOracle(UNISWAP_V3_SINGLE_PRICE_ORACLE).getPriceUSD18(
            BASE_CONVERSION_CHAINLINK_FEED, UNDERLYING_TKN, UNDERLYING_TKN_CL_POOL, twapInterval
        );
        if (_isBadData) {
            return (true, 0);
        }

>>      if (BASE_CONVERSION_DIA_FEED != address(0)) {
            (bool _subBadData, uint256 _baseConvPrice18) = IMinimalSinglePriceOracle(DIA_SINGLE_PRICE_ORACLE)
                .getPriceUSD18(address(0), BASE_IN_CL, BASE_CONVERSION_DIA_FEED, 0);
            if (_subBadData) {
                return (true, 0);
            }
            _price18 = (10 ** 18 * _price18) / _baseConvPrice18;
>>      } else if (BASE_CONVERSION_CL_POOL != address(0)) {
            (bool _subBadData, uint256 _baseConvPrice18) = IMinimalSinglePriceOracle(UNISWAP_V3_SINGLE_PRICE_ORACLE)
                .getPriceUSD18(address(0), BASE_IN_CL, BASE_CONVERSION_CL_POOL, twapInterval);
            if (_subBadData) {
                return (true, 0);
            }
            _price18 = (10 ** 18 * _price18) / _baseConvPrice18;
        }
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Peapods_2024-11-16 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

