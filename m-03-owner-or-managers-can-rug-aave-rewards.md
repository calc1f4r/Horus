---
# Core Classification
protocol: PoolTogether
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24994
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-04-pooltogether
source_link: https://code4rena.com/reports/2022-04-pooltogether
github_link: https://github.com/code-423n4/2022-04-pooltogether-findings/issues/89

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
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] Owner or Managers can rug Aave rewards

### Overview


This bug report discusses a malicious owner or manager who can steal all Aave rewards that are meant for PoolTogether users. The malicious actor can do this by exploiting a rug vector available in the AaveV3YieldSource.sol file. This file contains a function called `claimRewards()` which allows the caller to send the rewards to an arbitrary address. As a result, the malicious actor can send the rewards to their own address and steal them.

To mitigate this issue, PoolTogether recommends using a `poolAddressesProviderRegistry`-like contract to determine where the rewards should go, instead of letting an address be passed in. This will limit the possibilities of a rug pull. To further reduce the risk, PoolTogether also noted that these rewards are not tokens deposited by the users, so it is less of a concern.

### Original Finding Content

_Submitted by IllIllI, also found by GimelSec_

A malicious owner or manager can steal all Aave rewards that are meant for PoolTogether users.

Even if the user is benevolent the fact that there is a rug vector available may [negatively impact the protocol's reputation](https://twitter.com/RugDocIO/status/1411732108029181960).

### Proof of Concept

```solidity
File: contracts/AaveV3YieldSource.sol   #X

275     function claimRewards(address _to) external onlyManagerOrOwner returns (bool) {
276       require(_to != address(0), "AaveV3YS/payee-not-zero-address");
277   
278       address[] memory _assets = new address[](1);
279       _assets[0] = address(aToken);
280   
281       (address[] memory _rewardsList, uint256[] memory _claimedAmounts) = rewardsController
282         .claimAllRewards(_assets, _to);
```

[AaveV3YieldSource.sol#L275-L282](https://github.com/pooltogether/aave-v3-yield-source/blob/e63d1b0e396a5bce89f093630c282ca1c6627e44/contracts/AaveV3YieldSource.sol#L275-L282)<br>

The `claimRewards()` function allows the caller to send the rewards to an arbitrary address.

### Recommended Mitigation Steps

Use a `poolAddressesProviderRegistry`-like contract to determine where the rewards should go, instead of letting an address be passed in

**[PierrickGT (PoolTogether) acknowledged and commented](https://github.com/code-423n4/2022-04-pooltogether-findings/issues/89):**
 > Governance will own this contract with a multisig that will need 7 signatures out of 11 members before a transaction can be sent, so it limits the possibilities of a rug pull.
> These rewards are not tokens deposited by the users, so it's also less of a concern.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | PoolTogether |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-pooltogether
- **GitHub**: https://github.com/code-423n4/2022-04-pooltogether-findings/issues/89
- **Contest**: https://code4rena.com/reports/2022-04-pooltogether

### Keywords for Search

`vulnerability`

