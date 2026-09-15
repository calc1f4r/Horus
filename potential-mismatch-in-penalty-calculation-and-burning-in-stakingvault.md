---
# Core Classification
protocol: Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51792
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/altcoinist/staking
source_link: https://www.halborn.com/audits/altcoinist/staking
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
  - Halborn
---

## Vulnerability Title

Potential Mismatch in Penalty Calculation and Burning in StakingVault

### Overview


The report highlights a potential issue in the `penalizeUser` function of the StakingVault contract. The penalty calculation is done in assets, but it is burned in shares, which could lead to inconsistencies. This could result in unfair penalties for users and potentially cause the contract to revert in extreme cases. The report recommends consistently calculating the penalty in either assets or shares and converting it if necessary before burning. A suggested fix is provided, which includes adding a check to ensure the calculated penalty in shares does not exceed the user's balance. The issue has been solved by the Altcoinist team.

### Original Finding Content

##### Description

In the `penalizeUser` function of the StakingVault contract, there's a potential mismatch between how the penalty is calculated and how it's applied. The penalty is calculated in terms of assets, but it's burned in terms of shares, which could lead to inconsistencies.

  

`- src/StakingVault.sol`

```
if (deposits[owner] < balanceInAssets) {
    penalty = Math.min(
        balanceInAssets - deposits[owner],
        (inactivityRatio * balanceOf(owner)) / 1e18
    );
    _burn(owner, penalty);
}
```

The `penalty` is calculated as the minimum of two values:

1. The difference between the balance in assets and the deposits (in assets)
2. A proportion of the user's balance (in shares)

However, the `_burn` function is then called with this `penalty` value, which burns shares, not assets.

This mismatch could lead to incorrect penalty applications:

1. When the share price is greater than 1, users might be penalised more heavily than intended.
2. In extreme cases, the contract might attempt to burn more shares than the user has, potentially causing a revert

This inconsistency could lead to unfair penalties.

##### BVSS

[AO:A/AC:L/AX:L/R:N/S:U/C:N/A:L/I:N/D:M/Y:N (5.6)](/bvss?q=AO:A/AC:L/AX:L/R:N/S:U/C:N/A:L/I:N/D:M/Y:N)

##### Recommendation

To address the issue, the penalty calculation should be consistently done in either assets or shares, and then converted if necessary before burning. Here's a suggested fix:

```
if (deposits[owner] < balanceInAssets) {
    uint256 penaltyInAssets = Math.min(
        balanceInAssets - deposits[owner],
        (inactivityRatio * balanceInAssets) / 1e18
    );
    uint256 penaltyInShares = _convertToShares(penaltyInAssets, Math.Rounding.Up);
    _burn(owner, penaltyInShares);
}
```

Additionally, consider adding a check to ensure the calculated penalty in shares doesn't exceed the user's balance:

```
penaltyInShares = Math.min(penaltyInShares, balanceOf(owner));
```

##### Remediation

**SOLVED:** The suggested mitigation was implemented by the **Altcoinist team.**

##### Remediation Hash

<https://github.com/altcoinist-com/contracts/commit/3a82adceeb2934e25b2996f2382b1294fc20afce>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Staking |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/altcoinist/staking
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/altcoinist/staking

### Keywords for Search

`vulnerability`

