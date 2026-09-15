---
# Core Classification
protocol: Aligned Layer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38380
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2024/08/aligned-layer/
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
finders_count: 2
finders:
  - Martin Ortner
  -  George Kobakhidze
                        
---

## Vulnerability Title

Unused Imports ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



 Fixed with [yetanotherco/aligned\_layer\#843](https://github.com/yetanotherco/aligned_layer/pull/843) by removing the unused imports. We would like to note that the `ServiceManagerStorage` contract may optionally inherit `IServiceManager`.
 

#### Description


The following source units are imported but not referenced in the contract:


* `AlignedLayerServiceManager` unused `IPauserRegistry`, unused `Pausable`


**contracts/src/core/AlignedLayerServiceManager.sol:L4\-L6**



```
import {Pausable} from "eigenlayer-core/contracts/permissions/Pausable.sol";
import {IPauserRegistry} from "eigenlayer-core/contracts/interfaces/IPauserRegistry.sol";

```
* `AlignedLayerServiceManagerStorage.sol` should inherit `interface` `IServiceManager`


**contracts/src/core/AlignedLayerServiceManagerStorage.sol:L3**



```
import "eigenlayer-middleware/interfaces/IServiceManager.sol";

```
#### Recommendation


Remove unused imports and implement the IServiceManager interface in `AlignedLayerServiceManagerStorage`. Conduct a thorough review of all contracts to identify and eliminate any other unused imports or missing interface implementations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Aligned Layer |
| Report Date | N/A |
| Finders | Martin Ortner,  George Kobakhidze
                         |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2024/08/aligned-layer/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

