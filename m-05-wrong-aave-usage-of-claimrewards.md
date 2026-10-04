---
# Core Classification
protocol: Float Capital
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25534
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-08-floatcapital
source_link: https://code4rena.com/reports/2021-08-floatcapital
github_link: https://github.com/code-423n4/2021-08-floatcapital-findings/issues/49

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
  - dexes
  - cdp
  - services
  - derivatives
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-05] Wrong aave usage of `claimRewards`

### Overview


A bug was discovered in the Aave Yield Manager contract, where rewards would be unclaimable. According to Aave's documentation, aToken should be provided, but the code in the contract did not reflect this. The code in the contract was changed to address this issue, and the bug was confirmed by DenhamPreen and Moose-Code from Float. The bug was fixed by changing the code in the contract from `address[] memory rewardsDepositedAssets = new address[](0);` to `address[] memory rewardsDepositedAssets = new address[](1); rewardsDepositedAssets[0] = address(aToken);`.

### Original Finding Content

_Submitted by jonah1005_

Aave yield manager claims rewards with the payment token. According to aave's document, aToken should be provided.
The aave rewards would be unclaimable.

YieldManager's logic in [L161-L170](https://github.com/code-423n4/2021-08-floatcapital/blob/main/contracts/contracts/YieldManagerAave.sol#L161-L170)

Reference: https://docs.aave.com/developers/guides/liquidity-mining#claimrewards

Recommend changing to
```solidity
  address[] memory rewardsDepositedAssets = new address[](1);
  rewardsDepositedAssets[0] = address(aToken);
```

**[DenhamPreen (Float) confirmed](https://github.com/code-423n4/2021-08-floatcapital-findings/issues/49#issuecomment-896811177):**
 > Great catch!
>
> This contract is going to be upgradable but really applicable within this context 👍

**[moose-code (Float) commented](https://github.com/code-423n4/2021-08-floatcapital-findings/issues/49#issuecomment-896845365):**
 > Oof yeah! Good one :)
>
> Devil in those documentation details :)
>
> ![image](https://user-images.githubusercontent.com/20556729/129041188-b712e09a-f735-44d4-922f-328b156e2461.png)



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Float Capital |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-08-floatcapital
- **GitHub**: https://github.com/code-423n4/2021-08-floatcapital-findings/issues/49
- **Contest**: https://code4rena.com/reports/2021-08-floatcapital

### Keywords for Search

`vulnerability`

