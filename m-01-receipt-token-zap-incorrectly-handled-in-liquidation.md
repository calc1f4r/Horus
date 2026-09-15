---
# Core Classification
protocol: Tangent_2025-12-08
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64047
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-12-08.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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

[M-01] Receipt-token + Zap incorrectly handled in liquidation

### Overview


The report states that there is a bug in the code when a user requests liquidation with a specific setting and provides a "zap route". This results in the transfer of the wrong token to the zapper proxy, causing the swap to fail. The report recommends using the correct token address in this scenario to fix the bug.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

When a user requests liquidation with isReceiptOut = true and provides a zap route, the code transfers the vault receipt token (not LP token) to the zapper proxy. Instructs the zapper proxy to swap the LP token address (collatToken), but the zapper only holds the receipt token. Since approvals are not given for the receipt tokens swap will fail. 

```solidity
    function _postLiquidate(uint256 usgToBurn, PostLiquidate memory postLiquidate, ZapStruct calldata liquidationCall) internal {
        ...

        _transferCollateralWithdraw(liquidationCall.router != address(0) ? address(_zappingProxy) : msg.sender, postLiquidate.collatAmountToLiquidate, postLiquidate.isReceiptOut);

        if (liquidationCall.router != address(0)) {
            _zappingProxy.zapProxy(collatToken, usg, postLiquidate.minUsgOut, msg.sender, liquidationCall);
        }
```

## Recommendations

When isReceiptOut = true, and a zap is requested, use the receipt token address as tokenIn for zap contract.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tangent_2025-12-08 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-12-08.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

