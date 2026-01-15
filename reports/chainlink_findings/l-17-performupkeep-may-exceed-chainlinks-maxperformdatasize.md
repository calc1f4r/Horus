---
# Core Classification
protocol: Tanssi_2025-04-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63313
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Tanssi-security-review_2025-04-30.md
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

[L-17] `performUpkeep()` may exceed Chainlink's `maxPerformDataSize`

### Overview

See description below for full details.

### Original Finding Content


According to Chainlink [documentation](https://docs.chain.link/chainlink-automation/overview/supported-networks#ethereum) the maximum size in bytes that can be sent to `performUpkeep` function is `2000` bytes.

Within the `performUpkeep()` implementation, `performData` contains the sorted keys and the epoch from `performData`.

```solidity
File: contracts/middleware/Middleware.sol
316:     function performUpkeep(
317:         bytes calldata performData
318:     ) external override checkAccess {
319:         StorageMiddleware storage $ = _getMiddlewareStorage();
320:         address gateway = $.gateway;
321:         if (gateway == address(0)) {
322:             revert Middleware__GatewayNotSet();
323:         }
324: 
325:         uint48 currentTimestamp = Time.timestamp();
326:         if ((currentTimestamp - $.lastTimestamp) > $.interval) {
327:             $.lastTimestamp = currentTimestamp;
328: 
329:             // Decode the sorted keys and the epoch from performData
330:             (bytes32[] memory sortedKeys, uint48 epoch) = abi.decode(performData, (bytes32[], uint48));
331: 
332:             IOGateway(gateway).sendOperatorsData(sortedKeys, epoch);
333:         }
334:     }
```

Chainlink Keepers are also constrained by a strict maximum gas usage, which impacts their ability to execute high-cost operations such as `sortOperatorsByPower()`. The development team is aware of the significant gas consumption associated with this function, as noted in the code comments:

```solidity
File: contracts/middleware/OBaseMiddlewareReader.sol
521:     /**
522:      * @dev Sorts operators by their total power in descending order, after 500 it will be almost impossible to be used on-chain since 500 ≈ 36M gas
523:      * @param epoch The epoch number
524:      * @return sortedKeys Array of sorted operators keys based on their power
525:      */
526: 
```

However, there is an additional constraint that appears to be overlooked. Chainlink enforces a `maxPerformDataSize` limit, which imposes a stricter cap on the number of operators that can be handled. Since each operator key is represented as a `bytes32` value, the total number of keys that can be included is limited to: 2000 / 32 = 62 keys.

This results in a practical upper limit of 62 operators, which is significantly lower than the 500-operator estimate referenced in the comments.

The Middleware does not implement any mechanism which limits the number of operators, thus when that number becomes too big (there would be too many operators) - the Chainlink's `maxPerformDataSize` will be reached.


**Recommendations**

Implement a mechanism which limits the number of operators.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tanssi_2025-04-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Tanssi-security-review_2025-04-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

