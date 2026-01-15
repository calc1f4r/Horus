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
solodit_id: 51785
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/altcoinist/staking
source_link: https://www.halborn.com/audits/altcoinist/staking
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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Users can stake without an active subscription to the author

### Overview


The bug report describes an issue in the `StakingVault::_deposit` function where a subscriber can stake in an author's pool without an active subscription. This allows them to accrue rewards without being eligible to claim them until they renew their subscription. The report suggests adding a check to ensure that the subscriber has an active subscription before they can stake. The Altcoinist team has already applied the suggested mitigation.

### Original Finding Content

##### Description

To stake, a subscriber must have an active subscription to the author.

However, in the `StakingVault::_deposit` function, the following checks are used to restrict staking:

```
require(author != address(0), "UI");
require(authorTokenFactory.balanceOf(receiver, uint256(uint160(author))) > 0, "PD");
```

First, the function ensures the author's address is non-zero, and then checks if the subscriber holds an ERC1155 token corresponding to the author. This token is minted when a user subscribes to the author for the first time. However, this mechanism does not guarantee that the subscriber currently has an active subscription.

Due to this flaw, a past subscriber can stake in the author's pool and accrue rewards without an active subscription. These rewards cannot be redeemed until the subscriber renews the subscription. Once renewed, the subscriber becomes eligible to claim the rewards earned during the inactive subscription period.

##### Proof of Concept

Add the following function to the test PoC file:

```
function test_stake_noSub() public postTGE {
        console.log("========  Day 1  ======== ");
        console.log("[+] Alice buys 1 month Sub and stakes 10,000 ALTT");
        _subscribe(alice, carol, SubscribeRegistry.packages.MONTHLY, 1, 10000e18, address(0), true);

        skip(30 days);

        console.log("========  Day 31 ======== ");
        deal(address(altt), alice, 500e18);
        console.log("[+] Alice stakes 500 ALTT more even if her subscription is expired");
        vm.startPrank(alice);
        altt.approve(address(authorVault), 500e18);
        IERC4626(authorVault).deposit(500e18, alice);
}
```

Run `forge test --mt "test_stake_noSub" -vvv`

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:N/D:N/Y:H/R:N/S:U (8.8)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:N/D:N/Y:H/R:N/S:U)

##### Recommendation

Add the following check to `StakingVault::_deposit()`:

```
require(registry.getSubDetails(author, owner) > block.timestamp);
```

This ensures that the staker has an active subscription before they stake.

##### Remediation

**SOLVED:** The suggested mitigation was applied by the **Altcoinist team**.

##### Remediation Hash

<https://github.com/altcoinist-com/contracts/commit/aeeccfb46664a9c9ed8803d1b9eff2c1c2a05801>

##### References

[altcoinist-com/contracts/src/StakingVault.sol#L94](https://github.com/altcoinist-com/contracts/blob/master/src/StakingVault.sol#L94)

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

