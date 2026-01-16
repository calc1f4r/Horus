---
# Core Classification
protocol: Yearn v2 Vaults
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16951
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Gustavo Grieco
  - Mike Martel
---

## Vulnerability Title

Strategy migrations can be problematic and should be avoided

### Overview


This bug report is about a vulnerability in a software called Vault.vy. It is a low difficulty issue where strategy migrations can have serious effects on the security and correctness of the vaults. The report suggests that governance can trigger a strategy migration using the provided function, however, it is not clear why governance can call it outside of the vault context, which can result in an invalid state of the vault. 

The report recommends two solutions to address this issue. Short-term, it suggests replacing the strategy migration process with a simpler approach, such as retiring old strategies and adding newer ones. Long-term, it recommends reviewing the current vault functionality to identify high-risk operations and simplify its use as much as possible.

### Original Finding Content

## Error Reporting

**Type:** Error Reporting  
**Target:** Vault.vy  

**Difficulty:** Low  

## Description

If they are not performed manually, strategy migrations can have serious effects on the security and correctness of the vaults. It is best to disallow them and to instead force strategies to be re-added.

Governance can trigger a strategy migration using the following function:

```python
@external
def migrateStrategy(oldVersion: address, newVersion: address):
    """
    @notice
    Migrates a Strategy, including all assets from `oldVersion` to
    `newVersion`.
    This may only be called by governance.
    @dev
    Strategy must successfully migrate all capital and positions to new
    Strategy, or else this will upset the balance of the Vault.
    The new Strategy should be "empty" e.g. have no prior commitments to
    this Vault, otherwise it could have issues.
    @param oldVersion The existing Strategy to migrate from.
    @param newVersion The new Strategy to migrate to.
    """
    assert msg.sender == self.governance
    assert newVersion != ZERO_ADDRESS
    assert self.strategies[oldVersion].activation > 0
    assert self.strategies[newVersion].activation == 0
    strategy: StrategyParams = self.strategies[oldVersion]
    ...
    Strategy(oldVersion).migrate(newVersion)
    log StrategyMigrated(oldVersion, newVersion)
    for idx in range(MAXIMUM_STRATEGIES):
        if self.withdrawalQueue[idx] == oldVersion:
            self.withdrawalQueue[idx] = newVersion
    return  # Don't need to reorder anything because we swapped
```

**Figure 9.1:** Part of the `migrateStrategy` function in a vault

As the documentation states, governance should carefully perform the migration process to make sure that all assets are migrated to a new address and that the address has never interacted with the vault. If either of these conditions is not met, the vault can enter an invalid state.

Also note that governance can manually trigger a migration on a strategy itself instead of using a function in the vault:

```python
function migrate(address _newStrategy) external {
    require(msg.sender == address(vault) || msg.sender == governance());
    require(BaseStrategy(_newStrategy).vault() == vault);
    prepareMigration(_newStrategy);
    SafeERC20.safeTransfer(want, _newStrategy, want.balanceOf(address(this)));
}
```

**Figure 9.2:** The `migrate` function in the base strategy

However, it is unclear why governance is able to call `migrate` outside of the vault context, as updates to vault values may not occur as intended, resulting in an incoherent vault state.

## Exploit Scenario

A strategy is migrated to a newer version. However, because some of the invariants are not checked, the vault enters an invalid state. As a result, all the strategies have to be removed, and the vault should be redeployed.

## Recommendations

- **Short term:** Consider replacing the strategy migration process with a simpler approach in which old strategies are retired and newer ones are added.
- **Long term:** Review the current vault functionality to identify high-risk operations and simplify its use as much as possible.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Yearn v2 Vaults |
| Report Date | N/A |
| Finders | Gustavo Grieco, Mike Martel |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf

### Keywords for Search

`vulnerability`

