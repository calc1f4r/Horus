---
# Core Classification
protocol: ReyaNetwork-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41131
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-August.md
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

[M-06] Potential loss of Ether due to overpayment

### Overview


This bug report discusses an issue in the `fullfillOracleQueryPyth` function in the `Pyth.sol` contract. The problem is that users can accidentally send more Ether than required to the `pyth.updatePriceFeeds` function, resulting in a loss of Ether. The report suggests adding a validation step before calling the function to ensure the correct amount of Ether is sent.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In the `fullfillOracleQueryPyth` function within `Pyth.sol`, there is a potential issue where users can inadvertently send more Ether (`msg.value`) than required to the `pyth.updatePriceFeeds` function. This overpayment has not been refunded, resulting in a loss of Ether.

The function implementation is as follows:

```solidity
function fullfillOracleQueryPyth(address pythAddress, bytes calldata signedOffchainData) {
    IPyth pyth = IPyth(pythAddress);

    (bytes[] memory updateData) = abi.decode(signedOffchainData, (bytes[]));

>>  try pyth.updatePriceFeeds{ value: msg.value }(updateData) { }
    catch (bytes memory reason) {
        if (_isFeeRequired(reason)) {
            revert Errors.FeeRequiredPyth(pyth.getUpdateFee(updateData));
        } else {
            uint256 len = reason.length;
            assembly {
                revert(add(reason, 0x20), len)
            }
        }
    }
}
```

The `msg.value` is transferred without validating the exact fee required by `pyth.updatePriceFeeds`. Based on the `Pyth::updatePriceFeeds` function at the address [`0xdd24f84d36bf92c65f92307595335bdfab5bbd21`](https://etherscan.io/address/0xdd24f84d36bf92c65f92307595335bdfab5bbd21#code#F2#L71), there is no mechanism that returns any excess ETH sent:

```solidity
    function updatePriceFeeds(
        bytes[] calldata updateData
    ) public payable override {
        uint totalNumUpdates = 0;
        for (uint i = 0; i < updateData.length; ) {
            if (
                updateData[i].length > 4 &&
                UnsafeCalldataBytesLib.toUint32(updateData[i], 0) ==
                ACCUMULATOR_MAGIC
            ) {
                totalNumUpdates += updatePriceInfosFromAccumulatorUpdate(
                    updateData[i]
                );
            } else {
                updatePriceBatchFromVm(updateData[i]);
                totalNumUpdates += 1;
            }

            unchecked {
                i++;
            }
        }
        uint requiredFee = getTotalFee(totalNumUpdates);
        if (msg.value < requiredFee) revert PythErrors.InsufficientFee();
    }
```

Therefore, two scenarios could occur:

- A user sends more ETH than expected, resulting in the extra ETH not being returned to the user by `Pyth`.
- Since the `Pyth` contract is upgradeable, [the fees in `pyth` could change](https://etherscan.io/address/0xdd24f84d36bf92c65f92307595335bdfab5bbd21#code#F2#L62) before the function `fullfillOracleQueryPyth` is executed, causing them to differ from what was expected.

## Recommendations

Before calling `pyth.updatePriceFeeds`, calculate and validate the exact fee required. This can be achieved by calling `pyth.getUpdateFee(updateData)` and comparing it with `msg.value`.

```diff
function fullfillOracleQueryPyth(address pythAddress, bytes calldata signedOffchainData) {
    IPyth pyth = IPyth(pythAddress);

    (bytes[] memory updateData) = abi.decode(signedOffchainData, (bytes[]));
+   uint fee = pyth.getUpdateFee(updateData);
+   require(msg.value == fee);
    try pyth.updatePriceFeeds{ value: msg.value }(updateData) { }
    catch (bytes memory reason) {
        if (_isFeeRequired(reason)) {
            revert Errors.FeeRequiredPyth(pyth.getUpdateFee(updateData));
        } else {
            uint256 len = reason.length;
            assembly {
                revert(add(reason, 0x20), len)
            }
        }
    }
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | ReyaNetwork-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

