---
# Core Classification
protocol: Vertex LBA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47754
audit_firm: OtterSec
contest_link: https://vertexprotocol.com/
source_link: https://vertexprotocol.com/
github_link: https://github.com/vertex-protocol/vertex-lba/

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
finders_count: 4
finders:
  - Nicholas R. Putra
  - Woosun Song
  - Matteo Oliva
  - OtterSec
---

## Vulnerability Title

Incorrect Pruning Of Vesting Schedules

### Overview


The report discusses a bug in the _pruneExpiredVestingSchedules function in the Vesting.sol contract. This function is important for maintaining the efficiency of the vesting contract by removing expired vesting schedules. However, the deletion logic in the function is flawed, as it does not properly check whether the last element in the array is also expired before moving on to the next index. This can result in some expired schedules not being removed, leading to incorrect token balances and potential security risks. The report provides a proof of concept and suggests a solution using a while loop. The bug has been fixed in a recent update.

### Original Finding Content

## Prune Expired Vesting Schedules in Vesting

_pruneExpiredVestingSchedules_ in Vesting is crucial for maintaining the cleanliness and efficiency of the vesting contract. It identifies and removes vesting schedules past their specified end times, ensuring beneficiaries only claim tokens from active and relevant schedules.

## Vesting.sol SOLIDITY

```solidity
function _pruneExpiredVestingSchedules(address account) internal {
    uint64 currentTime = uint64(block.timestamp);
    for (uint32 i = 0; i < vestingScheduleIds[account].length; i++) {
        if (vestingSchedules[vestingScheduleIds[account][i]].endTime <= currentTime) {
            vestingScheduleIds[account][i] = vestingScheduleIds[account][vestingScheduleIds[account].length - 1];
            vestingScheduleIds[account].pop();
        }
    }
}
```

The issue arises from the deletion logic within the for loop, where the last element in the array replaces the expired element. However, _pruneExpiredVestingSchedules_ does not check whether the last element is also expired before moving to the following index. This may result in missing some expired schedules during the pruning process, only partially removing the expired vesting schedules.

Since expired vesting schedules should no longer be considered part of the beneficiary’s available vested balance, if they are not removed, the beneficiary may mistakenly believe they have more vested tokens than they actually do, resulting in incorrect decisions or actions based on this inaccurate balance. Thus, failing to remove expired vesting schedules may yield misleading information, token distribution issues, and potential security risks.

## Vertex LBA Audit 04 | Vulnerabilities

### Proof of Concept

1. Let there be an array of vesting schedules for a specific beneficiary:
   - Vesting Schedule 1: [Start Time: 1000, End Time: 1500, Amount: 100]
   - Vesting Schedule 2: [Start Time: 1200, End Time: 1700, Amount: 200]
   - Vesting Schedule 3: [Start Time: 1300, End Time: 1600, Amount: 300]
   - Vesting Schedule 4: [Start Time: 1400, End Time: 1900, Amount: 400]
   
2. The current time is 1350, and we want to prune the expired schedules. The function would pass through the list like this:
   - Check Vesting Schedule 1: Not expired (continue).
   - Check Vesting Schedule 2: Expired (replace with the last, Vesting Schedule 4).
   - Now, the loop moves to index two.
   
3. As the loop moves forward, Vesting Schedule 2 is replaced by Vesting Schedule 4, which is not yet checked. This may result in missing the opportunity to prune Vesting Schedule 4, which is also expired.

### Remediation

Utilize a while loop, which allows for continuous checking of the current index until the schedule at that index has not expired, ensuring that all expired schedules are pruned.

## Vesting.sol SOLIDITY

```solidity
function _pruneExpiredVestingSchedules(address account) internal {
    uint64 currentTime = uint64(block.timestamp);
    uint32 i = 0;
    while (i < vestingScheduleIds[account].length) {
        uint64 scheduleId = vestingScheduleIds[account][i];
        if (vestingSchedules[scheduleId].endTime <= currentTime) {
            vestingScheduleIds[account][i] = vestingScheduleIds[account][vestingScheduleIds[account].length - 1];
            vestingScheduleIds[account].pop();
        } else {
            i += 1;
        }
    }
}
```

## Patch

Fixed in 655103b.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Vertex LBA |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Woosun Song, Matteo Oliva, OtterSec |

### Source Links

- **Source**: https://vertexprotocol.com/
- **GitHub**: https://github.com/vertex-protocol/vertex-lba/
- **Contest**: https://vertexprotocol.com/

### Keywords for Search

`vulnerability`

