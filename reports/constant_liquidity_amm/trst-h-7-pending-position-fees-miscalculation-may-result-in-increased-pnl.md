---
# Core Classification
protocol: Stella
chain: everychain
category: logic
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19051
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
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
  - wrong_math
  - business_logic

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-H-7 Pending position fees miscalculation may result in increased PnL

### Overview


This bug report concerns the NonfungiblePositionManager contract, which manages positions in Uniswap V3 pools on behalf of users. When calculating pending liquidity position fees, the code was reading values for liquidity, tokensOwed0, and tokensOwed1 from the pool that included amounts from all users who had deposited funds in the price range of the position. This caused the PnL of UniswapV3Strategy positions to be significantly increased, resulting in increased payouts to lenders and loss of funds to borrowers/liquidators.

The recommended mitigation was to read the values of liquidity, tokensOwed0, and tokensOwed1 from the `IUniswapV3NPM(uniV3NPM).positions()` call on line 95. This call returns values specifically for the position identified by the token ID, and the team has fixed it as recommended to make the logic correct.

### Original Finding Content

**Description:**
When calculating pending liquidity position fees, **liquidity, tokensOwed0, and tokensOwed1**
are read from a Uniswap V3 pool using a position belonging to the 
NonfungiblePositionManager contract. However, the read values will also include the liquidity 
and the owed token amounts of all Uniswap V3 users who deposited funds in the price range 
of the position via the NonfungiblePositionManager contract. Since 
NonfungiblePositionManager manages positions in pools on behalf of users, the positions will 
hold liquidity of all NonfungiblePositionManager users. As a result, the PnL of 
UniswapV3Strategy positions may be significantly increased, resulting in increased payouts to 
lenders and loss of funds to borrowers/liquidators.

**Recommended Mitigation:**
Consider reading the values of liquidity, **tokensOwed0, and tokensOwed1** from the 
`IUniswapV3NPM(uniV3NPM).positions()` call on line 95. The call returns values specifically for 
the position identified by the token ID.

**Team response:**
Fixed.

**Mitigation Review:**
The team has fixed it as recommended to make the logic correct.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Stella |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Wrong Math, Business Logic`

