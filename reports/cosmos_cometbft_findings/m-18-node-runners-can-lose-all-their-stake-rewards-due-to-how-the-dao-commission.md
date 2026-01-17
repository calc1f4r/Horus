---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: uncategorized
vulnerability_type: min/max_cap_validation

# Attack Vector Details
attack_type: min/max_cap_validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5926
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/190

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
  - min/max_cap_validation

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - pashov
  - sahar
  - yixxas
  - cccz
  - joestakey
---

## Vulnerability Title

[M-18] Node runners can lose all their stake rewards due to how the DAO commissions can be set to a 100%

### Overview


This bug report concerns a vulnerability in the LiquidStakingManager.sol code which allows the DAO (Decentralized Autonomous Organization) to take all of the stake rewards from node runners. The vulnerability is that there is no limit to the amount of commission the DAO can take, and it can be set to a 100%. This percentage is used to calculate the amount of rewards the DAO will take, leaving the node runner with 0 rewards. The recommended mitigation step is to set a maximum cap on the amount of commission the DAO can take from node runners. The vulnerability was identified using manual review.

### Original Finding Content


Node runners can have all their stake rewards taken by the DAO as commissions can be set to a 100%.

### Proof of Concept

There is no limits on `_updateDAORevenueCommission()` except not exceeding `MODULO`, which means it can be set to a 100%.

[LiquidStakingManager.sol#L948-L955](https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/LiquidStakingManager.sol#L948-L955)

```solidity
    function _updateDAORevenueCommission(uint256 _commissionPercentage) internal {
        require(_commissionPercentage <= MODULO, "Invalid commission");

        emit DAOCommissionUpdated(daoCommissionPercentage, _commissionPercentage);

        daoCommissionPercentage = _commissionPercentage;
    }
```

This percentage is used to calculate `uint256 daoAmount = (_received * daoCommissionPercentage) / MODULO` in `_calculateCommission()`.<br>
Remaining is then calculated with `uint256 rest = _received - daoAmount`, and in this case `rest = 0`.<br>
When node runner calls `claimRewardsAsNodeRunner()`, the node runner will receive 0 rewards.<br>

### Recommended Mitigation Steps

There should be maximum cap on how much commission DAO can take from node runners.

**[vince0656 (Stakehouse) disputed and commented](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/190#issuecomment-1329453031):**
  > Node runners can see ahead of time what the % commission is and therefore, they can make a decision based on that. However, on reflection, a maximum amount is not a bad idea.

**[LSDan (judge) commented](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/190#issuecomment-1335557923):**
 > I will leave this in place as I think it's a valid concern. If the DAO is compromised ([specifically included in scope](https://github.com/code-423n4/2022-11-stakehouse#objectives)), the impact is felt immediately and applies to all unclaimed rewards. The node runners can't necessarily see a high fee rate coming in advance.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | pashov, sahar, yixxas, cccz, joestakey |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/190
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Min/Max Cap Validation`

