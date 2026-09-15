---
# Core Classification
protocol: VTVL
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47911
audit_firm: OtterSec
contest_link: https://vtvl.io/
source_link: https://vtvl.io/
github_link: https://github.com/VTVL-co/vtvl-smart-contracts/tree/audit-ready-jul-23

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
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Inaccurate Withdrawable Token Amount

### Overview


The bug report discusses an issue in the BaseMilestone contract where some tokens may become locked and unable to be withdrawn by the contract owner. This is caused by the contract not accurately tracking the tokens deposited by each recipient. To fix this, the availableAmount calculation in the withdrawAdmin function should consider both the contract balance and the amount of tokens reserved for vesting. This issue has been fixed in recent commits by considering all relevant factors when calculating the remaining withdrawable amount.

### Original Finding Content

## Token Withdrawal Issue in BaseMilestone Contract

In `BaseMilestone::withdrawAdmin`, the `availableAmount` is calculated as:

```
allocation * recipients.length - numTokensReservedForVesting.
```

This may result in locking some tokens that are not reserved for vesting.

## BaseMilestone.sol (SOLIDITY)

```solidity
function withdrawAdmin() public onlyOwner {
    uint256 availableAmount = allocation * recipients.length -
    numTokensReservedForVesting;
    tokenAddress.safeTransfer(msg.sender, availableAmount);
    emit AdminWithdrawn(_msgSender(), availableAmount);
}
```

The issue arises as the contract does not accurately track the actual tokens deposited by each recipient. It only keeps track of the total tokens reserved for vesting (`numTokensReservedForVesting`) across all milestones. Due to this, there may be instances where the contract mistakenly treats some tokens as reserved for vesting even though they have not been assigned to any specific recipient. As a result, these unassigned tokens are effectively locked and may not be withdrawn by the contract owner.

## Remediation

Calculate `availableAmount` considering both the current contract balance and the amount of tokens reserved for vesting. By doing so, the accurate amount withdrawable will be determined, preventing any unnecessary locking of funds beyond what is already reserved for vesting.

## BaseMilestone.sol (SOLIDITY)

```solidity
function withdrawAdmin() public onlyOwner {
    uint256 availableAmount = balanceOf(address(this)) -
    numTokensReservedForVesting;
    tokenAddress.safeTransfer(msg.sender, availableAmount);
    emit AdminWithdrawn(_msgSender(), availableAmount);
}
```

## Patch

Fixed in commits `dbf1f5a` and `cdfa29d` by considering both the contract token balance and the withdrawn token along with the locked tokens for calculating the remaining amount withdrawable.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | VTVL |
| Report Date | N/A |
| Finders | Robert Chen, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://vtvl.io/
- **GitHub**: https://github.com/VTVL-co/vtvl-smart-contracts/tree/audit-ready-jul-23
- **Contest**: https://vtvl.io/

### Keywords for Search

`vulnerability`

