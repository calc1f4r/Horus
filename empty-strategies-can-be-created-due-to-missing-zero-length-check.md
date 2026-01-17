---
# Core Classification
protocol: Octodefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61608
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
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
  - oracle

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Giovanni Di Siena
  - Farouk
---

## Vulnerability Title

Empty strategies can be created due to missing zero length check

### Overview

See description below for full details.

### Original Finding Content

**Description:** `StrategyBuilderPlugin.createStrategy()` does not currently revert if the `steps` array length is zero. This means strategies can be created that can never be deleted, per the `strategyExist` modifier logic that is applied to `StrategyBuilderPlugin.deleteStrategy()` checking the steps length (which is not enforced to be non-zero):

```solidity
modifier strategyExist(address wallet, uint32 id) {
    if (strategies[getStorageId(wallet, id)].steps.length == 0) {
        revert StrategyDoesNotExist();
    }
    _;
}
```

**Impact:** Impact is limited as strategies cannot be created on behalf of other wallets; however this behavior is most likely undesirable.

**Proof of Concept:** The following test can be added to `StrategyBuilderPlugin.t.sol`:

```solidity
function test_createStrategy_Empty() external {
    uint256 numSteps;
    IStrategyBuilderPlugin.StrategyStep[] memory steps = _createStrategySteps(numSteps);

    uint32 strategyID = 222;
    vm.prank(address(account1));
    strategyBuilderPlugin.createStrategy(strategyID, creator, steps);

    //Assert
    IStrategyBuilderPlugin.Strategy memory strategy = strategyBuilderPlugin.strategy(address(account1), strategyID);

    assertEq(strategy.creator, creator);
    assertEq(strategy.steps.length, numSteps);

    vm.prank(address(account1));
    vm.expectRevert(IStrategyBuilderPlugin.StrategyDoesNotExist.selector);
    strategyBuilderPlugin.deleteStrategy(strategyID);
}

function test_createStrategy_EmptyNonZeroLength() external {
    uint256 numSteps = 2;
    IStrategyBuilderPlugin.StrategyStep[] memory steps = new IStrategyBuilderPlugin.StrategyStep[](numSteps);

    uint32 strategyID = 222;
    vm.prank(address(account1));
    strategyBuilderPlugin.createStrategy(strategyID, creator, steps);

    //Assert
    IStrategyBuilderPlugin.Strategy memory strategy = strategyBuilderPlugin.strategy(address(account1), strategyID);

    assertEq(strategy.creator, creator);
    assertEq(strategy.steps.length, numSteps);

    vm.prank(address(account1));
    strategyBuilderPlugin.executeStrategy(strategyID);

    vm.prank(address(account1));
    strategyBuilderPlugin.deleteStrategy(strategyID);
}
```

**Recommended Mitigation:** Consider reverting if the `steps` length is zero. Note that it would still be possible to create what is effectively an empty strategy with non-zero array length by leveraging default condition address as the zero address as shown in the second PoC.

**OctoDeFi:** Fixed in PR [\#20](https://github.com/octodefi/strategy-builder-plugin/pull/20).

**Cyfrin:** Verified. Additional validation has been implemented to prevent empty strategy steps without conditions or actions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Octodefi |
| Report Date | N/A |
| Finders | Giovanni Di Siena, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

