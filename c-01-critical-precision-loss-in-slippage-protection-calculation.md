---
# Core Classification
protocol: ULTI-November
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43910
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/ULTI-security-review-November.md
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

[C-01] Critical precision loss in slippage protection calculation

### Overview


The ULTI contract has a bug in its slippage protection mechanism during token swaps. This means that when users make a trade using the contract, there is a high chance that they will lose money or the trade will not go through. The problem is caused by a mistake in the calculation of the expected amount of ULTI tokens that should be received in the trade. This mistake causes a loss of precision and can also disable the contract's internal protection against slippage. This bug can be exploited by malicious actors to manipulate the price of ULTI tokens and extract value from the contract's reserves. The recommendation is to fix the calculation by using the correct scaling factor of 1e18 instead of 18.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

The ULTI contract contains a precision error in its slippage protection mechanism during token swaps (using 18 instead of 1e18). In the `_swapInputTokenForUlti` function, the calculation of `expectedUltiAmountWithoutSlippage` uses an incorrect scaling factor that results in a significant precision loss.

```solidity
    function _swapInputTokenForUlti(uint256 inputAmountToSwap, uint256 minUltiAmount, uint256 twap, uint256 deadline)
        private
        returns (uint256 ultiAmount)
    {
        ...
        // 2. Calculate expected output without slippage
        uint256 expectedUltiAmountWithoutSlippage = inputAmountToSwap * 18 / twap; // @audit should be inputAmountToSwap * 1e18 / twap

        // 3. Choose the higher minimum amount between user-specified and internal slippage protection
        uint256 minUltiAmountInternal = (expectedUltiAmountWithoutSlippage * (10000 - MAX_SWAP_SLIPPAGE_BPS)) / 10000;
        uint256 effectiveMinUltiAmount = minUltiAmount > minUltiAmountInternal ? minUltiAmount : minUltiAmountInternal;
        ...

        return ultiAmount;
    }
```

The error leads to:

- Precision Loss: Using 18 instead of 1e18 as the scaling factor causes `expectedUltiAmountWithoutSlippage` to be drastically undervalued or rounded down to 0 for most practical input amounts.
- Broken Slippage Protection: When `expectedUltiAmountWithoutSlippage` is 0, `minUltiAmountInternal` also becomes 0, effectively disabling the contract's internal slippage protection.

Malicious actors can:

- Set a very low minUltiAmount (e.g., 1)
- Manipulate the ULTI/Input token price through market operations
- Execute swaps with extreme slippage
- Extract value from the protocol's reserves

## Recommendations

Fix the calculation of `expectedUltiAmountWithoutSlippage` by multiplying `inputAmountToSwap` by `1e18` instead of `18`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | ULTI-November |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/ULTI-security-review-November.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

