---
# Core Classification
protocol: Fair Funding by Alchemix & Unstoppable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6535
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/42
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-fair-funding-judging/issues/91

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - 0x52
  - ABA
  - jkoppel
  - hickuphh3
  - Ruhum
---

## Vulnerability Title

M-1: Migrator contract lacks sufficient permissions over vault positions

### Overview


The issue M-1 reports that the migrator contract lacks sufficient permissions over vault positions and was found by 0x52, hickuphh3, Ruhum, minhtrng, jkoppel, and ABA. This vulnerability is due to the fact that the `migrate()` function on the migration contract does not have permissions over the vault's shares to liquidate to underlying or yield tokens. This means that funds and positions cannot be successfully migrated. The recommendation to fix this issue is to call `approveWithdraw()` on the migrator contract for all of the vault's shares and consider using `raw_call()` for this function call. Unstoppable-DeFi has confirmed that this is correct and a `delegateCall` should have been used. They have created a pull request to fix this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-fair-funding-judging/issues/91 

## Found by 
0x52, hickuphh3, Ruhum, minhtrng, jkoppel, ABA

## Summary
The migrator contract lacks sufficient permissions over vault shares to successfully perform migration.

## Vulnerability Detail
> Since vault potentially holds an Alchemix position over a long time during which changes at Alchemix could happen, the `migration_admin` has complete control over the vault and its position after giving depositors a 30 day window to liquidate (or transfer with a flashloan) their position if they're not comfortable with the migration.

We see that all that `migrate()` does is to trigger the `migrate()` function on the migration contract. However, no permissions over the vault's shares were given to the migration contract to enable it to say, liquidate to underlying or yield tokens. It also goes against what was intended, that is, _"complete control over the vault and its position"_.

```vyper
@external
def migrate():
    """
    @notice
        Calls migrate function on the set migrator contract.
        This is just in case there are severe changes in Alchemix that
        require a full migration of the existing position.
    """
    assert self.migration_active <= block.timestamp, "migration not active"
    assert self.migration_executed == False, "migration already executed"
    self.migration_executed = True
    Migrator(self.migrator).migrate()
```

## Impact
Funds / positions cannot be successfully migrated due to lacking permissions.

## Code Snippet
https://github.com/sherlock-audit/2023-02-fair-funding/blob/main/fair-funding/contracts/Vault.vy#L545-L556

## Tool used
Manual Review

## Recommendation
In addition to invoking the `migrate()` function, consider calling `approveWithdraw()` on the migrator contract for all of the vault's shares.
https://alchemix-finance.gitbook.io/v2/docs/alchemistv2#approvewithdraw

Also consider using `raw_call()` for this function call because the current `alchemist` possibly reverts, bricking the migration process entirely.

## Discussion

**Unstoppable-DeFi**

This is correct, a `delegateCall` should have been used.

Will fix.

**Unstoppable-DeFi**

https://github.com/Unstoppable-DeFi/fair-funding/pull/6

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Fair Funding by Alchemix & Unstoppable |
| Report Date | N/A |
| Finders | 0x52, ABA, jkoppel, hickuphh3, Ruhum, minhtrng |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-fair-funding-judging/issues/91
- **Contest**: https://app.sherlock.xyz/audits/contests/42

### Keywords for Search

`vulnerability`

