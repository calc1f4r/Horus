---
# Core Classification
protocol: MCDEX Mai Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13717
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/05/mcdex-mai-protocol-v2/
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Martin Ortner
  - Alexander Wade
---

## Vulnerability Title

AMM - Amount of collateral spent or shares received may be unpredictable for liquidity provider  Acknowledged

### Overview


This bug report is about the unpredictability of the `addLiquidity()` and `removeLiquidity()` functions when providing or removing liquidity in a decentralized finance (DeFi) protocol. The price of the assets in the protocol can fluctuate at any time, making it difficult for users to predict the behavior of the functions. 

In order to make the functions more predictable, the report recommends allowing the caller to specify a price limit or maximum amount of collateral to be spent, and also to specify the minimum amount of shares expected to be received. This will help users to know what to expect when using the functions.

### Original Finding Content

#### Resolution



The client acknowledges this issue without providing further information or implementing the recommended fixes.


#### Description


When providing liquidity with `addLiquidity()`, the amount of collateral required is based on the current price and the amount of shares received depends on the total amount of shares in circulation. This price can fluctuate at a moment’s notice, making the behavior of the function unpredictable for the user.


The same is true when removing liquidity via `removeLiquidity()`.


#### Recommendation


Unpredictability can be introduced by someone front-running the transaction, or simply by poor timing. For example, adjustments to global variable configuration by the system admin will directly impact subsequent actions by the user. In order to ensure users know what to expect:


* Allow the caller to specify a price limit or maximum amount of collateral to be spent
* Allow the caller to specify the minimum amount of shares expected to be received

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | MCDEX Mai Protocol V2 |
| Report Date | N/A |
| Finders | Martin Ortner, Alexander Wade |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/05/mcdex-mai-protocol-v2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

