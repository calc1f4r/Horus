---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49796
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
  - oxtenma
---

## Vulnerability Title

Unsafe Casting performed in the `GMXOracle::_getTokenPriceMinMaxFormatted`

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/GMXOracle.sol#L311">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/GMXOracle.sol#L311</a>


## Summary
The function `GMXOracle::_getTokenPriceMinMaxFormatted` in line#314 have converted the int256 result from Chainlink Oracle to uint256. Converting int256 to uint256 can have unexpected consequences when done unsafely. 

## Vulnerability Details
The function `GMXOracle::_getTokenPriceMinMaxFormatted` in line#314 have converted the int256 result from Chainlink Oracle to uint256. Converting int256 to uint256 can have unexpected consequences when done unsafely. 
```
function _getTokenPriceMinMaxFormatted(address token) internal view returns (uint256) {
    (int256 _price, uint8 _priceDecimals) = chainlinkOracle.consult(token);

@>  return uint256(_price) * 10 ** (30 - IERC20Metadata(token).decimals() - _priceDecimals);
  }
```
We are providing a similar scenario that can be reproduced in Remix:
```
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract TestUnsafeCasting {
    function testUpsafeCasting(int256 x) public pure returns (uint256) {
        return uint256(x);
    }
}
```
In this case, when we input `-23` as input to the function `testUnsafeCasting`, it returns `115792089237316195423570985008687907853269984665640564039457584007913129639913` because of unsafe casting from int256 to uint256.

## Impact
Protocol may experience unexpected output from the function `GMXOracle::_getTokenPriceMinMaxFormatted`
## Tools Used
Manual Review, Remix
## Recommendations
Use Openzeppelin SafeCast Library.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | oxtenma |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://codehawks.cyfrin.io/c/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

