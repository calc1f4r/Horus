---
# Core Classification
protocol: Plaza Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49258
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/682
source_link: none
github_link: https://github.com/sherlock-audit/2024-12-plaza-finance-judging/issues/981

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
finders_count: 14
finders:
  - Adotsam
  - 056Security
  - noromeb
  - 0xAadi
  - KiroBrejka
---

## Vulnerability Title

M-18: Missing Chainlink Price Feeds for wstETH/USD and stETH/USD in BalancerOracleAdapter.sol

### Overview


This bug report discusses an issue with the BalancerOracleAdapter.sol contract, which is used to determine the prices of tokens in a Balancer pool. The contract relies on Chainlink price feeds, but the price feeds for wstETH/USD and stETH/USD do not exist. This means that any attempt to calculate prices for these tokens will fail, causing the contract to revert. This bug was found by multiple security researchers and has been acknowledged by the protocol. The cause of the issue is a line of code that expects price feeds in a specific format, which Chainlink does not provide. The bug can be triggered if wstETH or stETH tokens are part of the Balancer pool and someone queries the latestRoundData() function. There is currently no response or mitigation suggested for this bug.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-12-plaza-finance-judging/issues/981 

The protocol has acknowledged this issue.

## Found by 
056Security, 0rpse, 0xAadi, 0xShahilHussain, 0xadrii, Adotsam, Aymen0909, KiroBrejka, noromeb, pashap9990, sl1, solidityenj0yer, whitehat777, x0lohaclohell

### Summary

The BalancerOracleAdapter.sol contract relies on Chainlink price feeds to calculate the prices of tokens used in a Balancer pool to determine the reserveToken. However, the Chainlink price feed aggregators for wstETH/USD and stETH/USD do not exist. When these tokens are included in the Balancer pool, calls to latestRoundData() will revert, as the price feeds are unavailable.

### Root Cause

https://github.com/sherlock-audit/2024-12-plaza-finance/blob/14a962c52a8f4731bbe4655a2f6d0d85e144c7c2/plaza-evm/src/BalancerOracleAdapter.sol#L109

In the latestRoundData() function, the contract attempts to fetch prices for each token in the pool via Chainlink price feeds:

For tokens like wstETH and stETH, the contract expects a price feed in the form of wstETH/USD or stETH/USD. However, Chainlink does not provide such price feeds. As a result, any attempt to calculate prices for these tokens will fail, causing the contract to revert.


```javascript
    function latestRoundData() external view returns (uint80, int256, uint256, uint256, uint80) {
        .
        .
        .
        for(uint8 i = 0; i < tokens.length; i++) {
            oracleDecimals = getOracleDecimals(address(tokens[i]), USD);
@>          prices[i] = getOraclePrice(address(tokens[i]), USD).normalizeAmount(oracleDecimals, decimals);
        }
        .
        .
        .
    }
```

### Internal Pre-conditions

The Balancer pool contains wstETH or stETH as part of the tokens.

### External Pre-conditions

	The protocol or user queries the latestRoundData() function to fetch the price of tokens in the pool.

### Attack Path

_No response_

### Impact

	If wstETH or stETH tokens are part of the Balancer pool, the latestRoundData() function will always revert.

### PoC

_No response_

### Mitigation

_No response_

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Plaza Finance |
| Report Date | N/A |
| Finders | Adotsam, 056Security, noromeb, 0xAadi, KiroBrejka, whitehat777, 0rpse, solidityenj0yer, Aymen0909, pashap9990, 0xShahilHussain, 0xadrii, x0lohaclohell, sl1 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-12-plaza-finance-judging/issues/981
- **Contest**: https://app.sherlock.xyz/audits/contests/682

### Keywords for Search

`vulnerability`

