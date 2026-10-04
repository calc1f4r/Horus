---
# Core Classification
protocol: Futureswap V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11129
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/futureswap-v2-audit/
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

protocol_categories:
  - dexes
  - services
  - derivatives
  - liquidity_manager
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Exchanges

### Overview


Futureswap is a decentralized exchange platform that allows users to trade assets with up to 20x leverage. The exchange is created by governance via the ExchangeFactory and liquidity can be added to the exchange by liquidity providers in exchange for non-transferable liquidity tokens. These tokens represent a share of the exchange’s liquidity and can be redeemed. Traders can open leveraged long or short positions with up to 20x leverage. This bug report is about the ExchangeFactory, which is responsible for creating the exchange. It is defined by an asset token and a stablecoin, and is used to add liquidity to the exchange.

### Original Finding Content

A Futureswap [`Exchange`](https://github.com/futureswap/fs_core/blob/96255fc4a550a5f34681c117b5969b848d07b3a3/contracts/exchange/Exchange.sol) is defined by [an asset token and a stablecoin](https://github.com/futureswap/fs_core/blob/96255fc4a550a5f34681c117b5969b848d07b3a3/contracts/exchange/Exchange.sol#L31). An exchange can be created by governance via the [`ExchangeFactory`](https://github.com/futureswap/fs_core/blob/96255fc4a550a5f34681c117b5969b848d07b3a3/contracts/exchange/ExchangeFactory.sol). Liquidity providers can add liquidity to the exchange, in exchange for non-transferable [liquidity tokens](https://github.com/futureswap/fs_core/blob/96255fc4a550a5f34681c117b5969b848d07b3a3/contracts/liquidity/LiquidityToken.sol). These liquidity tokens represent a share of the exchange’s liquidity and can be redeemed.


Traders can open leveraged long or short positions with up to 20x leverage.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Futureswap V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/futureswap-v2-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

