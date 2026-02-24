---
# Core Classification
protocol: Vertex Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48378
audit_firm: OtterSec
contest_link: https://vertexprotocol.io/
source_link: https://vertexprotocol.io/
github_link: github.com/vertex-protocol/vertex-evm.

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
finders_count: 4
finders:
  - Shiva Shankar
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Improper Settlement Calculation

### Overview


The bug report is about an error in the PerpEngine code that calculates the amount that users can settle in the perp market. The current code does not consider the user's portion of the liquidity pool when calculating profit and loss, leading to inconsistencies and a drain of funds. The suggested solution is to change the calculation to consider the ratio of the user's liquidity pool amount to the total pool amount. This issue has been fixed in a recent patch.

### Original Finding Content

## PerpEngine Settlement State Calculation

In PerpEngine, `getSettlementState` is used to calculate the amount that users can settle at that time by calculating the total profit/loss that they made in the perp market.

## Code Snippet
```solidity
contracts/PerpEngine.sol
(int256 ammBaseX18, int256 ammQuoteX18) = MathHelper.ammEquilibrium(
    lpState.base.fromInt(),
    lpState.quote.fromInt(),
    priceX18
);

int256 positionPnlX18 = priceX18.mul(balance.amountX18 + ammBaseX18) +
    balance.vQuoteBalanceX18 +
    ammQuoteX18;
```

## Profit and Loss Calculations
For profit and loss calculations, the entire pool’s base and quote balance is considered, whereas the user’s portion (`lpBalance/supply`) of the amount in it only needs to be considered. Every user will receive the entire liquidity pool’s base and quote value in their profit, leading to a drain of funds and inconsistencies.

## Remediation
Consider `amountLp/supply` ratio of pool liquidity for calculating the user’s PNL.

## Patch
The Position PNL calculation is changed to consider only `amountLp/supply` ratio of `ammBase` and `ammQuote` amounts. Fixed in #130.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Vertex Protocol |
| Report Date | N/A |
| Finders | Shiva Shankar, Robert Chen, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://vertexprotocol.io/
- **GitHub**: github.com/vertex-protocol/vertex-evm.
- **Contest**: https://vertexprotocol.io/

### Keywords for Search

`vulnerability`

