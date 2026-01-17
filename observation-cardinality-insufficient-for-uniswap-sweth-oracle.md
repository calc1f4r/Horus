---
# Core Classification
protocol: Ion Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32704
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ion-protocol-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Observation Cardinality Insufficient for Uniswap SwETH Oracle

### Overview


The SwEthSpotOracle contract uses a Uniswap v3 TWAP oracle to get the price of the swETH token. However, the intended pool does not have a large enough observation cardinality to support the TWAP window. This could prevent users from modifying their positions and result in liquidation of vaults. To fix this, the observation cardinality of the pool should be increased and the TWAP should not be used until it reaches the target amount. The Ion Protocol team is aware of this issue and will not launch with Swell's stETH until it is resolved.

### Original Finding Content

The [`SwEthSpotOracle` contract](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/spot/SwEthSpotOracle.sol#L11) uses a Uniswap v3 TWAP oracle to get the price of the swETH token. The [intended pool (ETH/swETH 0.05% fee pool)](https://info.uniswap.org/home#/pools/0x30ea22c879628514f1494d4bbfef79d21a6b49a2) does not currently have a large enough [observation cardinality](https://uniswapv3book.com/docs/milestone_5/price-oracle/#observations-and-cardinality) to support the TWAP window (2 hours) intended to be used. The observation cardinality of the pool should be at least as large as the number of blocks in the TWAP window (600 blocks) otherwise the TWAP calculation may fail as the Uniswap pool would not contain any data from the beginning of the TWAP window.


This would prevent users from [modifying their positions](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L679). As a result, vaults could be liquidated if there was a sufficient change in the exchange rate and users would be unable to repay their debt, or deposit collateral into their vault to prevent liquidation.


Consider increasing the observation cardinality for the pool by calling the `increaseObservationCardinalityNext` function on the pool contract with an input amount that is at least as large as the number of blocks within the TWAP window. Further, the TWAP should not be used until the Uniswap pool observation cardinality has increased to the target amount. The constructor for the `SwEthSpotOracle` contract should validate that the observation cardinality is sufficiently large when deploying the contract.


***Update:** Acknowledged, will resolve. Ion Protocol team stated:*



> *This is a known issue. The team is aware that the observation cardinality of the swETH Uniswap AMM needs to be increased for the TWAP to function properly. We will not be launching with Swell's stETH until the observation cardinality is increased.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Ion Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ion-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

