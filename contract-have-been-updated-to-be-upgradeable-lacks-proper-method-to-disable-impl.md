---
# Core Classification
protocol: Narwhal Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44692
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal Finance.md
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

Contract have been updated to be upgradeable lacks proper method to disable implementation contracts’ initialize(...) method

### Overview


This bug report discusses an issue with the latest code update, where several contracts have been made upgradeable using OpenZeppelin Upgradeable library. However, the current approach used to disable the initialize() method in these contracts still leaves a risk of an attacker taking control over the implementation contract. This can be fixed by using a different approach, which has now been implemented in the code. 

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

In the latest commit a72e06b, several contracts have been made upgradeable using OpenZeppelin Upgradeable library.
Following are the contracts which are made upgradeable:
NarhwalRefferals
NarwhalTrading
NarwhalTradingCallbacks
TradingStorage
As it is recommended in OpenZeppelin’s documentation to not leave implementation contract uninitialised as attacker can take advantage of the same and that may affect the proxy contract. 
Because of the same reason, all of the above mentioned contracts use `disableInitializer()` method to disable the initialize() method. 
This approach does not resolve the issue completely and still put the risk of attacker taking control over the implementation contract. Let us look what happens when contracts are deployed.
When the proxy and implementation contract is deployed, initialization will be done in the context of proxy contract but not implementation contract.
Implementation contract will have  `storageT` as address(0) as it is not initialized.
Deployer can call `disableInitializers()` only if `gov` is set but it will revert as `storageT` is not set only.
Deployer will need to make a call to implementation contract’s `initialize(...)` method which can be front-run by Attacker to take control over the implementation contract.
Even if deployer is able to call the initialize(...) method, it will disable the initialize() method after the call. Deployer will not need to call `disableInitializers()` anymore to do so.
This is the exact reason why OpenZeppelin suggests to use the following:
```solidity
/// @custom:oz-upgrades-unsafe-allow constructor
constructor() {
_disableInitializers();
}
```
Using this approach will disable the initializers for the implementation contracts directly without any other transaction. The above approach is suggested as well to avoid being dependent on a transaction to disable the initializer or being front-run by attackers.
**Fixed**: Issue fixed in commit 3998b5b

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Narwhal Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

