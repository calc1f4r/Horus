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
solodit_id: 45921
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

Unrestricted “On-Behalf” Borrowing

### Overview


The report discusses a bug found in the code of a financial protocol. This bug allows an attacker to borrow tokens from the protocol on behalf of another user without proper authorization. This means that the attacker can take the borrowed tokens for themselves, leaving the victim with the debt. The report includes a demonstration of how this attack can be carried out. The recommendation is to fix the bug by requiring proper authorization for on-behalf borrowing or disallowing it altogether. The bug has been resolved.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

Evoq.sol → borrow() / internal call _borrow()
PositionsManager.sol → borrowLogic()
These functions allow specifying arbitrary _borrower and _receiver addresses without verifying that msg.sender is actually authorized to borrow on behalf of _borrower. As a result, an attacker can borrow against another user’s collateral, sending the borrowed tokens to themselves.

**Scenario:**

The attacker sees that User A (victim) has a large collateral.
Attacker calls borrow(...) with _borrower = User A and _receiver = Attacker.
Protocol sees User A’s collateral, deems the borrow safe, and transfers tokens to the attacker.
User A is left with the borrowed debt and no tokens.

**PoC: **

```solidity
function testBorrow2Attack() public {
       uint256 amount = 10_000 ether;


       address bob = address(0x1234);
       address alice = address(0xdeff);
       console.log("Bob address:", bob);
       console.log("Alice address:", alice);
       deal(usdc, address(alice), INITIAL_BALANCE * WAD);
       uint256 aliceBalance = ERC20(usdc).balanceOf(address(alice));
       console.log(aliceBalance);
       vm.startPrank(alice);
       ERC20(usdc).approve(address(evoq), 2 * amount);
       evoq.supply(vUsdc, 2 * amount);


       vm.startPrank(bob);


       evoq.borrow(vUsdt, amount, alice, bob);
   }
```
In other words, Alice can supply funds to the protocol, and Bob can borrow funds on behalf of her(bob need not put any collateral into the protocol!). This will also mean that Alice's debt position increases instead of Bob.

**Recommendation**:

Require msg.sender == _borrower or implement a robust delegation (e.g., signed approval) for on-behalf borrowing.
Disallow free-form _borrower unless proper authorization is enforced.

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

