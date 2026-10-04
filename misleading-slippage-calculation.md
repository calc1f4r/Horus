---
# Core Classification
protocol: Aarna
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37169
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-04-aarna.md
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
  - Zokyo
---

## Vulnerability Title

Misleading slippage calculation

### Overview


This bug report discusses a problem with the uniswapV3Router function in the AFiBase contract. This function is supposed to set a minimum amount of output tokens that the caller will receive from a Uniswap swap in order to prevent slippage. However, due to a logic error, the minimum amount is always set to 10, making the protection ineffective. The recommendation is to adjust the SLIPPAGE_FACTOR based on the type of asset being traded. This issue has been resolved.

### Original Finding Content

**Severity**: High

**Status**:  Resolved

**Description**

The uniswapV3Router function from AFiBase contract is intended to calculate and use the minimumAmountOut to set a floor on the acceptable amount of output tokens the caller will receive from a Uniswap swap, as a protection against slippage. However, due to the logic within the function, the minimumAmountOut is effectively always set to 10 if initially calculated to be equal to or greater than 10
```solidity
   //safe calculation
   if (minimumAmountOut >= 10) {
     minimumAmountOut -= (minimumAmountOut - 10);
   }
```
The actual purpose of the minimumAmountOut is to protect users from unfavorable market shifts by ensuring that they get at least the minimum expected amount from their swap. By effectively setting this minimum to a static value of 10, the protection becomes essentially meaningless.

**Recommendation**: 

Distinguish between long-tail assets and relatively stable ones and adjust the SLIPPAGE_FACTOR accordingly.

**Fix**: 

The issue has been fixed as recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Aarna |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-04-aarna.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

