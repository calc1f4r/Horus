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
solodit_id: 13208
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/01/rocket-pool-atlas-v1.2/
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
finders_count: 2
finders:
  - Dominik Muhs
  -  Martin Ortner

---

## Vulnerability Title

RocketMinipoolDelegate - Redundant refund() call on forced finalization ✓ Fixed

### Overview


This bug report is about an issue with the `RocketMinipoolDelegate.refund` function in the code of the RocketPool project. The function will force finalization if a user previously distributed the pool, however, the `_finalise()` function already calls `_refund()` if there is a node refund balance to transfer, making the additional call to `_refund()` in `refund()` obsolete. The bug was fixed by refactoring `refund()` to avoid a double invocation of `_refund()` in the `_finalise()` codepath. The fix can be found in the GitHub repository at <https://github.com/rocket-pool/rocketpool/tree/77d7cca65b7c0557cfda078a4fc45f9ac0cc6cc6>. The recommendation was to refactor the if condition to contain `_refund()` in the else branch.

### Original Finding Content

#### Resolution



Fixed in <https://github.com/rocket-pool/rocketpool/tree/77d7cca65b7c0557cfda078a4fc45f9ac0cc6cc6> by refactoring `refund()` to avoid a double invocation of `_refund()` in the `_finalise()` codepath.



> 
> Fixed per the recommendation. Thanks.
> 
> 
> 




#### Description


The `RocketMinipoolDelegate.refund` function will force finalization if a user previously distributed the pool. However, `_finalise` already calls `_refund()` if there is a node refund balance to transfer, making the additional call to `_refund()` in `refund()` obsolete.


#### Examples


**code/contracts/contract/minipool/RocketMinipoolDelegate.sol:L200-L209**



```
function refund() override external onlyMinipoolOwnerOrWithdrawalAddress(msg.sender) onlyInitialised {
    // Check refund balance
    require(nodeRefundBalance > 0, "No amount of the node deposit is available for refund");
    // If this minipool was distributed by a user, force finalisation on the node operator
    if (!finalised && userDistributed) {
        \_finalise();
    }
    // Refund node
    \_refund();
}

```
**code/contracts/contract/minipool/RocketMinipoolDelegate.sol:L445-L459**



```
function \_finalise() private {
    // Get contracts
    RocketMinipoolManagerInterface rocketMinipoolManager = RocketMinipoolManagerInterface(getContractAddress("rocketMinipoolManager"));
    // Can only finalise the pool once
    require(!finalised, "Minipool has already been finalised");
    // Set finalised flag
    finalised = true;
    // If slash is required then perform it
    if (nodeSlashBalance > 0) {
        \_slash();
    }
    // Refund node operator if required
    if (nodeRefundBalance > 0) {
        \_refund();
    }

```
#### Recommendation


We recommend refactoring the if condition to contain `_refund()` in the else branch.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

