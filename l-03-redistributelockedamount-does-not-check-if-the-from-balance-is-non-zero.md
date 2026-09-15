---
# Core Classification
protocol: Ethena-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41344
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ethena-security-review-August.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-03] `redistributeLockedAmount` does not check if the `from` balance is non-zero

### Overview

See description below for full details.

### Original Finding Content

Across `StakedENA` functions, especially `_deposit` and `transferInRewards`, there is always a check to ensure the provided amount is non-zero. However, this check is missing in `redistributeLockedAmount`. If `redistributeLockedAmount` is called with a from the balance of 0, it will set `vestingAmount` to 0 and update `lastDistributionTimestamp` when the to address is the zero address. If the `to` address is non-zero, it will mint 0 shares to that address.

```solidity
  function redistributeLockedAmount(address from, address to) external nonReentrant onlyRole(DEFAULT_ADMIN_ROLE) {
    if (!hasRole(BLACKLISTED_ROLE, from) || hasRole(BLACKLISTED_ROLE, to)) revert OperationNotAllowed();
   // @audit - no check if amountToDistribute is non-zero
    uint256 amountToDistribute = balanceOf(from);
    uint256 enaToVest = previewRedeem(amountToDistribute);
    _burn(from, amountToDistribute);
    // to address of address(0) enables burning
    if (to == address(0)) {
      _updateVestingAmount(enaToVest);
    } else {
      _mint(to, amountToDistribute);
    }

    emit StakedENARedistributed(from, to, amountToDistribute);
  }
```

Consider adding a non-zero check to match the safeguards in other functions

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ethena-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ethena-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

