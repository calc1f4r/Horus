---
# Core Classification
protocol: Dyad
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41696
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Dyad-security-review.md
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

protocol_categories:
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Liquidated users are wrongly protected from slashing due to incorrect XP update

### Overview


The report describes a bug that occurs when liquidating a vault. Liquidating a vault is supposed to act as both a withdrawal and deposit function, but when withdrawing from a kerosene vault, the note's xp is not affected. This is because the code uses the `updateXP` function instead of the `beforeKeroseneWithdrawn` function. The report recommends fixing this by refactoring the code to use the `beforeKeroseneWithdrawn` function before the `updateXP` function.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

On a base level, liquidating a vault functions as both a `withdraw` and `deposit` function and upon withdrawing from a kerosene vault, the note's xp is slashed. However, during liquidations, this is not done for the liquidated note, as `updateXP` is used instead, rather than the `beforeKeroseneWithdrawn`. As a result, the note xp is not affected even during the pseudowithdrawal.

```solidity
                vault.move(id, to, asset);
                if (address(vault) == KEROSENE_VAULT) {
                    dyadXP.updateXP(id);
                    dyadXP.updateXP(to);
                }
            }
```

## Recommendations

Fixing this might need a bit of refactoring. Something like below will work.

```diff
                vaultAmounts[i] = asset;

-                vault.move(id, to, asset);
-                if (address(vault) == KEROSENE_VAULT) {
-                    dyadXP.updateXP(id);
-                    dyadXP.updateXP(to);
-                }
-            }
+              if (address(vault) == KEROSENE_VAULT) {
+                   dyadXP.beforeKeroseneWithdrawn(id);
+                   vault.move(id, to, asset);//This subtracts from id first and adds to to
+                   dyadXP.updateXP(to);
+               } else {
+               vault.move(id, to, asset);
+           }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Dyad |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Dyad-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

