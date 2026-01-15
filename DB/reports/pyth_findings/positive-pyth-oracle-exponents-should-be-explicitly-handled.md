---
# Core Classification
protocol: Octodefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61607
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
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

protocol_categories:
  - oracle

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Giovanni Di Siena
  - Farouk
---

## Vulnerability Title

Positive Pyth oracle exponents should be explicitly handled

### Overview

See description below for full details.

### Original Finding Content

**Description:** `PriceOracle._scalePythPrice()` assumes that the exponent `_expo` will always be negative:

```solidity
    function _scalePythPrice(int256 _price, int32 _expo) internal pure returns (uint256) {
        if (_price < 0) {
            revert NegativePriceNotAllowed();
        }

@>      uint256 _absExpo = uint32(-_expo);

        if (_expo <= -18) {
            return uint256(_price) * (10 ** (_absExpo - 18));
        }

        return uint256(_price) * 10 ** (18 - _absExpo);
    }
```

While this assumption is [not likely to be violated](https://x.com/abarbatei/status/1901327645373030711), it is possible for the exponent to be configured as a positive value based on its signed type and usage in [other libraries](https://github.com/pyth-network/pyth-crosschain/blob/main/target_chains/ethereum/sdk/solidity/PythUtils.sol).

If the protocol were to ever rely on a Pyth oracle with a positive exponent then `uint32(-expo)` could silently underflow, resulting in a huge absolute value and causing execution to revert during the final scaling.

**Recommended Mitigation:** Consider explicitly handling the case where the exponent is positive.

**OctoDeFi:** Fixed in PR [\#19](https://github.com/octodefi/strategy-builder-plugin/pull/19).

**Cyfrin:** Verified. The positive exponent case is now explicitly handled.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Octodefi |
| Report Date | N/A |
| Finders | Giovanni Di Siena, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

