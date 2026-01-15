---
# Core Classification
protocol: Xyro
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45666
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-29-Xyro.md
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
  - Zokyo
---

## Vulnerability Title

Users can lose funds due to `safeTransferFrom` after approval.

### Overview


This bug report is about a critical issue in the `deposit()` function of the `Treasury.sol` smart contract. The function uses a `safeTransferFrom()` call and allows anyone to call it, which can lead to a front-running attack. This means that someone could transfer funds from a user's account without their permission. The same issue is also present in the `depositWithPermit()` function. To fix this, the report recommends implementing a deposit function in each game contract or adding an access restriction to the `deposit()` function to only allow game contracts to use it. The bug has been resolved.

### Original Finding Content

**Severity**: Critical	

**Status**: Resolved

**Description**

The `deposit()` function within the `Treasury.sol` smart contract implements a `safeTransferFrom()` call:
```solidity
function deposit(uint256 amount, address from) public {
       SafeERC20.safeTransferFrom(
           IERC20(approvedToken),
           from,
           address(this),
           amount * 10 ** IERC20Mint(approvedToken).decimals()
       );
   }
```

As can be seen, the `from` is specified within the function's parameters, and the function is public and callable by anyone.

Consider the following scenario:
Alice approves 1000 tokens to Treasury.sol for any reason.
Any directly calls `deposit()` setting Alice’s address as `from`.
Step 2 can be executed as a front-running attack also.
Alice’s funds are transferred to the Treasury without her being able to withdraw them.

The same issue is present within the `depositWithPermit()` function.

**Recommendation**:

This `deposit()` is used by other contracts to handle player’s deposits, so there are several solutions:
Instead of directly calling Treasury’s deposit function, implement a deposit() function directly in each game contract using msg.sender as `from` parameter.
Add an access restriction modifier to Treasury’s deposit function, where only game’s contracts are allowed to execute the function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Xyro |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-29-Xyro.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

