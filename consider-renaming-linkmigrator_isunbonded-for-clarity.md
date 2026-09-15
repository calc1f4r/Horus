---
# Core Classification
protocol: Stakelink Pr152 Linkmigrator
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56941
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md
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
finders_count: 2
finders:
  - Immeas
  - holydevoti0n
---

## Vulnerability Title

Consider renaming `LINKMigrator::_isUnbonded` for clarity

### Overview

See description below for full details.

### Original Finding Content

**Description:** In the `LINKMigrator` contract, the function [`_isUnbonded`](https://github.com/stakedotlink/contracts/blob/0bd5e1eecd866b2077d6887e922c4c5940a6b452/contracts/linkStaking/LINKMigrator.sol#L132-L137) checks whether a user is currently within the claim period for Chainlink staking:

```solidity
function _isUnbonded(address _account) private view returns (bool) {
    uint256 unbondingPeriodEndsAt = communityPool.getUnbondingEndsAt(_account);
    if (unbondingPeriodEndsAt == 0 || block.timestamp < unbondingPeriodEndsAt) return false;

    return block.timestamp <= communityPool.getClaimPeriodEndsAt(_account);
}
```

While functionally correct, the name `_isUnbonded` may not clearly convey its purpose, as it specifically checks whether a user is in the claim period. For improved clarity and consistency with Chainlink’s naming convention—such as in [`StakingPoolBase::_inClaimPeriod`](https://etherscan.io/address/0xbc10f2e862ed4502144c7d632a3459f49dfcdb5e#code)—renaming it could make the intent more immediately clear:

```solidity
function _inClaimPeriod(Staker storage staker) private view returns (bool) {
  if (staker.unbondingPeriodEndsAt == 0 || block.timestamp < staker.unbondingPeriodEndsAt) {
    return false;
  }

  return block.timestamp <= staker.claimPeriodEndsAt;
}
```

**Recommended Mitigation:** Consider renaming `_isUnbonded` to `_inClaimPeriod` to better reflect its logic and improve code readability.

**stake.link:**
Fixed in [`9d710bf`](https://github.com/stakedotlink/contracts/commit/9d710bf35304e9b45ed1ad8468714915817904a1)

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Stakelink Pr152 Linkmigrator |
| Report Date | N/A |
| Finders | Immeas, holydevoti0n |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

