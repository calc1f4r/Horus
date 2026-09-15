---
# Core Classification
protocol: Benqi Governance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63814
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
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
finders_count: 3
finders:
  - ChainDefenders](https://x.com/defendersaudits) ([0x539](https://x.com/1337web3) & [PeterSR
  - Giovanni Di Siena
  - Jorge
---

## Vulnerability Title

Missing interface compliance validation in `DistributorManager`

### Overview

See description below for full details.

### Original Finding Content

**Description:** The `DistributionManager` contract does not currently validate that the `budgetAllocator` and controller module contracts implement the required interfaces when set during initialization or via `setBudgetAllocator()` and `setModuleForController()` respectively. Both the `UnifiedBudgetAllocator` and `BenqiCoreModule` contracts implement `ERC165::supportsInterface` to declare interface compliance; however, the setter functions do not verify this before accepting the contracts as valid.

```solidity
// DistributionManager.sol
function _setBudgetAllocator(IBudgetAllocator _budgetAllocator) internal {
    if (address(_budgetAllocator) == address(0)) revert InvalidAddress("budgetAllocator");

    // @audit -  missing interface validation check

    address oldAllocator = address(budgetAllocator);
    budgetAllocator = _budgetAllocator;

    emit BudgetAllocatorSet(oldAllocator, address(_budgetAllocator));
}

function _setModuleForController(
    address _rewardController,
    IDistributionModule _module
) internal {
    if (_rewardController == address(0)) revert InvalidAddress("rewardController");
    if (address(_module) == address(0)) revert InvalidAddress("module");

    // @audit -  missing interface validation check

    if (address(rewardControllerToModule[_rewardController]) != address(0)) {
        revert ControllerAlreadyRegistered(_rewardController);
    }

    _activeRewardControllers.add(_rewardController);
    rewardControllerToModule[_rewardController] = _module;

    emit ModuleForControllerSet(_rewardController, address(_module));
}
```

**Impact:** Setting an incompatible contract would completely DoS the distribution system.

**Recommended Mitigation:** Add ERC-165 interface validation checks to both setter functions:

```soldity
if (!IERC165(address(_budgetAllocator)).supportsInterface(type(IBudgetAllocator).interfaceId)) {
      revert InvalidInterface("budgetAllocator");
}
```

**BENQI:** Acknowledged.

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Benqi Governance |
| Report Date | N/A |
| Finders | ChainDefenders](https://x.com/defendersaudits) ([0x539](https://x.com/1337web3) & [PeterSR, Giovanni Di Siena, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

