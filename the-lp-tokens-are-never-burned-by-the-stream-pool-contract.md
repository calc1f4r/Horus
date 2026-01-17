---
# Core Classification
protocol: PixelSwap DEX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45155
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-12-pixelswap-dex-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-12-pixelswap-dex-securityreview.pdf
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
finders_count: 2
finders:
  - Guillermo Larregay
  - Tarun Bansal
---

## Vulnerability Title

The LP tokens are never burned by the Stream Pool contract

### Overview


This bug report describes a low difficulty bug related to data validation in the contract "jetton/jetton_factory.tact". The "PixelswapStreamPool" contract is sending the "burn" message to the Jetton master contract of the pair's LP token instead of the Jetton wallet owned by itself. This results in LP tokens not being burned when users remove their liquidity. This bug can be exploited by adding and removing a large amount of liquidity, resulting in an increase in the LP token balance of the "PixelswapStreamPool" contract. The report recommends updating the "burn" function of the "JettonFactory" trait contract to send the burn message to the Jetton wallet owned by the "PixelswapStreamPool" contract in the short term and checking the system state after a transaction in the long term. The team has determined that this issue has been resolved after conducting a fix review.

### Original Finding Content

## Diﬃculty: Low

## Type: Data Validation

### Target: contracts/jetton/jetton_factory.tact

### Description

The `PixelswapStreamPool` contract sends the `burn` message to the Jetton master contract of the pair's LP token instead of the Jetton wallet owned by itself. This results in the LP tokens never being burned. Users remove their liquidity by transferring their LP tokens to the `PixelswapStreamPool` contract with a payload to send the `RemoveLiquidityJettonNotification` message to the `PixelswapStreamPool` contract. The `RemoveLiquidityJettonNotification` handler function of the Stream Pool contract updates the reserves and LP token supply stored in the `pair_config` map and calls the `self.burn` function. The `burn` function is inherited from the `JettonFactory` trait contract:

**[Redacted]**

The `burn` function of the `JettonFactory` trait sends the `burn` message to the Jetton master contract of the LP token with the `bounce` flag set to `false`. The Jetton master contract reverts the transaction, and the `burn` message is never processed by the Jetton contracts of the LP token.

### Exploit Scenario

Alice adds 1,000,000,000 nanotons TON and 1,000,000,000 nanotons USDC to the pool and mints 1,000,000,000 nanotons LP tokens. After some time, Alice removes her liquidity by transferring her LP tokens to the `PixelswapStreamPool` contract, but the LP tokens are not burned by the Stream Pool contract, and the LP token balance of the Stream Pool contract is increased by 1,000,000,000 nanotons LP tokens.

### Recommendations

- **Short term**: Update the `burn` function of the `JettonFactory` trait contract to send the burn message to the Jetton wallet owned by the Stream Pool contract.
- **Long term**: Check the whole system state after a transaction in a test case to ensure correctness of the test cases.

### Fix Review Status

After conducting a fix review, the team determined that this issue has been resolved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | PixelSwap DEX |
| Report Date | N/A |
| Finders | Guillermo Larregay, Tarun Bansal |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-12-pixelswap-dex-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-12-pixelswap-dex-securityreview.pdf

### Keywords for Search

`vulnerability`

