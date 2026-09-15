---
# Core Classification
protocol: Kilnfi Staking (Consensys)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30462
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/08/kilnfi-staking-consensys/
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
  -  Martin Ortner

  - Tejaswa Rastogi
---

## Vulnerability Title

ProxyAdmin May Cause DoS for SYS_ADMIN

### Overview


The report describes a bug in the `TransparentUpgradeableProxy` system where the ProxyAdmin is unable to delegate calls to the implementation. This means that the SYS_ADMIN cannot be the same as the ProxyAdmin. Additionally, the system-wide pause feature prevents anyone from interacting with the staking contract, including the SYS_ADMIN. This may not be desired by the auditee team, as they may need to manually intervene in the system even when it is paused. The recommendation is to modify the system-wide pause feature to allow the SYS_ADMIN to call staking functions even when the system is paused. 

### Original Finding Content

#### Description


As the `TransparentUpgradeableProxy` doesn’t allow the ProxyAdmin to delegate calls to the implementation, it means the `SYS_ADMIN` can’t be the same as ProxyAdmin. Now, talking about the design, the proxy defines a system-wide feature to pause or unpause. If the proxyAdmin pauses the staking contract, it implies no one can interact with it, not even the `SYS_ADMIN`, which might not be what the auditee team wants. There may be multiple scenarios where the auditee team wants to intervene manually in the system even if the system is paused, for instance, withdrawing funds while restricting the withdrawer.



```
 if (msg.sender == \_getAdmin()) {
 bytes memory ret;
 bytes4 selector = msg.sig;
 if (selector == ITransparentUpgradeableProxy.upgradeTo.selector) {
 ret = \_dispatchUpgradeTo();
 } else if (selector == ITransparentUpgradeableProxy.upgradeToAndCall.selector) {
 ret = \_dispatchUpgradeToAndCall();
 } else if (selector == ITransparentUpgradeableProxy.changeAdmin.selector) {
 ret = \_dispatchChangeAdmin();
 } else if (selector == ITransparentUpgradeableProxy.admin.selector) {
 ret = \_dispatchAdmin();
 } else if (selector == ITransparentUpgradeableProxy.implementation.selector) {
 ret = \_dispatchImplementation();
 } else {
 revert("TransparentUpgradeableProxy: admin cannot fallback to proxy target");
 }
 assembly {
 return(add(ret, 0x20), mload(ret))
 }

```
#### Recommendation


The system-wide pause feature should allow the SYS\_ADMIN to call the staking functions if the system is paused. Something like:



```
function \_beforeFallback() internal override {
 if (StorageSlot.getBooleanSlot(\_PAUSE\_SLOT).value == false || msg.sender == stakingContract.getAdmin() || msg.sender == address(0)) {

 super.\_beforeFallback();
 }

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Kilnfi Staking (Consensys) |
| Report Date | N/A |
| Finders |  Martin Ortner
, Tejaswa Rastogi |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/08/kilnfi-staking-consensys/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

