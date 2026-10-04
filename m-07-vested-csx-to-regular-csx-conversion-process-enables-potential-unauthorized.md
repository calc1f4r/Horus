---
# Core Classification
protocol: Csx
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44013
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/CSX-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-07] `Vested CSX` to `Regular CSX` Conversion Process Enables Potential Unauthorized Withdrawal of Staked Deposits by Malicious Council

### Overview


The report describes a bug in the CSX protocol that allows the Council role to have too much power, including the ability to withdraw tokens without restrictions and change important contracts. This role can also be mistakenly given to the wrong address. The affected code can be found in two files: VestedStaking.sol and Keepers.sol. The team recommends removing some privileges or implementing a two-step process to transfer the council role. They have acknowledged and fixed the issue.

### Original Finding Content

## Severity

Medium Risk

## Description

Some of the key privileges of the Council role:

- Ability to execute a forced withdrawal of tokens from the contract via `cliff()` function without any restrictions. In the standard `withdraw()` method there is a validation check that requires the vesting period (2 years) to pass before the `Vester` is able to withdraw.
- Ability to change factory and keeper contracts.

Additionally, the Council role can be changed through `changeCouncil()` function and mistakenly a wrong address can be given resulting in this role being set to an unexpected address.

## Location of Affected Code

File: [VestedStaking.sol#L191](https://github.com/csx-protocol/csx-contracts/blob/bc51a67ccff86f2c691375f3cc92ee8c0a9fc369/contracts/CSX/VestedStaking.sol#L191)

```solidity
/// @notice Executes a forced withdrawal of tokens from the contract.
/// @dev Can only be called by the council to mitigate against malicious vesters.
/// @param amount Specifies the amount of tokens to be withdrawn.
function cliff(uint256 amount) external onlyCouncil {
  if (amount > vesting.amount || amount == 0) {
    revert NotEnoughTokens();
  }
  vesting.amount -= amount;
  cliffedAmount += amount;
  sCsxToken.unStake(amount);
  csxToken.safeTransfer(msg.sender, amount);
  emit Cliff(msg.sender, amount, vesting.amount);
}
```

File: [Keepers.sol#L94](https://github.com/csx-protocol/csx-contracts/blob/bc51a67ccff86f2c691375f3cc92ee8c0a9fc369/contracts/Keepers/Keepers.sol#L94)

```solidity
function changeCouncil(address _newCouncil) public onlyCouncil {
  if (_newCouncil == address(0)) {
    revert NotCouncil();
  }
  council = _newCouncil;
  emit CouncilChanged(_newCouncil);
}
```

## Recommendation

There are two vectors to resolve the risks:

1. Consider removing some owner privileges or using a `Timelock` contract.
2. It is recommended to implement a two-step process where the council nominates an account, and the nominated account needs to call an `acceptCouncilRole()` function for the transfer of the council role to succeed fully. This ensures the nominated `EOA` account is valid and active.

## Team Response

Acknowledged and fixed as proposed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Csx |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/CSX-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

