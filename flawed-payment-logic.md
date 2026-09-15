---
# Core Classification
protocol: RFX Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51990
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/rfx-exchange/rfx-contracts
source_link: https://www.halborn.com/audits/rfx-exchange/rfx-contracts
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
  - Halborn
---

## Vulnerability Title

Flawed payment logic

### Overview

See description below for full details.

### Original Finding Content

##### Description

The **Oracle** contract relies on the **Pyth Network** for querying price feeds using `pyth.parsePriceFeedUpdates`, which necessitates a pre-calculated fee. However, the current payment logic has several issues:

  

1. The `_validateRealtimeFeeds` function does not validate whether the caller has provided sufficient ETH to cover the fees when calculating the fee. This oversight allows the caller to utilize contract funds and bypass the payment requirement.
2. The `validateRealtimeFeeds` function, which incurs fees by calling `_validateRealtimeFeeds`, lacks the `payable` modifier. Consequently, it does not allow callers to attach the necessary funds to cover fees. If the contract has insufficient funds, this function becomes temporarily disabled. Since the `Oracle` contract lacks a payable fallback or receive function, funds can only be transferred by either self-destructing from another contract to transfer funds or by attaching a large amount of ETH when calling `setPrices`, the only available payable function.

Code Location
-------------

The `_validateRealtimeFeeds` function does not validate whether the caller has provided sufficient ETH to cover the fees:

```
function _validateRealtimeFeeds(
        DataStore dataStore,
        address[] memory realtimeFeedTokens,
        bytes[] memory realtimeFeedData
    ) internal returns (OracleUtils.RealtimeFeedReport[] memory) {
        ...
        for (uint256 i; i < realtimeFeedTokens.length; i++) {
            ...
            uint fee = pyth.getUpdateFee(feedData);

            /// @dev Reverts if the transferred fee is not sufficient or the updateData is invalid or there is
            /// no update for any of the given `priceIds` within the given time range
            uint64 minPublishTime = uint64(Chain.currentTimestamp() - maxPriceAge);
            uint64 maxPublishTime = uint64(Chain.currentTimestamp() + maxPriceAge);
            PythStructs.PriceFeed[] memory priceFeeds = pyth.parsePriceFeedUpdates{value: fee}(feedData, feedIds, minPublishTime, maxPublishTime);
            ...
        }
        ...
    }
```

The `validateRealtimeFeeds` function calls the `_validateRealtimeFeeds`function. However, it lacks the `payable` modifier:

```
function validateRealtimeFeeds(
    DataStore dataStore,
    address[] memory realtimeFeedTokens,
    bytes[] memory realtimeFeedData
) external onlyController returns (OracleUtils.RealtimeFeedReport[] memory) {
    return _validateRealtimeFeeds(dataStore, realtimeFeedTokens, realtimeFeedData);
}
```

##### BVSS

[AO:A/AC:L/AX:L/R:P/S:C/C:N/A:M/I:N/D:M/Y:N (3.9)](/bvss?q=AO:A/AC:L/AX:L/R:P/S:C/C:N/A:M/I:N/D:M/Y:N)

##### Recommendation

It is recommended to implement the following changes:

* Validate that the caller has attached sufficient ETH to cover the fee and refund any excess amount within `_validateRealtimeFeeds`.
* Add the `payable` keyword to the `validateRealtimeFeeds` function to allow callers to attach ETH for covering the fees.

##### Remediation

**SOLVED**: The **RFX team** solved the issue when refactoring the codebase to v2.1.

##### Remediation Comment

Fixed/Refactored in RFX2.1

##### Remediation Hash

<https://github.com/relative-finance/rfx-contracts/tree/develop-v2>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | RFX Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/rfx-exchange/rfx-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/rfx-exchange/rfx-contracts

### Keywords for Search

`vulnerability`

