---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17910
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ22022.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ22022.pdf
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Gustavo Grieco
  - Michael Colburn
---

## Vulnerability Title

Missing events in several contracts

### Overview

See description below for full details.

### Original Finding Content

## Data Validation Issue in Frax Finance Contracts

## Difficulty: High

## Type: Data Validation

## Description

An insufficient number of events is declared in the Frax Finance contracts. As a result, malfunctioning contracts or malicious attacks may not be noticed.

For instance, long-term swaps are executed in batches by the `executeVirtualOrdersUntilTimestamp` function:

```solidity
/// @notice executes all virtual orders until blockTimestamp is reached.
function executeVirtualOrdersUntilTimestamp(LongTermOrders storage longTermOrders, uint256 blockTimestamp, ExecuteVirtualOrdersResult memory reserveResult) internal {
    uint256 nextExpiryBlockTimestamp = longTermOrders.lastVirtualOrderTimestamp
    - (longTermOrders.lastVirtualOrderTimestamp % longTermOrders.orderTimeInterval) +
    longTermOrders.orderTimeInterval;

    // iterate through time intervals eligible for order expiries, moving state forward
    OrderPool storage orderPool0 = longTermOrders.OrderPool0;
    OrderPool storage orderPool1 = longTermOrders.OrderPool1;
    while (nextExpiryBlockTimestamp < blockTimestamp) {
        // Optimization for skipping blocks with no expiry
        if (orderPool0.salesRateEndingPerTimeInterval[nextExpiryBlockTimestamp] > 0 || orderPool1.salesRateEndingPerTimeInterval[nextExpiryBlockTimestamp] > 0) {
            // amount sold from virtual trades
            uint256 blockTimestampElapsed = nextExpiryBlockTimestamp - longTermOrders.lastVirtualOrderTimestamp;
            uint256 token0SellAmount = orderPool0.currentSalesRate * blockTimestampElapsed / SELL_RATE_ADDITIONAL_PRECISION;
            uint256 token1SellAmount = orderPool1.currentSalesRate * blockTimestampElapsed / SELL_RATE_ADDITIONAL_PRECISION;
            (uint256 token0Out, uint256 token1Out) = executeVirtualTradesAndOrderExpiries(reserveResult, token0SellAmount, token1SellAmount);
            updateOrderPoolAfterExecution(longTermOrders, orderPool0, orderPool1, token0Out, token1Out, nextExpiryBlockTimestamp);
        }
        nextExpiryBlockTimestamp += longTermOrders.orderTimeInterval;
    }

    // finally, move state to current blockTimestamp if necessary
    if (longTermOrders.lastVirtualOrderTimestamp != blockTimestamp) {
        // amount sold from virtual trades
        uint256 blockTimestampElapsed = blockTimestamp - longTermOrders.lastVirtualOrderTimestamp;
        uint256 token0SellAmount = orderPool0.currentSalesRate * blockTimestampElapsed / SELL_RATE_ADDITIONAL_PRECISION;
        uint256 token1SellAmount = orderPool1.currentSalesRate * blockTimestampElapsed / SELL_RATE_ADDITIONAL_PRECISION;
        (uint256 token0Out, uint256 token1Out) = executeVirtualTradesAndOrderExpiries(reserveResult, token0SellAmount, token1SellAmount);
        updateOrderPoolAfterExecution(longTermOrders, orderPool0, orderPool1, token0Out, token1Out, blockTimestamp);
    }
}
```

*Figure 3.1: Uniswap_V2_TWAMM/twamm/LongTermOrders.sol#L216-L252*

However, despite the complexity of this function, it does not emit any events; it will be difficult to monitor issues that may arise whenever the function is executed. 

Additionally, important operations in the `FPIControllerPool` and `CPITrackerOracle` contracts do not emit any events:

```solidity
function toggleMints() external onlyByOwnGov {
    mints_paused = !mints_paused;
}

function toggleRedeems() external onlyByOwnGov {
    redeems_paused = !redeems_paused;
}

function setFraxBorrowCap(int256 _frax_borrow_cap) external onlyByOwnGov {
    frax_borrow_cap = _frax_borrow_cap;
}

function setMintCap(uint256 _fpi_mint_cap) external onlyByOwnGov {
    fpi_mint_cap = _fpi_mint_cap;
}
```

*Figure 3.2: FPI/FPIControllerPool.sol#L528-L542*

Events generated during contract execution aid in monitoring, baselining of behavior, and detection of suspicious activity. Without events, users and blockchain-monitoring systems cannot easily detect behavior that falls outside the baseline conditions, and it will be difficult to review the correct behavior of the contracts once they have been deployed.

## Exploit Scenario

Eve, a malicious user, discovers a vulnerability that allows her to manipulate long-term swaps. Because no events are generated from her actions, the attack goes unnoticed. Eve uses her exploit to drain liquidity or prevent other users from swapping before the Frax Finance team has a chance to respond.

## Recommendations

- **Short term**: Emit events for all operations that may contribute to a higher level of monitoring and alerting, even internal ones.
- **Long term**: Consider using a blockchain-monitoring system to track any suspicious behavior in the contracts. A monitoring mechanism for critical events could quickly detect system compromises.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Gustavo Grieco, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ22022.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ22022.pdf

### Keywords for Search

`vulnerability`

