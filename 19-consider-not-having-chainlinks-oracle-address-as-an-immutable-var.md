---
# Core Classification
protocol: LoopFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49095
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-loopfi
source_link: https://code4rena.com/reports/2024-07-loopfi
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
finders_count: 0
finders:
---

## Vulnerability Title

[19] Consider not having Chainlink's oracle address as an immutable var

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2024-07-loopfi/blob/57871f64bdea450c1f04c9a53dc1a78223719164/src/oracle/BalancerOracle.sol#L23

```solidity
IOracle public immutable chainlinkOracle;
```

### Impact

Using an immutable reference for the Chainlink oracle address reduces flexibility and could lead to issues if the Chainlink oracle address needs to be updated or if it becomes compromised.

### Recommended Mitigation Steps

Replace the immutable reference with a mutable state variable and implement a function to update the Chainlink oracle address:

```diff
- IOracle public immutable chainlinkOracle;
+ IOracle public chainlinkOracle;
..snip
+function updateChainlinkOracle(address newOracle) external onlyRole(MANAGER_ROLE) {
+    require(newOracle != address(0), "Invalid oracle address");
+    chainlinkOracle = IOracle(newOracle);
+}
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LoopFi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-loopfi
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-07-loopfi

### Keywords for Search

`vulnerability`

