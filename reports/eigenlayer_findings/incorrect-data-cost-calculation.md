---
# Core Classification
protocol: Omni Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53596
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma_Prime_Omni_Network_Omni_Chain_2_Security_Assessment_Report_v2_1.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma_Prime_Omni_Network_Omni_Chain_2_Security_Assessment_Report_v2_1.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Incorrect Data Cost Calculation

### Overview


The report highlights an issue with the calculation of data costs for cross-chain transactions on the Omni platform. The current method of calculating data costs does not account for the size of the entire transaction and can result in users paying lower fees than intended. The report recommends adding a fixed amount of overhead to the data cost calculation and implementing a premium based on the confirmation level of the transaction to account for volatility in gas prices and exchange rates. The Omni team has acknowledged the issue and is working on a solution in FeeOracleV2.

### Original Finding Content

## Description

There are components to the data cost calculation that are incorrect or do not account for gas and asset price volatility, which can lead to a fee that is lower than intended.

The `FeeOracleV1.feeFor()` function uses the size of the transaction input data (also referred to as calldata) to calculate `dataGas`. This assumes that rollups only post transaction input data and does not include other transaction fields such as transaction nonce, gas price, and gas limit.

```solidity
IFeeOracleV1.ChainFeeParams storage dataP = _feeParams[execP.postsTo];
// ...
// @audit dataGasPrice uses the current `dataP.gasPrice` and `dataP.toNativeRate` values
uint256 dataGasPrice = dataP.gasPrice * dataP.toNativeRate / CONVERSION_RATE_DENOM;
// 16 gas per non-zero byte, assume non-zero bytes
// TODO: given we mostly support rollups that post data to L1, it may be cheaper for users to count
// non-zero bytes (consuming L2 execution gas) to reduce their L1 data fee
// @audit data.length refers to the size of the cross-chain call's calldata
uint256 dataGas = data.length * 16;
```

Rollups such as Optimism and Base post the entire signed transaction serialized with RLP encoding. This means that the size of the posted data for a transaction is larger than just the transaction input data.

Furthermore, the `dataGasPrice` used in data cost calculation does not account for the volatility of the destination chain’s gas price, as well as the volatility in the exchange rate of the destination chain’s native token relative to the source chain’s native token. These values can vary greatly at the time of execution of the `XMsg` in `OmniPortal.xsubmit()`, resulting in the user paying less than the intended amount of fees.

## Recommendations

- To account for the data size of the total RLP encoded signed transaction, add a fixed amount of data to the data cost calculation as overhead.
- To account for the volatility in the destination chain’s gas price and the exchange rate of the destination chain’s native token relative to the source chain’s native token, add a premium to `dataGasPrice` that is dependent on the confirmation level of the `XMsg`. For example, an `XMsg` that uses the latest confirmation level can be charged a 10% premium, while an `XMsg` that uses the finalized confirmation level can be charged a 20% premium since the delay between calling `xcall()` and `xsubmit()` is longer.

## Resolution

The Omni team has acknowledged this issue with the following comment:

> "We are aware of this issue and have performed PnL analysis on our testnet to ensure that we do not undercharge for data. We are also working on FeeOracleV2 to address all fee-related issues brought up in this review."

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Omni Network |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma_Prime_Omni_Network_Omni_Chain_2_Security_Assessment_Report_v2_1.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma_Prime_Omni_Network_Omni_Chain_2_Security_Assessment_Report_v2_1.pdf

### Keywords for Search

`vulnerability`

