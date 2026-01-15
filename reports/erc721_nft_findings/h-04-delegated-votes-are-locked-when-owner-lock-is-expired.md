---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26972
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-verwa
source_link: https://code4rena.com/reports/2023-08-verwa
github_link: https://github.com/code-423n4/2023-08-verwa-findings/issues/268

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 20
finders:
  - popular00
  - seerether
  - qpzm
  - kaden
  - Tendency
---

## Vulnerability Title

[H-04] Delegated votes are locked when owner lock is expired

### Overview


This bug report is about a vulnerability in the VoteEscrow.sol code, which is part of veRWA, a decentralized voting system. The vulnerability is that if a user forgets to undelegate their locked votes before the lock expires, their tokens are essentially locked forever. This means that they will not be able to call the `withdraw()` function to exit the system.

This vulnerability was discovered by running the `forge test --match-test testUnSuccessUnDelegate` test, which is part of VoteEscrow.t.sol. This test showed that when a user tried to undelegate after their lock had expired, they received a "Delegatee lock expired" error.

The recommended mitigation step is to refactor the code to skip the `toLocked.end > block.timestamp` check when undelegating. This could be done by adding a small delay (e.g., 1 second) to the lock end time when a user undelegates. This would ensure that users are not locked out of the system if they forget to undelegate before their lock expires.

### Original Finding Content


<https://github.com/code-423n4/2023-08-verwa/blob/a693b4db05b9e202816346a6f9cada94f28a2698/src/VotingEscrow.sol#L331> 

<https://github.com/code-423n4/2023-08-verwa/blob/a693b4db05b9e202816346a6f9cada94f28a2698/src/VotingEscrow.sol#L371-L374>

<https://github.com/code-423n4/2023-08-verwa/blob/a693b4db05b9e202816346a6f9cada94f28a2698/src/VotingEscrow.sol#L383>

In `delegate()` of VoteEscrow\.sol, a user is able to delegate their locked votes to someone else, and undelegate (i.e. delegate back to themselves). When the user tries to re-delegate, either to someone else or themselves, the lock must not be expired. This is problematic because if a user forgets and lets their lock become expired, they cannot undelegate. This blocks withdrawal, which means their tokens are essentially locked forever.

### Proof of Concept

To exit the system, Alice must call `withdraw()`. However, since they've delegated, they will not be able to.

<details>

```solidity
function withdraw() external nonReentrant {
	...
	require(locked_.delegatee == msg.sender, "Lock delegated");
	...
}
```

To re-delegate to themselves (undelegate), they call `delegate(alice.address)`. However, there is a check to see if `toLocked.end` has expired, which would be true since it would point to Alice's lock.

    function delegate(address _addr) external nonReentrant {
    	LockedBalance memory locked_ = locked[msg.sender];
    	...
    	LockedBalance memory fromLocked;
    	LockedBalance memory toLocked;
    	locked_.delegatee = _addr;
    	if (delegatee == msg.sender) {
    		...
    	// @audit this else if will execute
    	} else if (_addr == msg.sender) {
    		// Undelegate
    		fromLocked = locked[delegatee]; // @audit Delegatee
    		toLocked = locked_; // @audit Alice's lock
    	}
    	...
    	require(toLocked.end > block.timestamp, "Delegatee lock expired");

This is a test to be added into VoteEscrow\.t.sol. It can be manually run by executing `forge test --match-test testUnSuccessUnDelegate`.

```solidity
function testUnSuccessUnDelegate() public {
	testSuccessDelegate();
	vm.warp(ve.LOCKTIME() + 1 days);

	// Try to undelegate
	vm.startPrank(user1);
	vm.expectRevert("Delegatee lock expired");
	ve.delegate(user1);

	// Still user2
	(, , , address delegatee) = ve.locked(user1);
	assertEq(delegatee, user2);
}
```
</details>

### Recommended Mitigation Steps

Consider refactoring the code to skip `toLocked.end > block.timestamp` if undelegating. For example, adding a small delay (e.g., 1 second) to the lock end time when a user undelegates.

**[alcueca (Judge) commented](https://github.com/code-423n4/2023-08-verwa-findings/issues/268#issuecomment-1694504863):**
 > This vulnerability, if not found, would have meant that some users would have permanently lost assets in the form of voting power. While at that point the application owners would certainly warn users to not let their locks expire without undelegating, many users would not get the warning, as it is not that easy to make sure that every user is aware of something. The result is that time and again, users would get their tokens locked forever.

**[OpenCoreCH (veRWA) confirmed on duplicate 112](https://github.com/code-423n4/2023-08-verwa-findings/issues/112)**


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | popular00, seerether, qpzm, kaden, Tendency, ltyu, KmanOfficial, carrotsmuggler, 3docSec, MrPotatoMagic, 0xDING99YA, zhaojie, Yuki, bin2chen, pep7siup, 1, 2, mert\_eren, RED-LOTUS-REACH, bart1e |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-verwa
- **GitHub**: https://github.com/code-423n4/2023-08-verwa-findings/issues/268
- **Contest**: https://code4rena.com/reports/2023-08-verwa

### Keywords for Search

`vulnerability`

