---
# Core Classification
protocol: KittenSwap_2025-05-07
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58154
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/KittenSwap-security-review_2025-05-07.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-03] `ExternalBribe.earned` skips rewards before the last `tokenId` checkpoint

### Overview


This bug report discusses an issue with the `ExternalBribe.earned` function. The function is supposed to loop through previous rewards to determine the amount earned, but it is currently skipping the checkpoint before `_endIndex`. This means that rewards are not being counted correctly. To fix this, the calculation logic should be updated to include `_endIndex`. A test file has been provided to demonstrate the issue and a recommendation to change the code has been made. 

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

Inside `ExternalBribe.earned`, it first loops up to `_endIndex - 1` to determine whether to include previous rewards in the earned amount.

```solidity
    function earned(address token, uint tokenId) public view returns (uint) {
        uint _startTimestamp = lastEarn[token][tokenId];
        if (numCheckpoints[tokenId] == 0) {
            return 0;
        }

        uint _startIndex = getPriorBalanceIndex(tokenId, _startTimestamp);
        uint _endIndex = numCheckpoints[tokenId] - 1;

        uint reward = 0;
        // you only earn once per epoch (after it's over)
        RewardCheckpoint memory prevRewards;

        prevRewards.timestamp = _bribeStart(_startTimestamp);

        _prev._prevSupply = 1;

        console.log("END INDEX : ");
        console.log(_endIndex);

        if (_endIndex > 0) {
>>>         for (uint i = _startIndex; i <= _endIndex - 1; i++) {
                _prev._prevTs = checkpoints[tokenId][i].timestamp;
                _prev._prevBal = checkpoints[tokenId][i].balanceOf;
                uint _nextEpochStart = _bribeStart(_prev._prevTs);
                // check that you've earned it
                // this won't happen until a week has passed
>>>             if (_nextEpochStart > prevRewards.timestamp) {
                    console.log("REWARD ADDED : ");
                    console.log(prevRewards.balance);
                    reward += prevRewards.balance;
                }

                prevRewards.timestamp = _nextEpochStart;
                _prev._prevSupply = supplyCheckpoints[
                    getPriorSupplyIndex(_nextEpochStart + DURATION)
                ].supply;
                prevRewards.balance =
                    (_prev._prevBal *
                        tokenRewardsPerEpoch[token][_nextEpochStart]) /
                    _prev._prevSupply;
            }
        }

        Checkpoint memory _cp0 = checkpoints[tokenId][_endIndex];
        (_prev._prevTs, _prev._prevBal) = (_cp0.timestamp, _cp0.balanceOf);

        uint _lastEpochStart = _bribeStart(_prev._prevTs);
        uint _lastEpochEnd = _lastEpochStart + DURATION;

        if (
            block.timestamp > _lastEpochEnd && _startTimestamp < _lastEpochEnd
        ) {
            SupplyCheckpoint memory _scp0 = supplyCheckpoints[
                getPriorSupplyIndex(_lastEpochEnd)
            ];
            _prev._prevSupply = _scp0.supply;
            reward += (_prev._prevBal *
                    tokenRewardsPerEpoch[token][_lastEpochStart]) /
                _prev._prevSupply;
        }

        return reward;
    }
```

However, the logic should include `_endIndex`, as the checkpoint before it must be checked, otherwise, it will always be skipped and not counted as a reward.

Add the following test file to the repo: https://gist.github.com/said017/b96daba163bf2e1eb101589bc541ce06.

Run the test :

```shell
forge test --match-test testEpochCalculationIssue -vvv
```

Log output :

```shell
Logs:

  Earned at end of first epoch: 100000000000000000000

  Earned at end of second epoch: 0

  Earned at end of third epoch: 100000000000000000000
```

## Recommendations

Change the calculation logic to include `_endIndex`.

```diff
    function earned(address token, uint tokenId) public view returns (uint) {
        uint _startTimestamp = lastEarn[token][tokenId];
        if (numCheckpoints[tokenId] == 0) {
            return 0;
        }

        uint _startIndex = getPriorBalanceIndex(tokenId, _startTimestamp);
        uint _endIndex = numCheckpoints[tokenId] - 1;

        uint reward = 0;
        // you only earn once per epoch (after it's over)
        RewardCheckpoint memory prevRewards;

        prevRewards.timestamp = _bribeStart(_startTimestamp);

        _prev._prevSupply = 1;

        console.log("END INDEX : ");
        console.log(_endIndex);

        if (_endIndex > 0) {
-            for (uint i = _startIndex; i <= _endIndex - 1; i++) {
+            for (uint i = _startIndex; i <= _endIndex ; i++) {
                _prev._prevTs = checkpoints[tokenId][i].timestamp;
                _prev._prevBal = checkpoints[tokenId][i].balanceOf;
                uint _nextEpochStart = _bribeStart(_prev._prevTs);
                // check that you've earned it
                // this won't happen until a week has passed
                if (_nextEpochStart > prevRewards.timestamp) {
                    console.log("REWARD ADDED : ");
                    console.log(prevRewards.balance);
                    reward += prevRewards.balance;
                }
/ ...
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | KittenSwap_2025-05-07 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/KittenSwap-security-review_2025-05-07.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

