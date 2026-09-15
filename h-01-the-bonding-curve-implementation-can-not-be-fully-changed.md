---
# Core Classification
protocol: Moarcandy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36509
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/MoarCandy-security-review.md
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

[H-01] The bonding curve implementation can not be fully changed

### Overview


This bug report is about a function in the `BondingERC20TokenFactory` that is not working as intended. The function is supposed to update the bonding curve implementation, but it does not update the `getOutputPrice` function, which calculates the token price. This can lead to incorrect token prices at the end of the curve. The recommendation is to implement the `getOutputPrice` function in a different contract to fix this issue.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Medium

**Description**

The `BondingERC20TokenFactory.updateBondingCurve` function should update the bonding curve implementation, but it does not change the `getOutputPrice` function, which also calculates the token price since the function is hardcoded in the `ContinuosBondingERC20Token` contract.

```solidity
    function getOutputPrice(
        uint256 outputAmount,
        uint256 inputReserve,
        uint256 outputReserve
    )
        public
        pure
        returns (uint256)
    {
        require(inputReserve > 0 && outputReserve > 0, "Reserves must be greater than 0");
        uint256 numerator = inputReserve * outputAmount;
        uint256 denominator = (outputReserve - outputAmount);
        return numerator / denominator + 1;
    }
```

This can cause an incorrect token price calculation at the end of the curve where the price usually is the highest.

**Recommendations**

Consider implementing the `getOutputPrice` function in the `AMMFormula` contract instead of the `ContinuosBondingERC20Token` contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Moarcandy |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/MoarCandy-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

