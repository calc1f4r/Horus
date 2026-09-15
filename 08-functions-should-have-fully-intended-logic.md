---
# Core Classification
protocol: Ethena Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29395
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-ethena
source_link: https://code4rena.com/reports/2023-10-ethena
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
  - staking_pool
  - decentralized_stablecoin

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[08] Functions should have fully intended logic

### Overview

See description below for full details.

### Original Finding Content

The function below is meant to be used only for minting. Hence, redeeming has got nothing to do with this view function. Consider refactoring the first if block so [`mint()`](https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/EthenaMinting.sol#L171) could revert earlier if need be:

https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/EthenaMinting.sol#L351-L374

```diff
  function verifyRoute(Route calldata route, OrderType orderType) public view override returns (bool) {
    // routes only used to mint
-    if (orderType == OrderType.REDEEM) {
-      return true;
-    }
+    if (orderType =! OrderType.MINT) {
+      return false;
+    }
    uint256 totalRatio = 0;
    if (route.addresses.length != route.ratios.length) {
      return false;
    }
    if (route.addresses.length == 0) {
      return false;
    }
    for (uint256 i = 0; i < route.addresses.length; ++i) {
      if (!_custodianAddresses.contains(route.addresses[i]) || route.addresses[i] == address(0) || route.ratios[i] == 0)
      {
        return false;
      }
      totalRatio += route.ratios[i];
    }
    if (totalRatio != 10_000) {
      return false;
    }
    return true;
  }
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ethena Labs |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-ethena
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-10-ethena

### Keywords for Search

`vulnerability`

