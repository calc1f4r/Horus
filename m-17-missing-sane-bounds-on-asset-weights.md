---
# Core Classification
protocol: veToken Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6138
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-vetoken-finance-contest
source_link: https://code4rena.com/reports/2022-05-vetoken
github_link: https://github.com/code-423n4/2022-05-vetoken-findings/issues/192

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
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - IllIllI
---

## Vulnerability Title

[M-17] Missing sane bounds on asset weights

### Overview


This bug report is about a vulnerability in the VeTokenMinter smart contract that can cause unexpected amounts of inflation or deflation. The problem is due to the lack of bounds checks in the update function, which allows the admin to set weights to extreme values ranging from zero to the maximum possible. This can lead to an incorrect reward calculation by the reward contract, resulting in excessive inflation or deflation. The issue was discovered through code inspection and can be mitigated by having sane upper and lower limits on the values.

### Original Finding Content

_Submitted by IllIllI_

The admin may fat-finger a change, or be malicious, and have the weights be extreme - ranging from zero to `type(uint256).max`, which would cause the booster to pay out unexpected amounts

### Proof of Concept

No bounds checks in the update function:

```
File: contracts/VeTokenMinter.sol   \#1

41       function updateveAssetWeight(address veAssetOperator, uint256 newWeight) external onlyOwner {
42           require(operators.contains(veAssetOperator), "not an veAsset operator");
43           totalWeight -= veAssetWeights[veAssetOperator];
44           veAssetWeights[veAssetOperator] = newWeight;
45           totalWeight += newWeight;
46       }
```

<https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/contracts/VeTokenMinter.sol#L41-L46>

The value is used by the reward contract to determine how much to mint:

```
File: contracts/Booster.sol   \#2

598       function rewardClaimed(
599           uint256 _pid,
600           address _address,
601           uint256 _amount
602       ) external returns (bool) {
603           address rewardContract = poolInfo[_pid].veAssetRewards;
604           require(msg.sender == rewardContract || msg.sender == lockRewards, "!auth");
605           ITokenMinter veTokenMinter = ITokenMinter(minter);
606           //calc the amount of veAssetEarned
607           uint256 _veAssetEarned = _amount.mul(veTokenMinter.veAssetWeights(address(this))).div(
608               veTokenMinter.totalWeight()
609           );
610           //mint reward tokens
611           ITokenMinter(minter).mint(_address, _veAssetEarned);
```

<https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/contracts/Booster.sol#L598-L611>

Wrong values will lead to excessive inflation/deflation.

### Recommended Mitigation Steps

Have sane upper/lower limits on the values.

**[solvetony  (veToken Finance) confirmed, but disagreed with severity and commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/192#issuecomment-1156727045):**
 > We may consider adding this.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/192#issuecomment-1193438892):**
 > The warden has shown how due to a lack of checks certain assets may provide a disproportionate amount of rewards.
> 
> Because this is contingent on an admin mistake, and the impact would be loss or gain of Yield; I believe Medium Severity to be appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | veToken Finance |
| Report Date | N/A |
| Finders | IllIllI |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-vetoken
- **GitHub**: https://github.com/code-423n4/2022-05-vetoken-findings/issues/192
- **Contest**: https://code4rena.com/contests/2022-05-vetoken-finance-contest

### Keywords for Search

`vulnerability`

