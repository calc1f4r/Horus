---
# Core Classification
protocol: Zap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35667
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-07-Zap.md
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
  - Zokyo
---

## Vulnerability Title

Missing `disableinitializers()` in constructor can lead to malicious takeover of the implementation contract

### Overview


The bug report states that there is a medium severity bug in the Airdrop.sol contract that has been resolved. The bug allows an attacker to take over an uninitialized contract, which can affect both the proxy and its implementation contract. This means that the proxy can be impacted by the bug. The reason for this is that when the Airdrop contract is deployed and initialized, the initialize method on the newly created AirdropZap proxy's implementation contract is not called. This allows anyone to call that method and pass in any values they want, which can be dangerous if an attacker passes in a contract that calls `selfdestruct`. This will erase all code from the implementation contract and give the attacker control over it. To prevent this from happening, it is recommended to invoke the `_disableInitializers()` function from Openzeppelin in the constructor of the contract. This will automatically lock the implementation contract when it is deployed.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Location**: Airdrop.sol

**Description**

An uninitialized contract can be taken over by an attacker. This applies to both a proxy and its implementation contract, which may impact the proxy. But in case of the implementation contract, a `disableinitializers()` is necessary to be called in the constructor.
This is because when the Airdrop contract is deployed and initialized, the initialize method on the newly created AirdropZap proxy's implementation contract is never called. As such, anyone can call that method and pass in whatever values they want as arguments. If an attacker passes in a contract as argument that calls `selfdestruct`, it will be run in the context of the `AirdropZap` implementation contract and will erase all code from that address.

**Recommendation**

To prevent the implementation contract from being used, you should invoke the `_disableInitializers()` function from Openzeppelin in the constructor to automatically lock it when it is deployed:
 ```solidity
 constructor() {
     _disableInitializers();
 }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-07-Zap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

