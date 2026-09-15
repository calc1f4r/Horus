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
solodit_id: 45270
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-11-ethena-labs
source_link: https://code4rena.com/reports/2024-11-ethena-labs
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

[L-07] The`GATEKEEPER_ROLE` shouldn't be allowed to remove the `COLLATERAL_MANAGER_ROLE`

### Overview

See description below for full details.

### Original Finding Content


From the [readme](https://github.com/code-423n4/2024-11-ethena-labs/blob/main/README.md), the `GATEKEEPER` has the ability to disable minting and redeeming.
| Role              | Description                                                                        |
|-------------------|------------------------------------------------------------------------------------|
| GATEKEEPER        | has the ability to disable minting and redeeming                                   |

However, in the codebase, the `GATEKEEPER_ROLE` can remove the `COLLATERAL_MANAGER_ROLE` from an account.
```solidity
File: contracts\ustb\UStbMinting.sol
379:     function removeCollateralManagerRole(address collateralManager) external onlyRole(GATEKEEPER_ROLE) {
380:         _revokeRole(`COLLATERAL_MANAGER_ROLE`, collateralManager);
381:     }
```
The `COLLATERAL_MANAGER_ROLE` can transfer an asset to a custody wallet using the `transferToCustody()` function.

It means that the `GATEKEEPER_ROLE` can remove the functionality to transfer assets to the custody wallet.

It is recommended to modify the code as follows:
```diff
File: contracts\ustb\UStbMinting.sol
-        function removeCollateralManagerRole(address collateralManager) external onlyRole(DEFAULT_ADMIN_ROLE) {
+        function removeCollateralManagerRole(address collateralManager) external onlyRole(GATEKEEPER_ROLE) {
380:         _revokeRole(`COLLATERAL_MANAGER_ROLE`, collateralManager);
381:     }
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

- **Source**: https://code4rena.com/reports/2024-11-ethena-labs
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-11-ethena-labs

### Keywords for Search

`vulnerability`

