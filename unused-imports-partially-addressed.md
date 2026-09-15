---
# Core Classification
protocol: Rocket Pool Atlas (v1.2)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13218
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/01/rocket-pool-atlas-v1.2/
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
  - Dominik Muhs
  -  Martin Ortner

---

## Vulnerability Title

Unused Imports  Partially Addressed

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



Addressed in <https://github.com/rocket-pool/rocketpool/tree/77d7cca65b7c0557cfda078a4fc45f9ac0cc6cc6> by removing all but the following two mentioned unused imports:


* `RocketRewardsPoolInterface`
* `RocketSmoothingPoolInterface`




#### Description


The following source units are imported but not referenced in the importing source unit:


**code/contracts/contract/rewards/RocketMerkleDistributorMainnet.sol:L11**



```
import "../../interface/rewards/RocketSmoothingPoolInterface.sol";

```
**code/contracts/contract/minipool/RocketMinipoolFactory.sol:L12-L18**



```
import "../../interface/minipool/RocketMinipoolManagerInterface.sol";
import "../../interface/minipool/RocketMinipoolQueueInterface.sol";
import "../../interface/node/RocketNodeStakingInterface.sol";
import "../../interface/util/AddressSetStorageInterface.sol";
import "../../interface/node/RocketNodeManagerInterface.sol";
import "../../interface/network/RocketNetworkPricesInterface.sol";
import "../../interface/dao/protocol/settings/RocketDAOProtocolSettingsMinipoolInterface.sol";

```
**code/contracts/contract/minipool/RocketMinipoolFactory.sol:L8-L10**



```
import "../../types/MinipoolStatus.sol";
import "../../types/MinipoolDeposit.sol";
import "../../interface/dao/node/RocketDAONodeTrustedInterface.sol";

```
**code/contracts/contract/minipool/RocketMinipoolBase.sol:L7-L8**



```
import "../../types/MinipoolDeposit.sol";
import "../../types/MinipoolStatus.sol";

```
**code/contracts/contract/minipool/RocketMinipoolDelegate.sol:L13-L14**



```
import "../../interface/network/RocketNetworkPricesInterface.sol";
import "../../interface/node/RocketNodeManagerInterface.sol";

```
**code/contracts/contract/node/RocketNodeManager.sol:L13**



```
import "../../interface/rewards/claims/RocketClaimNodeInterface.sol";

```
**code/contracts/contract/rewards/RocketClaimDAO.sol:L7**



```
import "../../interface/rewards/RocketRewardsPoolInterface.sol";

```
Duplicate Import:


**code/contracts/contract/minipool/RocketMinipoolFactory.sol:L19-L20**



```
import "../../interface/dao/protocol/settings/RocketDAOProtocolSettingsNodeInterface.sol";
import "../../interface/dao/protocol/settings/RocketDAOProtocolSettingsNodeInterface.sol";

```
The above list is exemplary, and there are likely more occurrences across the code base.


#### Recommendation


We recommend checking all imports and removing unused/unreferenced and unnecessary imports.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Rocket Pool Atlas (v1.2) |
| Report Date | N/A |
| Finders | Dominik Muhs,  Martin Ortner
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/01/rocket-pool-atlas-v1.2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

