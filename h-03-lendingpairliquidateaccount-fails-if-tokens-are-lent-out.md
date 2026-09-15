---
# Core Classification
protocol: Wild Credit
chain: everychain
category: uncategorized
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 469
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-wild-credit-contest
source_link: https://code4rena.com/reports/2021-07-wildcredit
github_link: https://github.com/code-423n4/2021-07-wildcredit-findings/issues/123

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - liquidation

protocol_categories:
  - dexes
  - cdp
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[H-03] LendingPair.liquidateAccount fails if tokens are lent out

### Overview


This bug report is about the `LendingPair.liquidateAccount` function in a lending protocol. This function is used to pay out underlying supply tokens to the liquidator, however, there may not be enough of the supply tokens in the contract to do so. This is because the contract only ensures a certain minimum reserve. As a result, liquidations cannot be performed if all tokens are lent out. 

As an example, if user A supplies 1k$ WETH and user B supplies 1.5k$ DAI and borrows the ~1k$ WETH (leaving only the minimum reserve), the ETH price drops but user B cannot be liquidated as there is not enough WETH in the pool. 

The recommendation is to mint LP supply tokens to the message sender instead. This way, the liquidator can seize the borrower's LP tokens.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

The `LendingPair.liquidateAccount` function tries to pay out underlying supply tokens to the liquidator using `_safeTransfer(IERC20(supplyToken), msg.sender, supplyOutput)` but there's no reason why there should be enough `supplyOutput` amount in the contract, the contract only ensures `minReserve`.

## Impact
No liquidations can be performed if all tokens are lent out.
Example: User A supplies 1k$ WETH, User B supplies 1.5k$ DAI and borrows the ~1k$ WETH (only leaves `minReserve`). The ETH price drops but user B cannot be liquidated as there's not enough WETH in the pool anymore to pay out the liquidator.

## Recommendation
Mint LP supply tokens to `msg.sender` instead, these are the LP supply tokens that were burnt from the borrower. This way the liquidator basically seizes the borrower's LP tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Wild Credit |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-wildcredit
- **GitHub**: https://github.com/code-423n4/2021-07-wildcredit-findings/issues/123
- **Contest**: https://code4rena.com/contests/2021-07-wild-credit-contest

### Keywords for Search

`Liquidation`

