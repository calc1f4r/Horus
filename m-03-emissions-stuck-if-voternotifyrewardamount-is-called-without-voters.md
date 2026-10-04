---
# Core Classification
protocol: KittenSwap_2025-07-31
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61956
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/KittenSwap-security-review_2025-07-31.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Emissions stuck if `Voter.notifyRewardAmount()` is called without voters

### Overview


The Voter contract has a function called `notifyRewardAmount()` that allows anyone to donate `KITTEN` tokens for the current period. These tokens are then distributed among registered gauges based on their share of the total votes. However, this function does not check if there are any active voters in the current period, which means that if it is called during a period with no votes, the donated tokens will be stuck in the contract and not distributed to any gauge. To fix this issue, it is recommended to either disallow calling the function if there are no voters in the current period or to track undistributed rewards and carry them over to the next period.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In the `Voter` contract, the `notifyRewardAmount()` function allows anyone to donate `KITTEN` tokens for the current period, which are distributed among registered gauges based on their share of the total votes. This function is also invoked by `Minter.updatePeriod()` to mint and allocate emissions starting from the next epoch period after the `Voter.start()` call.

However, the function does not validate whether the current period has any active voters; it does not check if `period[_period].globalTotalVotes > 0`. As a result, if the function is called during a period with no votes, the donated emissions will be stuck in the contract and will not be distributed to any gauge.

```solidity
  function notifyRewardAmount(uint256 _amount) public {
        uint256 currentPeriod = getCurrentPeriod();

        kitten.safeTransferFrom(msg.sender, address(this), _amount);
        period[currentPeriod].totalEmissions += _amount;
    }
```

```solidity
function _distribute(uint256 _period, address _gauge) internal {
        //...
        IVoter.Period storage ps = period[_period];
        IVoter.Emissions storage es = ps.gaugeEmissions[_gauge];
        if (es.distributed) revert EmissionsAlreadyDistributedForPeriod();

        uint256 emissions = (ps.totalEmissions * ps.gaugeTotalVotes[_gauge]) /
            ps.globalTotalVotes;
       //...
    }
```

## Recommendations

Disallow calling `Voter.notifyRewardAmount()` if the current period has no voters by checking `period[_period].globalTotalVotes == 0`, or alternatively, track undistributed rewards and carry them over to the next period.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | KittenSwap_2025-07-31 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/KittenSwap-security-review_2025-07-31.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

