---
# Core Classification
protocol: stETH by EaseDeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64090
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1203
source_link: none
github_link: https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi-judging/issues/899

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
finders_count: 9
finders:
  - befree3x
  - khaye26
  - Sir\_Shades
  - hanz
  - thimthor
---

## Vulnerability Title

M-7: Missing Uniswap V3 cardinality initialization in `StNxmOracle` leads to permanent Denial of Service

### Overview


Summary:

The `StNxmOracle` contract, which calculates the price of `stNXM` using a Uniswap V3 pool, is failing due to a default setting in newly created pools. The pool's `observationCardinality` is set to 1 by default, which is not enough to cover the 30-minute Time-Weighted Average Price (TWAP) that the contract needs. This causes the `price()` function to consistently revert, making the oracle unusable and affecting dependent systems. The root cause is that the constructor fails to initialize the pool with enough historical observation slots. This results in a Denial of Service (DoS) for the lending integration and prevents users from borrowing and liquidators from securing the protocol. To fix this, the pool's `observationCardinality` should be increased in the constructor. The protocol team has already fixed this issue in their code.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi-judging/issues/899 

## Found by 
0x73696d616f, 0xAsen, Almanax, Anas22, Sir\_Shades, befree3x, hanz, khaye26, thimthor

### Summary

The `StNxmOracle` contract calculates the price of `stNXM` using a 30-minute Time-Weighted Average Price (TWAP) from a Uniswap V3 pool. However, newly created Uniswap V3 pools are initialized with an `observationCardinality` of 1 by default, which only stores the current block's state.

Because the Oracle does not expand this cardinality during initialization, calls to `OracleLibrary.consult` requesting data from 1800 seconds (30 minutes) ago will inevitably fail. This causes the [`price()`](https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi/blob/main/stNXM-Contracts/contracts/core/stNxmOracle.sol#L31-L40) function to revert consistently, rendering the oracle unusable and bricking any dependent systems (like Morpho markets) immediately upon deployment.

### Root Cause

In `stNxmOracle.sol`, the constructor sets the `dex` address but fails to call `increaseObservationCardinalityNext` on the Uniswap V3 pool.

By default, Uniswap V3 pools have an `observationCardinality` of 1. To successfully query a TWAP over a window of `TWAP_PERIOD` (1800 seconds), the pool must be configured to store enough historical observation slots to cover that duration given the chain's block time. Without this initialization, `OracleLibrary.consult` reverts when trying to interpolate a past timestamp.

### Internal Pre-conditions

1. `StNxmOracle` is deployed with a reference to a Uniswap V3 pool.
2. The `StNxmOracle` attempts to query a TWAP period of 1800 seconds (`TWAP_PERIOD`).

### External Pre-conditions

1. The linked Uniswap V3 pool has the default `observationCardinality` of 1 (or any value insufficient to cover 30 minutes of history).


### Attack Path


1.  **Deployment:** The protocol deploys `StNxmOracle`.
2.  **Interaction:** A user or the Morpho protocol calls `stNxmOracle.price()` to value collateral.
3.  **Execution:**
    * The function calls `OracleLibrary.consult(dex, 1800)`.
    * The library attempts to fetch the observation from 1800 seconds ago.
    * The Uniswap pool checks its observation buffer. Since cardinality is 1, it cannot provide history.
4.  **Failure:** The transaction reverts.
5.  **DoS:** The Oracle remains unusable until an external party manually calls `increaseObservationCardinalityNext` on the pool and waits for the buffer to fill.


### Impact

The protocol cannot execute Oracle updates. This results in an immediate Denial of Service (DoS) for the lending integration. Morpho cannot retrieve a valid price, preventing users from borrowing and preventing liquidators from securing the protocol.

### PoC

_No response_

### Mitigation

In the `StNxmOracle` constructor, verify the pool's cardinality and increase it if necessary to support the 30-minute TWAP. A safe buffer is recommended (e.g., 100 slots).

```diff
    constructor(address _dex, address _wNxm, address _stNxm) {
        dex = IUniswapV3Pool(_dex);
        wNxm = _wNxm;
        stNxm = _stNxm;
        startTime = block.timestamp;

+       // Increase cardinality to ensure enough history for 30m TWAP
+       // 100 slots is usually sufficient for 30 mins on Mainnet (12s blocks)
+       // But safer to go higher or calculate exact needs.
+       dex.increaseObservationCardinalityNext(100);
    }
```

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/EaseDeFi/stNXM-Contracts/commit/98c005807c5f74d61de7280d572c4aac7ba2f8cb







### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | stETH by EaseDeFi |
| Report Date | N/A |
| Finders | befree3x, khaye26, Sir\_Shades, hanz, thimthor, 0xAsen, 0x73696d616f, Anas22, Almanax |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi-judging/issues/899
- **Contest**: https://app.sherlock.xyz/audits/contests/1203

### Keywords for Search

`vulnerability`

