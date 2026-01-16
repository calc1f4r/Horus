---
# Core Classification
protocol: Nayms 2024 (Retainer)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59473
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nayms-2024-retainer/04e1c37c-19e8-4c7d-b743-268e4a6466c9/index.html
source_link: https://certificate.quantstamp.com/full/nayms-2024-retainer/04e1c37c-19e8-4c7d-b743-268e4a6466c9/index.html
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
finders_count: 3
finders:
  - Roman Rohleder
  - Valerian Callens
  - Jeffrey Kam
---

## Vulnerability Title

User can artificially inflate stake boosts for the next interval by repeating stake and unstake actions

### Overview


The client has identified and fixed a bug in the `contracts-v3/LibTokenizedVaultStaking.sol` file. In the `_unstake()` function, the stake boost for the next `vTokenId` is not being reset to zero, which can lead to an attacker inflating their boost and claiming more rewards than they should be allowed. The recommendation is to reset the boost for the next `vTokenId` to zero in the `unstake()` function. 

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `0aee3f1731d2b22c556c21a5a221eb5b14fedc98`.

**File(s) affected:**`contracts-v3/LibTokenizedVaultStaking.sol`

**Description:** In `_unstake()`, we only set `s.stakeBoost[vTokenId][_stakerId] = 0;` back to zero, but we do not set the stake boost for the next `vTokenId` back to zero. When a user stake in the current interval, part of the stake boost will be allocated to the next `vTokenId` proportional to the time it was staked between the current interval and the next interval, as shown in the following lines:

```
uint256 boostTotal = (_amount * _getA(_entityId)) / _getD(_entityId);
uint256 boostNext;

if (_isStakingInitialized(_entityId)) {
    boostNext = (boostTotal * (block.timestamp - _calculateStartTimeOfCurrentInterval(_entityId))) / s.stakingConfigs[_entityId].interval;
}

uint256 boost = boostTotal - boostNext;

// give to the staker
s.stakeBoost[vTokenId][_stakerId] += boost;
s.stakeBoost[nextVTokenId][_stakerId] += boostNext;
```

Since the stake boost is never reset for the next `vTokenId`, an attacker can inflate the stake boost for the next interval by repeatedly staking and unstaking in the current interval. Then, at the start of the next interval, an attacker can simply stake a small amount, but he will be able to claim more rewards than should be allowed due to the inflated boost.

**Recommendation:** Consider resetting the boost for the next `vTokenId` back to zero in the function `unstake()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Nayms 2024 (Retainer) |
| Report Date | N/A |
| Finders | Roman Rohleder, Valerian Callens, Jeffrey Kam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nayms-2024-retainer/04e1c37c-19e8-4c7d-b743-268e4a6466c9/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nayms-2024-retainer/04e1c37c-19e8-4c7d-b743-268e4a6466c9/index.html

### Keywords for Search

`vulnerability`

