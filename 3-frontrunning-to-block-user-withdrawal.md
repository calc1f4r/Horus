---
# Core Classification
protocol: 1Inch
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53458
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2022-11-04-1inch.md
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
  - Hexens
---

## Vulnerability Title

3. Frontrunning to block user withdrawal

### Overview


This bug report discusses a high severity issue in the function `withdraw` and `withdrawTo` in the St1inch.sol smart contract. These functions can be exploited by malicious actors by calling `depositFor` or `depositForWithPermit` and passing the victim's account and 0 as amount and any lock period as duration. This can block any user withdrawal requests. The issue has been fixed by making the duration of the lock updatable only by the owner. 

### Original Finding Content

**Severity:** High

**Path:** St1inch.sol:#L118-L134, L145-L165

**Description:** 

The functions `withdraw` and `withdrawTo` can be frontrunned by any illicit
actor by calling `depositFor` or `depositForWithPermit` and passing the
victims account and 0 as amount and any lock period as duration (e.g.
`MAX_LOCK_PERIOD`). Since the function `_deposit` ignores token transfer
logic in case of 0 amount and just adds the lock duration. Any user
withdrawal requests can be blocked using such attack vector.

```
function depositFor(
       address account,
       uint256 amount,
       uint256 duration
   ) external {
       _deposit(account, amount, duration);
   }

   function depositForWithPermit(
       address account,
       uint256 amount,
       uint256 duration,
       bytes calldata permit
   ) public {
       oneInch.safePermit(permit);
       _deposit(account, amount, duration);

   }
```
```
function _deposit(
       address account,
       uint256 amount,
       uint256 duration
   ) private {
       if (_deposits[account] > 0 && amount > 0 && duration > 0) revert 
ChangeAmountAndUnlockTimeForExistingAccount();
       if (amount > 0) {
           oneInch.transferFrom(msg.sender, address(this), amount);
           _deposits[account] += amount;
           totalDeposits += amount;
       }
       uint256 lockedTill = Math.max(_unlockTime[account], block.timestamp) + 
duration;
       uint256 lockedPeriod = lockedTill - block.timestamp;
       if (lockedPeriod < MIN_LOCK_PERIOD) revert LockTimeLessMinLock();
       if (lockedPeriod > MAX_LOCK_PERIOD) revert LockTimeMoreMaxLock();
       _unlockTime[account] = lockedTill;
       _mint(account, _balanceAt(_deposits[account], lockedTill) / 
_VOTING_POWER_DIVIDER - balanceOf(account));

   }
```

**Remediation:**  The duration of the lock should be updatable only
by the owner, e.g. depositFor and depositForWithPermit should call
_deposit with 0 duration.

**Status:** Fixed



- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | 1Inch |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2022-11-04-1inch.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

