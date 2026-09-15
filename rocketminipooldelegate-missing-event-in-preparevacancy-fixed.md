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
solodit_id: 13216
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

RocketMinipoolDelegate - Missing event in prepareVacancy ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



Fixed in <https://github.com/rocket-pool/rocketpool/tree/77d7cca65b7c0557cfda078a4fc45f9ac0cc6cc6> by emitting a new event `MinipoolVacancyPrepared`.



> 
> Agreed. Added event per recommendation. Thanks.
> 
> 
> 




#### Description


The function `prepareVacancy` updates multiple contract state variables and should therefore emit an event.


#### Examples


**code/contracts/contract/minipool/RocketMinipoolDelegate.sol:L286-L309**



```
/// @dev Sets the bond value and vacancy flag on this minipool
/// @param \_bondAmount The bond amount selected by the node operator
/// @param \_currentBalance The current balance of the validator on the beaconchain (will be checked by oDAO and scrubbed if not correct)
function prepareVacancy(uint256 \_bondAmount, uint256 \_currentBalance) override external onlyLatestContract("rocketMinipoolManager", msg.sender) onlyInitialised {
    // Check status
    require(status == MinipoolStatus.Initialised, "Must be in initialised status");
    // Sanity check that refund balance is zero
    require(nodeRefundBalance == 0, "Refund balance not zero");
    // Check balance
    RocketDAOProtocolSettingsMinipoolInterface rocketDAOProtocolSettingsMinipool = RocketDAOProtocolSettingsMinipoolInterface(getContractAddress("rocketDAOProtocolSettingsMinipool"));
    uint256 launchAmount = rocketDAOProtocolSettingsMinipool.getLaunchBalance();
    require(\_currentBalance >= launchAmount, "Balance is too low");
    // Store bond amount
    nodeDepositBalance = \_bondAmount;
    // Calculate user amount from launch amount
    userDepositBalance = launchAmount.sub(nodeDepositBalance);
    // Flag as vacant
    vacant = true;
    preMigrationBalance = \_currentBalance;
    // Refund the node whatever rewards they have accrued prior to becoming a RP validator
    nodeRefundBalance = \_currentBalance.sub(launchAmount);
    // Set status to preLaunch
    setStatus(MinipoolStatus.Prelaunch);
}

```
#### Recommendation


Emit the missing event.

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

