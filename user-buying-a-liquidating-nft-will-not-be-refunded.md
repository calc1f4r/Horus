---
# Core Classification
protocol: Nemeos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59593
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
source_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
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
finders_count: 3
finders:
  - Sebastian Banescu
  - Faycal Lalidji
  - Guillermo Escobero
---

## Vulnerability Title

User Buying a Liquidating NFT Will Not Be Refunded

### Overview


The DutchAuctionLiquidator contract has a bug where it does not refund the user buying a NFT for the difference between the ETH they paid and the current price. This has been fixed in the latest update and the pool will now only receive the expected price. The liquidator will receive any excess of the tokens paid. It is recommended to confirm if this is the intended behavior and consider refunding the user if not.

### Original Finding Content

**Update**
Fixed in `cb5cf9578eec80aaa537abf6cf39ae3dbdb4e456` and `7a817943a8cb2176ba03f88105aa1196c68cce61`. The pool will only receive the expected price `currentPrice`. The liquidator will receive any excess of the tokens paid (`msg.value - currentPrice`).

**File(s) affected:**`DutchAuctionLiquidator.sol`

**Description:** When a borrower is late in his loan payments, other users can start a liquidation process. Any address can call `DutchAuctionLiquidator.buy()` and buy the NFT at `currentPrice` (linearly decreasing from the starting loan price).

`DutchAuctionLiquidator.buy()` validates that the ETH being paid is greater than this price (strict equality will not work here as the price changes with block timestamp). However, it does not refund the user buying the NFT for that difference (`msg.value - currentPrice`).

This difference will be sent to the user being liquidated in the `Pool` contract (`Pool.refundFromLiquidation()`).

**Recommendation:** Confirm that this is the expected behavior. If not, consider refunding the user buying the liquidated NFT.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Nemeos |
| Report Date | N/A |
| Finders | Sebastian Banescu, Faycal Lalidji, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html

### Keywords for Search

`vulnerability`

