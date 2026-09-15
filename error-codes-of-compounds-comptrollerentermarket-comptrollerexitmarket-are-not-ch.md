---
# Core Classification
protocol: DeFi Saver
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13476
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/03/defi-saver/
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
  - cdp
  - yield
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - David Oz Kashi
  - Shayan Eskandari
---

## Vulnerability Title

Error codes of Compound’s Comptroller.enterMarket, Comptroller.exitMarket are not checked ✓ Fixed

### Overview


This bug report is about an issue with Compound's enterMarket/exitMarket functions, which return an error code instead of reverting in case of failure. The DeFi Saver smart contracts do not check for the error codes returned from Compound smart contracts, which could lead to unexpected results. The code flow might revert due to unavailability of the CTokens, but early on checks for Compound errors are suggested. The caller contract should revert in case the error code is not 0. The bug has now been fixed in DecenterApps/[email protected]`7075e49` by reverting in the case the return value is non zero.

### Original Finding Content

#### Resolution



Fixed in [DecenterApps/[email protected]`7075e49`](https://github.com/DecenterApps/defisaver-v3-contracts/commit/7075e490bde07ad82fe8b904eea1c076c7efe391) by reverting in the case the return value is non zero.


#### Description


Compound’s `enterMarket/exitMarket` functions return an error code instead of reverting in case of failure.
DeFi Saver smart contracts never check for the error codes returned from Compound smart contracts, although the code flow might revert due to unavailability of the CTokens, however early on checks for Compound errors are suggested.


#### Examples


**code/contracts/actions/compound/helpers/CompHelper.sol:L26-L37**



```
function enterMarket(address \_cTokenAddr) public {
    address[] memory markets = new address[](1);
    markets[0] = \_cTokenAddr;

    IComptroller(COMPTROLLER\_ADDR).enterMarkets(markets);
}

/// @notice Exits the Compound market
/// @param \_cTokenAddr CToken address of the token
function exitMarket(address \_cTokenAddr) public {
    IComptroller(COMPTROLLER\_ADDR).exitMarket(\_cTokenAddr);
}

```
#### Recommendation


Caller contract should revert in case the error code is not 0.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | DeFi Saver |
| Report Date | N/A |
| Finders | David Oz Kashi, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/03/defi-saver/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

