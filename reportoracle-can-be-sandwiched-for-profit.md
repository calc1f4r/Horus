---
# Core Classification
protocol: Geodefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20752
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/11/geodefi/
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
  - Sergii Kravchenko
  -  Christian Goll
  -  Chingiz Mardanov

---

## Vulnerability Title

reportOracle can be sandwiched for profit.

### Overview


This bug report discusses the potential for a MEV searcher to exploit the price update of an on-chain transaction. This would allow the searcher to predict the future price of the transaction and then act accordingly. For example, the searcher could use a flash loan to mint as much gETH as possible, then bundle the transaction, and finally redeem the gETH for ETH at a higher price per share. This attack could be profitable, despite the fees associated with it, if the oracle is not updated frequently enough. To prevent this attack, the oracle should be updated daily.

### Original Finding Content

#### Description


The fact that price update happens in an on-chain transaction gives the searches the ability to see the future price and then act accordingly.


#### Examples


MEV searcher can find the `reportOracle` transaction in the mem-pool and if the price is about to increase he could proceed to mint as much gETH as he can with a flash loan. They would then bundle the `reportOracle` transaction. Finally, they would redeem all the gETH for ETH at a higher price per share value as the last transaction in the bundle.


This paired with the fact that oracle might be updated less frequently than once per day, could lead to the fact that profits from this attack will outweigh the fees for performing it.


Fortunately, due to the nature of the protocol, the price fluctuations from day to day will most likely be smaller than the fees encountered during this arbitrage, but this is still something to be aware of when updating the values for DWP donations and fees. But it also makes it crucial to update the oracle every day not to increase the profit margins for this attack.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Geodefi |
| Report Date | N/A |
| Finders | Sergii Kravchenko,  Christian Goll,  Chingiz Mardanov
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/11/geodefi/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

