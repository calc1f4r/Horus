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
solodit_id: 49084
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

[08] Fallback oracles should be implemented in the `CDPVault`

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2024-07-loopfi/blob/57871f64bdea450c1f04c9a53dc1a78223719164/src/CDPVault.sol#L52-L53

```solidity
    /// @notice Oracle of the collateral token
    IOracle public immutable oracle;
```

Now whenever any pricing logic is to be implemented, [this function](https://github.com/code-423n4/2024-07-loopfi/blob/57871f64bdea450c1f04c9a53dc1a78223719164/src/CDPVault.sol#L289-L291) is called: 

```solidity
function spotPrice() public view returns (uint256) {
  return oracle.spot(address(token));
}
```

However, the problem is that if anything happens to the underlying oracle then the Vault is completely bricked. For example, if the attached oracle is a Chainlink oracle that gets put down for maintenance or for change of address, the whole vault's logic that relies on pricing is broken.

### Impact

QA, due to the very low likelihood. However, if this occurs, liquidations are completely broken allowing users to accrue bad debt, so is the `modifyCollateralAndDebt()` and every other function that relies on using the spot prices.

### Recommended Mitigation Steps

Since there is already a support of multiple price providers in protocol, consider modifying `CDPVault#spotPrice()` to first try to get the price from the current/primary oracle set, then set a secondary/fallback oracle for the collateral in case the first one fails, this can easily be achieved by a try/catch logic.

To mitigate the risk associated with relying solely on a primary oracle for pricing information in the `CDPVault`, implementing a fallback oracle mechanism is crucial. This approach ensures that if the primary oracle fails or undergoes maintenance, the system can still function by relying on a secondary oracle. This fallback mechanism can be implemented using Solidity's `try`/`catch` error handling mechanism introduced in Solidity version 0.6.x.

Here's how you can modify the `spotPrice()` function in the `CDPVault.sol` contract to incorporate a fallback oracle:

```diff
contract CDPVault {

..snip
    // CDPVault Parameters
    /// @notice Oracle of the collateral token
    IOracle public immutable oracle;
+    /// @notice Secondary/fallback oracle in case the primary oracle fails
+    IOracle public immutable fallbackOracle;

..snip

    function spotPrice() public view returns (uint256) {
-        return oracle.spot(address(token));
+        // Try getting the price from the primary oracle
+        try oracle.spot(address(token)) returns (uint256 price) {
+            return price;
+        } catch {
+            // If the primary oracle call fails, fall back to the secondary oracle
+            return fallbackOracle.spot(address(token));
+        }
+    }


..snip
}
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

