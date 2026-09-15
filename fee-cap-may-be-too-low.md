---
# Core Classification
protocol: USDT0 Polygon Integration Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62197
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/usdt0-polygon-integration-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Fee Cap May Be Too Low

### Overview


The bug report states that there is a problem with the fee cap set for the deployment of the `Polygon_SpokePool` contract. The fee is calculated in source-chain-native tokens, but the set fee cap may not be enough to cover the execution fee on the destination chain, which is Ethereum mainnet. This is because the native token on the Polygon network is POL, which is worth about USD ~0.24, and the fee for transfers from L2 chains to Ethereum mainnet is currently quoted at USD ~1.26 (about 5 POL). This means that cross-chain transfers for USDT0 may fail. To fix this issue, it is suggested to set a higher fee cap that takes into account the lower value of the native POL token compared to ETH. The bug has been resolved in a recent commit.

### Original Finding Content

A [fee cap](https://github.com/across-protocol/contracts/blob/d9826e30b51bbb3067df07c9532f4a5f6fe56f1c/deploy/011_deploy_polygon_spokepool.ts#L24) of `1e18` is set upon the deployment of the `Polygon_SpokePool` contract. Since the fee is calculated for execution on the destination chain but is expressed in source-chain-native tokens, the fee required may be higher than the set `feeCap`. On the Polygon network, the native token is POL and 1 unit of POL is equal to USD ~0.24. This is unlikely to cover the execution fee for the destination chain (Ethereum mainnet). For example, fees for USDT0 transfers from L2 chains such as Optimism to Ethereum mainnet are quoted at USD ~1.26 at this time (about 5 POL). The LayerZero documentation also provides a helpful [example](https://docs.layerzero.network/v2/concepts/protocol/transaction-pricing#example-scenario) of fee calculation for Polygon to Ethereum mainnet transfers. Therefore, cross-chain transfers for USDT0 - where the destination chain is Ethereum mainnet - may fail.

Consider setting a higher fee cap which takes into account the lower relative value of the native POL token to ETH.

**Update**: *Resolved in [commit 6a9655e](https://github.com/across-protocol/contracts/pull/1083/commits/6a9655ea8bc7d7f526f6c7be7a94509372703a93).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | USDT0 Polygon Integration Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/usdt0-polygon-integration-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

