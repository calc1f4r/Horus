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
solodit_id: 44688
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

TradingStorage implementation contract is left uninitialized

### Overview


The bug report is about a medium severity issue in a contract called TradingStorage. It has been updated to use a new method called `initialize()` which has a modifier called `initializer`. This is recommended by OpenZeppelin to prevent attackers from taking advantage of uninitialized contracts. The report suggests using a specific method from OpenZeppelin's documentation to fix this issue. The bug has been partially fixed in a commit, but there is still a possibility for an attacker to take control of the contract. To fully fix the issue, the deployer needs to make a call to the contract's `initialize()` method, which can be front-run by an attacker. The report recommends using a different approach suggested by OpenZeppelin to disable initializers directly without any other transaction. This will prevent the contract from being dependent on a transaction and avoid being front-run by attackers. The bug has been fully fixed in a later commit.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

TradingStorage contract has been updated to use initialize() method which uses `initializer` modifier. It is recommended in OpenZeppelin’s documentation to not leave implementation contract uninitialised as attacker can take advantage of the same and that may affect the proxy contract. 

**Recommendation**: 

Use this suggested method in OpenZeppelin’s documentation to mitigate this issue.
**Fix-1** : Issue has been partially fixed in commit a72e06b. 
The method `disableInitializers()` is added which needs to be called to disable anyone to call the `initialize` method. 
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
**Fix-2**: Issue fixed in commit 3998b5b

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

