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
solodit_id: 64233
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

Precision loss in the `SecuritizeSwap.calculateDsTokenAmount()` function.

### Overview

See description below for full details.

### Original Finding Content

**Description:** When `stableCoinDecimals` is greater than `dsTokenDecimals`, the calculation is divided into two parts: dividing by `(10 ** (stableCoinDecimals - dsTokenDecimals))` at `L242` and then multiplying by `10 ** stableCoinDecimals` at `L245`. This can result in a loss of precision.

```solidity
        if (stableCoinDecimals <= dsTokenDecimals) {
            adjustedStableCoinAmount = _stableCoinAmount * (10 ** (dsTokenDecimals - stableCoinDecimals));
        } else {
242         adjustedStableCoinAmount = _stableCoinAmount / (10 ** (stableCoinDecimals - dsTokenDecimals));
        }
        // The InternalNavSecuritizeImplementation uses rate expressed with same number of decimals as stableCoin
245     uint256 dsTokenAmount = adjustedStableCoinAmount * 10 ** stableCoinDecimals / currentNavRate;
```

**Impact:** The calculated `dsTokenAmount` is less than it should be, resulting in a loss of funds for users.

**Proof Of Concept:**

In fact, the correct formula is
```solidity
        dsTokenAmount = _stableCoinAmount * 10 ** dsTokenDecimals / currentNavRate;
```

Let's consider the following scenario:
1. `stableCoinDecimals = 18`
2. `dsTokenDecimals = 6`
3. `currentNavRate = 1e12`(implying `stableCoin : dsToken = 1e6 : 1`)
4. `_stableCoinAmount = 1e18 - 1`

The current logic calculates as follows:
- `L242`: `adjustedStableCoinAmount = (1e18 - 1) / (10 ** (18 - 6)) = 1e6 - 1`
- `L245`: `dsTokenAmount = (1e6 - 1) * 10 ** 18 / 1e12 = 1e12 - 1e6`

However, the actual correct `dsTokenAmount` should be `(1e18 - 1) * 1e6 / 1e12 = 1e12 - 1`, resulting in a difference of `1e6 - 1`.

**Recommended Mitigation:** The intermediate variable `adjustedStableCoinAmount` is unnecessary.

```diff
    function calculateDsTokenAmount(uint256 _stableCoinAmount) internal view returns (uint256, uint256) {
        uint256 stableCoinDecimals = ERC20(address(stableCoinToken)).decimals();
        uint256 dsTokenDecimals = ERC20(address(dsToken)).decimals();
        uint256 currentNavRate = navProvider.rate();

-       uint256 adjustedStableCoinAmount;
-       if (stableCoinDecimals <= dsTokenDecimals) {
-           adjustedStableCoinAmount = _stableCoinAmount * (10 ** (dsTokenDecimals - stableCoinDecimals));
-       } else {
-           adjustedStableCoinAmount = _stableCoinAmount / (10 ** (stableCoinDecimals - dsTokenDecimals));
-       }
-       // The InternalNavSecuritizeImplementation uses rate expressed with same number of decimals as stableCoin
-       uint256 dsTokenAmount = adjustedStableCoinAmount * 10 ** stableCoinDecimals / currentNavRate;

+       uint256 dsTokenAmount = _stableCoinAmount * 10 ** dsTokenDecimals / currentNavRate;

        return (dsTokenAmount, currentNavRate);
    }
```


**Securitize:** Fixed in commit [b09460](https://bitbucket.org/securitize_dev/securitize-swap/commits/b094604b341123a49c8abbd6e1c3d53d7c102f28)

**Cyfrin:** Verified.

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

