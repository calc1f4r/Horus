---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26971
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-verwa
source_link: https://code4rena.com/reports/2023-08-verwa
github_link: https://github.com/code-423n4/2023-08-verwa-findings/issues/288

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
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - cducrest
  - oakcobalt
  - Yanchuan
  - markus\_ether
  - bin2chen
---

## Vulnerability Title

[H-03] When adding a gauge, its initial value has to be set by an admin or all voting power towards it will be lost

### Overview


This bug report is about a bug found in the GaugeController.sol file of the 2023-08-verwa project. The bug is caused by the mapping `time_weight` which takes a gauge as a parameter and returns the most recent timestamp a gauge has had its weight recorded/updated. The problem is that the initial value of any `time_weight[_gauge_addr]` will be 0, and unless admins call manually `_change_gauge_weight` to set an initial value, `time_weight[_gauge_addr]` will remain 0. This means that any votes happening in the time between the adding of the gauge and the admin set function will be lost.

The bug was found using the Foundry tool and the recommended mitigation step is to call `change_gauge_weight` and set its initial weight to 0 upon adding a gauge.

### Original Finding Content


<https://github.com/code-423n4/2023-08-verwa/blob/main/src/GaugeController.sol#L118> 

<https://github.com/code-423n4/2023-08-verwa/blob/main/src/GaugeController.sol#L204>

Voting power towards gauges will be lost and project will not work properly

### Proof of Concept

The mapping `time_weight` takes a gauge as a param and returns the most recent timestamp a gauge has had its weight recorded/ updated. There are 2 ways to set this value: through `_get_weight` and `_change_gauge_weight`.

<details>

```solidity
function _get_weight(address _gauge_addr) private returns (uint256) {
        uint256 t = time_weight[_gauge_addr];
        if (t > 0) {
            Point memory pt = points_weight[_gauge_addr][t];
            for (uint256 i; i < 500; ++i) {
                if (t > block.timestamp) break;
                t += WEEK;
                uint256 d_bias = pt.slope * WEEK;
                if (pt.bias > d_bias) {
                    pt.bias -= d_bias;
                    uint256 d_slope = changes_weight[_gauge_addr][t];
                    pt.slope -= d_slope;
                } else {
                    pt.bias = 0;
                    pt.slope = 0;
                }
                points_weight[_gauge_addr][t] = pt;
                if (t > block.timestamp) time_weight[_gauge_addr] = t;
            }
            return pt.bias;
        } else {
            return 0;
        }
    }
```

The problem in `_get_weight` is that the initial value of any `time_weight[_gauge_addr]` will be 0. It will go through the entirety of the loop and `t` will increase +1 week for every iteration. The problem is that even after 500 iterations `t` will be `< block.timestamp` so the value of `time_weight[_gauge_addr]` will remain 0. Unless admins call manually `_change_gauge_weight` to set an initial value, `time_weight[_gauge_addr]` will remain 0. Any  time a user will use `_get_weight` to fill with recent data, the function will iterate over old values and will do nothing. Recent values won't be set and anything depending on it will receive 0 as a recent value.

```solidity
    function _change_gauge_weight(address _gauge, uint256 _weight) internal {
        uint256 old_gauge_weight = _get_weight(_gauge);
        uint256 old_sum = _get_sum();
        uint256 next_time = ((block.timestamp + WEEK) / WEEK) * WEEK;

        points_weight[_gauge][next_time].bias = _weight;
        time_weight[_gauge] = next_time;

        uint256 new_sum = old_sum + _weight - old_gauge_weight;
        points_sum[next_time].bias = new_sum;
        time_sum = next_time;
    }
```

Since `_change_gauge_weight` is not called within `add_gauge`, even if we expect the owners to call it, any votes happening in the time between the adding of the gauge and the admin set function will be lost. The user will only be able to retrieve them by later removing their vote and voting again.
Here are 3 written test-cases which prove the statements above:

```solidity
   function testWithoutManualSet() public {
        vm.startPrank(gov);
        gc.add_gauge(gauge1);
        vm.stopPrank();

        vm.startPrank(user1);
        ve.createLock{value: 1 ether}(1 ether);
        gc.vote_for_gauge_weights(gauge1, 10000);
        uint weight = gc.get_gauge_weight(gauge1);
        console.log("gauge's weight after voting: ", weight);
        vm.stopPrank();
    }

    function testWithManualSet() public { 
        vm.startPrank(gov);
        gc.add_gauge(gauge1);
        gc.change_gauge_weight(gauge1, 0);
        vm.stopPrank();

        vm.startPrank(user1);
        ve.createLock{value: 1 ether}(1 ether);
        gc.vote_for_gauge_weights(gauge1, 10000);
        uint weight = gc.get_gauge_weight(gauge1);
        console.log("gauge's weight after voting: ", weight);
        vm.stopPrank();
    }

    function testWithChangeMidway() public {
        vm.startPrank(gov);
        gc.add_gauge(gauge1);
        vm.stopPrank();

        vm.startPrank(user1);
        ve.createLock{value: 1 ether}(1 ether);
        gc.vote_for_gauge_weights(gauge1, 10000);
        uint weight = gc.get_gauge_weight(gauge1);
        console.log("gauge's weight after voting: ", weight);
        vm.stopPrank();

        vm.prank(gov);
        gc.change_gauge_weight(gauge1, 0);

        vm.startPrank(user1);
        gc.vote_for_gauge_weights(gauge1, 10000);
        weight = gc.get_gauge_weight(gauge1);
        console.log("gauge's weight after voting after admin set", weight);

        gc.vote_for_gauge_weights(gauge1, 0);
        gc.vote_for_gauge_weights(gauge1, 10000);
        weight = gc.get_gauge_weight(gauge1);
        console.log("gauge's weight after voting after admin set after vote reset", weight);
        
    }
```

and the respective results:

    [PASS] testWithoutManualSet() (gas: 645984)
    Logs:
      gauge's weight after voting:  0

```

    [PASS] testWithManualSet() (gas: 667994)
    Logs:
      gauge's weight after voting:  993424657416307200
```

```

    [PASS] testWithChangeMidway() (gas: 744022)
    Logs:
      gauge's weight after voting:  0
      gauge's weight after voting after admin set 0
      gauge's weight after voting after admin set after vote reset 993424657416307200
```

</details>

### Tools Used

Foundry

### Recommended Mitigation Steps

Upon adding a gauge, make a call to `change_gauge_weight` and set its initial weight to 0.

**[\_\_141345\_\_ (Lookout) commented](https://github.com/code-423n4/2023-08-verwa-findings/issues/288#issuecomment-1678351795):**
 > Forget to initialize `time_weight[]` when add new gauge.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | cducrest, oakcobalt, Yanchuan, markus\_ether, bin2chen, 0xComfyCat, Brenzee, deadrxsezzz, auditsea, Team\_Rocket |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-verwa
- **GitHub**: https://github.com/code-423n4/2023-08-verwa-findings/issues/288
- **Contest**: https://code4rena.com/reports/2023-08-verwa

### Keywords for Search

`vulnerability`

