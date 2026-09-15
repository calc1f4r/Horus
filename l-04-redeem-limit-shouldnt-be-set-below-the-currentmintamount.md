---
# Core Classification
protocol: Ondo Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6420
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-ondo-finance-contest
source_link: https://code4rena.com/reports/2023-01-ondo
github_link: #l-04-redeem-limit-shouldnt-be-set-below-the-currentmintamount

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
  - leveraged_farming
  - rwa
  - services
  - cdp
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-04] Redeem limit shouldn't be set below the `currentMintAmount`

### Overview

See description below for full details.

### Original Finding Content

The function `setRedeemLimit` is used by the admin to update the amount of token that can be redeemed during one epoch.<br>
A check should be made to ensure the new redeem limit isn't set below the `currentMintAmount`.<br>
As this problem will lead to the users not being able to request redeem their minted amount of cash on the current epoch.

```solidity
contracts/cash/CashManager.sol

// Before
609:  function setRedeemLimit(
610:    uint256 _redeemLimit
612:  ) external onlyRole(MANAGER_ADMIN) {
613:    uint256 oldRedeemLimit = redeemLimit;
614:    redeemLimit = _redeemLimit;
615:    emit RedeemLimitSet(oldRedeemLimit, _redeemLimit);
616:  }

// After 
609:  function setRedeemLimit(
610:    uint256 _redeemLimit
612:  ) external onlyRole(MANAGER_ADMIN) {
613:    require(_redeemLimit > currentMintAmount, "RedeemLimit below the currentMintAmount")
614:    uint256 oldRedeemLimit = redeemLimit;
615:    redeemLimit = _redeemLimit;
616:    emit RedeemLimitSet(oldRedeemLimit, _redeemLimit);
617:  }
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ondo Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-ondo
- **GitHub**: #l-04-redeem-limit-shouldnt-be-set-below-the-currentmintamount
- **Contest**: https://code4rena.com/contests/2023-01-ondo-finance-contest

### Keywords for Search

`vulnerability`

