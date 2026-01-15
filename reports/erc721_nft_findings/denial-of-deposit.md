---
# Core Classification
protocol: Vault-Tec
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48255
audit_firm: OtterSec
contest_link: N/A
source_link: N/A
github_link: github.com/vault-tec-team/vault-tec-core.

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
finders_count: 3
finders:
  - Robert Chen
  - Woosun Song
  - OtterSec
---

## Vulnerability Title

Denial Of Deposit

### Overview


The report discusses a bug in the MultiRewardsTimeLockPoolV3 contract where users can claim extra rewards if they have a badge token. The amount of bonus is calculated using the getBadgeMultiplier function. However, the gas used in this function is directly proportional to the length of the delegatesOf[_depositorAddress] array. This means that a malicious user can increase the array length and prevent a user from making a deposit. A proof-of-concept is provided where an attacker deploys a fake contract and calls delegateBadgeTo with certain arguments to exhaust the gas and prevent future deposits. The suggested fix is to add a check in the delegateBadgeTo function to only allow holders of valid badges to perform delegations. The bug has been fixed in the latest update of the contract.

### Original Finding Content

## Vulnerability Report: MultiRewardsTimeLockPoolV3

In `MultiRewardsTimeLockPoolV3`, users may claim additional rewards if they are delegated recipients of badge tokens, which are ERC1155 tokens that represent increased shares. The bonus available from badges is calculated using the `getBadgeMultiplier` function.

## Function: getBadgeMultiplier

```solidity
function getBadgeMultiplier(address _depositorAddress) private view returns (uint256) {
    uint256 badgeMultiplier = 0;
    if (ineligibleList[_depositorAddress]) {
        return badgeMultiplier;
    }
    for (uint256 index = 0; index < delegatesOf[_depositorAddress].length; index++) {
        Delegate memory delegateBadge = delegatesOf[_depositorAddress][index];
        BadgeData memory badge = delegateBadge.badge;
        if (IERC1155(badge.contractAddress).balanceOf(delegateBadge.owner, badge.tokenId) > 0) {
            badgeMultiplier = badgeMultiplier + (badgesBoostedMapping[badge.contractAddress][badge.tokenId]);
        }
    }
    return badgeMultiplier;
}
```

The amount of gas used during the execution of this function is linearly proportional to the length of the `delegatesOf[_depositorAddress]` array. Therefore, if a malicious user is capable of arbitrarily increasing the length, they may prevent a user from making a deposit.

## Proof of Concept

1. An attacker deploys the following contract.

```solidity
contract FakeERC1155 {
    function balanceOf(address owner, uint256 tokenId) external view returns (uint256) {
        return 1;
    }
}
```

2. The attacker calls `delegateBadgeTo` with the following arguments:
   - **badgeContract**: The address of the `FakeERC1155` deployed in the previous step.
   - **tokenId**: 0.
   - **delegator**: The target user subject to a denial of deposit.
  
3. The attacker performs step 2 with `tokenIds 1 · · · N`.

4. If **N** is sufficiently large, all of the target user’s future deposits will revert due to gas exhaustion. Our calculations showed that **N ≥ 7000** is sufficient to render the execution of `deposit()` to exceed the current block gas limit of ETH mainnet, which is **30 × 10^6 units**.

Please find the proof-of-concept code in this section.

## Remediation

The following check should be added to the `delegateBadgeTo` function so that only holders of valid badges can perform delegations.

```solidity
require(inBadgesList[_badgeContract][_tokenId], "invalid badge");
```

## Patch

Fixed in commit **74bad90**.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Vault-Tec |
| Report Date | N/A |
| Finders | Robert Chen, Woosun Song, OtterSec |

### Source Links

- **Source**: N/A
- **GitHub**: github.com/vault-tec-team/vault-tec-core.
- **Contest**: N/A

### Keywords for Search

`vulnerability`

