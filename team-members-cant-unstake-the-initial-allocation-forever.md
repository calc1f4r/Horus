---
# Core Classification
protocol: Goldilocks
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30924
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
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
  - Hans
---

## Vulnerability Title

Team members can't unstake the initial allocation forever.

### Overview


This bug report discusses a problem where team members are unable to unstake their tokens forever. This is because the function `_vestingCheck` returns 0 for team members, preventing them from unstaking. Additionally, the function `stake` does not prevent team members from staking, causing them to be unable to unstake if they have staked additionally. The recommended solution is to use the same logic for team members as for initial investors in the `_vestingCheck` function. The client has acknowledged the issue and a pull request has been made to fix it. The bug has been verified by Cyfrin.

### Original Finding Content

**Severity:** High

**Description:** When users call `unstake()`, it calculates the vested amount using `_vestingCheck()`.

```solidity
  function _vestingCheck(address user, uint256 amount) internal view returns (uint256) {
    if(teamAllocations[user] > 0) return 0; //@audit return 0 for team members
    uint256 initialAllocation = seedAllocations[user];
    if(initialAllocation > 0) {
      if(block.timestamp < vestingStart) return 0;
      uint256 vestPortion = FixedPointMathLib.divWad(block.timestamp - vestingStart, vestingEnd - vestingStart);
      return FixedPointMathLib.mulWad(vestPortion, initialAllocation) - (initialAllocation - stakedLocks[user]);
    }
    else {
      return amount;
    }
  }
```

But it returns 0 for team members and they can't unstake forever.
Furthermore, in `stake()`, it just prevents seed investors, not team members. So if team members have staked additionally, they can't unstake also.

**Impact:** Team members can't unstake forever.

**Recommended Mitigation:** `_vestingCheck` should use the same logic as initial investors for team mates.

**Client:** Acknowledged, it is intended that the team cannot unstake their tokens. [PR #4](https://github.com/0xgeeb/goldilocks-core/pull/4) fixes issue of `stake` not preventing team members from staking.

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Goldilocks |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

