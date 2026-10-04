---
# Core Classification
protocol: stHYPE_2025-10-13
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63213
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/stHYPE-security-review_2025-10-13.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Incorrect management of redeemable funds

### Overview


This report explains a bug that was found and resolved in the code for a smart contract. The issue was that the code did not take into account that new fees may have been withdrawn, leaving insufficient funds for earlier transactions. This could cause problems with redeeming tokens and could potentially result in lost funds. A solution was proposed to add a condition to the code to prevent this from happening. It was also recommended to adjust the withdrawal of fees and not take into account pending fees when checking if a transaction can be redeemed. 

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

`Overseer._redeemable()` checks if a burn can be redeemed by making sure that the contract has enough balance to cover the burn amount minus already redeemed amounts and pending protocol fees.

```solidity
    function _redeemable(uint256 burnId) internal view returns (bool) {
        uint256 sum = burns[burnId].sum;
        uint256 difference = sum < redeemed ? 0 : sum - redeemed;
        return burns[burnId].completed == false && difference + protocolPendingFee <= address(this).balance;
    }
```

This calculation assumes that any redemption with a higher burn ID has left enough balance for all previous burns to be redeemed, which is correct. However, it does not take into account that after that, new fees may have been accrued and withdrawn, which would leave an insufficient balance for the earlier burns to be redeemed.

### Proof of concept

```solidity
function test_audit_redeemReverts() public {
	// Setup
	_addStakingModule();
	address[] memory stakingModules = overseer.getStakingModules();
	address stakingModule = stakingModules[0];

	address user1 = makeAddr("user1");
	address user2 = makeAddr("user2");
	address user3 = makeAddr("user3");
	vm.deal(user1, 1 ether);
	vm.deal(user2, 1 ether);
	vm.deal(user3, 1 ether);

	vm.startPrank(gov);
	overseer.setSyncInterval(84_600);
	overseer.grantRole(overseer.FEE_RECIPIENT_ROLE(), address(this));
	vm.stopPrank();

	// Users mint stHYPE
	vm.prank(user1);
	overseer.mint{value: 1 ether}(user1);

	vm.prank(user2);
	overseer.mint{value: 1 ether}(user2);

	vm.prank(user3);
	overseer.mint{value: 1 ether}(user3);

	// Deposit to staking module
	Overseer.DepositInput[] memory inputs = new Overseer.DepositInput[](1);
	inputs[0] = Overseer.DepositInput({index: 0, amount: 1 ether, data: ""});
	vm.prank(gov);
	overseer.deposit(inputs);
	CoreSimulatorLib.nextBlock();

	// Simulate the effect of staking to validators
	stakingModule.call{value: 0.01 ether}("");

	// User 1 burns
	vm.prank(user1);
	uint256 user1BurnId = overseer.burn(user1, 1 ether, "");

	// User 2 burns and redeems
	vm.prank(user2);
	overseer.burnAndRedeemIfPossible(user2, 1 ether, "");

	// Rebase accrues protocol fees
	vm.warp(block.timestamp + 84_600);
	vm.prank(gov);
	overseer.rebase();
	
	// Protocol fees are claimed
	overseer.claimFee(0, true);

	// User 1 burn is supposed to be redeemable
	assertTrue(overseer.redeemable(user1BurnId));

	// Redemption reverts due to lack of funds
	vm.prank(user1);
	vm.expectRevert(bytes("Transfer failed"));
	overseer.redeem(user1BurnId);
	assertTrue(address(overseer).balance < 1 ether);
}
```

## Recommendations

A partial fix would be adding the `burns[burnId].amount <= address(this).balance` condition to the `_redeemable()` function. This will prevent the `_redeemable()` function from returning true if the contract does not have enough balance to cover the specific burn amount.

If it is wanted to guarantee redemptions of a burn ID will always allow all previous burns to be redeemed, then the withdrawal of protocol fees should be adjusted to allow withdrawing only when `burns[latestBurnId].sum - redeemed + protocolPendingFee <= address(this).balance`. Additionally, the `protocolPendingFee` should not be taken into account in the `_redeemable()` function when `burnId < latestBurnId`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | stHYPE_2025-10-13 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/stHYPE-security-review_2025-10-13.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

