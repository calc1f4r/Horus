---
# Core Classification
protocol: Tanssi_2025-04-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63310
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Tanssi-security-review_2025-04-30.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-14] Pending slashes are not taken into account

### Overview

See description below for full details.

### Original Finding Content


`Middleware.sol` uses `IBaseDelegator(IVault(vault).delegator()).stakeAt()` to decide the max slashable amount:

```solidity
        uint256 vaultStake = IBaseDelegator(IVault(vault).delegator()).stakeAt(
            subnetwork, params.operator, params.epochStartTs, new bytes(0)
        );
```

When using a VetoSlasher, pending slashes are not reflected in the `stake()`/`stakeAt()` calls. This is explicitly mentioned in the [Symbiotic documentation](https://docs.symbiotic.fi/manuals/network-manual#:~:text=You%20are%20aware,slashings%E2%80%99%20processing%20logic.):

> "You are aware that NetworkRestakeDelegator.stakeAt()/FullRestakeDelegator.stakeAt() (the function returning a stake for an Operator in your Network) counts the whole existing money as a real stake, meaning that it doesn’t take into account pending slashings from you or your 'neighbor' Networks. Hence, it should be covered by your Middleware, depending on the Vault’s type and your slashings’ processing logic."

This can lead to several issues:

- Since slashing is applied as a percentage, if a validator is slashed multiple times within a single epoch (which is possible because the Tanssi chain executes the validator's maximum slash from the previous era(capped at 75%) at the start of each era), and an epoch contains multiple eras, then both slashes may end up using the same stake amount. If the time between vetoSlasher.requestSlash and vetoSlasher.executeSlash spans more than one era, both slashes might be executed based on the stake from the first slash. If the combined slash percentage exceeds 50%, the second slash may fail.
- Validators may be considered opted-in and slashable when they should not be, due to pending slashings not being accounted for in the stake calculation.

Recommendations:

It's not possible/feasible to track pending slashes from external networks. This is simply a weakness of the symbiotic protocol. 





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tanssi_2025-04-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Tanssi-security-review_2025-04-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

